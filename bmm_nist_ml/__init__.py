import json
import os.path
from pathlib import Path

import numpy as np
from scipy import spatial

import bluesky.plans as bp
import bluesky.plan_stubs as bps

from ophyd import Component as Cpt, Device, Signal
from ophyd.sim import SynAxis, SynSignal

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


def load_xafs_scans_json():
    init_path = Path(os.path.abspath(__file__))
    data_path = init_path.parent.parent / "data" / "xafs_scans.json"
    with open(data_path, "rt") as data_file:
        xafs_scans = json.load(data_file)
    print(f"loaded {len(xafs_scans)} scans from {data_path}")
    return xafs_scans


def load_xafs_scans():
    xafs_scans = load_xafs_scans_json()
    row_count = len(xafs_scans)
    column_count = 2
    xafs_scans_xy = np.zeros((row_count, column_count))
    xafs_scans_list = []
    for row_i, (uuid, scan_info) in enumerate(xafs_scans.items()):
        xafs_scans_xy[row_i, :] = scan_info["x"], scan_info["y"]
        scan_info["uuid"] = uuid
        xafs_scans_list.append(scan_info)

    return xafs_scans_xy, xafs_scans_list


class BmmNistMlDetector(Device):
    """
    Evaluate a point on a Gaussian based on the value of a motor.
    Parameters
    ----------
    name : str
        The name of the detector
    motor0 : SynAxis
        The 'x' coordinate of the 2-D gaussian blob
    motor_field0 : str
        The name field of the motor. Should be the key in motor0.describe()
    motor1 : SynAxis
        The 'y' coordinate of the 2-D gaussian blob
    motor_field1 : str
        The name field of the motor. Should be the key in motor1.describe()
    center : iterable, optional
        The center of the gaussian blob
        Defaults to (0,0)
    Imax : float, optional
        The intensity at `center`
        Defaults to 1
    sigma : float, optional
        Standard deviation for gaussian blob
        Defaults to 1
    noise : {'poisson', 'uniform', None}, optional
        Add noise to the gaussian peak..
        Defaults to None
    noise_multiplier : float, optional
        Only relevant for 'uniform' noise. Multiply the random amount of
        noise by 'noise_multiplier'
        Defaults to 1
    random_state : numpy random state object, optional
        np.random.RandomState(0), to generate random number with given seed
    Example
    -------
    motor = SynAxis(name='motor')
    det = SynGauss('det', motor, 'motor', center=0, Imax=1, sigma=1)
    """

    val = Cpt(SynSignal, kind="hinted")
    # Imax = Cpt(Signal, value=10, kind="config")
    # center = Cpt(Signal, value=0, kind="config")
    # sigma = Cpt(Signal, value=1, kind="config")
    # noise = Cpt(
    #     EnumSignal,
    #     value="none",
    #     kind="config",
    #     enum_strings=("none", "poisson", "uniform"),
    # )
    # noise_multiplier = Cpt(Signal, value=1, kind="config")

    def get_neaest_distance_and_index(self, x, y):
        nearest_distance, nearest_index = self.xafs_kd_tree.query([x, y])
        print(f"nearest distance to {x},{y} is {nearest_distance}")
        print(f"scan_info for nearest point is {self.xafs_scans_list[nearest_index]}")
        return nearest_distance, nearest_index

    def _compute(self):
        x = self._motor0.read()[self._motor_field0]["value"]
        y = self._motor1.read()[self._motor_field1]["value"]

        nearest_distance, nearest_index = self.get_neaest_distance_and_index(x, y)
        v = x * y
        #m = np.array([x, y])
        # Imax = self.Imax.get()
        # center = self.center.get()
        # sigma = self.sigma.get()
        # noise = self.noise.get()
        # noise_multiplier = self.noise_multiplier.get()
        # v = Imax * np.exp(-np.sum((m - center) ** 2) / (2 * sigma ** 2))
        # if noise == "poisson":
        #     v = int(self.random_state.poisson(np.round(v), 1))
        # elif noise == "uniform":
        #     v += self.random_state.uniform(-1, 1) * noise_multiplier
        return v

    def __init__(
        self,
        name,
        motor0,
        motor_field0,
        motor1,
        motor_field1,
        # center,
        # Imax,
        # sigma=1,
        # noise="none",
        # noise_multiplier=1,
        # random_state=None,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self._motor0 = motor0
        self._motor1 = motor1
        self._motor_field0 = motor_field0
        self._motor_field1 = motor_field1

        self.xafs_scans_xy, self.xafs_scans_list = load_xafs_scans()
        self.xafs_kd_tree = spatial.KDTree(self.xafs_scans_xy)
        # self.center.put(center)
        # self.Imax.put(Imax)
        # self.sigma.put(sigma)
        # self.noise.put(noise)
        # self.noise_multiplier.put(noise_multiplier)

        # if random_state is None:
        #     random_state = np.random
        # self.random_state = random_state
        self.val.name = self.name
        self.val.sim_set_func(self._compute)

        self.trigger()

    def trigger(self, *args, **kwargs):
        return self.val.trigger(*args, **kwargs)


def the_plan(x1, x2):
    motor1 = SynAxis(name="motor1", labels={"motors"})
    motor2 = SynAxis(name="motor2", labels={"motors"})

    detector = BmmNistMlDetector("det", motor1, "motoe1", motor2, "motor2")
    yield bps.mv(motor1, x1)
    yield bps.mv(motor2, x2)
    yield bp.count([detector])
