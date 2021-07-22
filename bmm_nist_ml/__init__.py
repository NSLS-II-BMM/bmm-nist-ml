import json
import os.path
from pathlib import Path

import numpy as np
from scipy import spatial

import bluesky.plans as bp
import bluesky.plan_stubs as bps

from ophyd import Component as Cpt, Device, Signal
from ophyd.sim import SynAxis, SynSignal

import suitcase.mongo_normalized

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

serializer = suitcase.mongo_normalized.Serializer(
    "mongodb://localhost:27017/bmm",
    # Why twice? Because Serializer requires you to specify metadatastore and
    # asset registry separately, even though in modern deployments they are
    # typically the same database, only ever separated for historical reasons.
    "mongodb://localhost:27017/bmm",
)


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
    Example
    -------
    motor1 = SynAxis(name='motor1')
    motor2 = SynAxis(name='motor2')
    det = BmmNistMlDetector('det', motor1, 'motor1', motor2, 'motor2')
    """

    val = Cpt(SynSignal, kind="hinted")

    def get_nearest_distance_and_index(self, x, y):
        nearest_distance, nearest_index = self.xafs_kd_tree.query([x, y])
        print(f"nearest distance to {x},{y} is {nearest_distance}")
        print(f"scan_info for nearest point is {self.xafs_scans_list[nearest_index]}")
        return nearest_distance, nearest_index

    def _compute(self):
        x = self._motor0.read()[self._motor_field0]["value"]
        y = self._motor1.read()[self._motor_field1]["value"]

        nearest_distance, nearest_index = self.get_nearest_distance_and_index(x, y)
        v = x * y
        return v

    def __init__(
        self,
        name,
        motor0,
        motor_field0,
        motor1,
        motor_field1,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self._motor0 = motor0
        self._motor1 = motor1
        self._motor_field0 = motor_field0
        self._motor_field1 = motor_field1

        self.xafs_scans_xy, self.xafs_scans_list = load_xafs_scans()
        self.xafs_kd_tree = spatial.KDTree(self.xafs_scans_xy)

        self.val.name = self.name
        self.val.sim_set_func(self._compute)

        # trigger once to set a value in Signal val
        self.trigger()

    def trigger(self, *args, **kwargs):
        return self.val.trigger(*args, **kwargs)


def the_plan(x1, x2):
    motor1 = SynAxis(name="motor1", labels={"motors"})
    motor2 = SynAxis(name="motor2", labels={"motors"})

    detector = BmmNistMlDetector("det", motor1, "motor1", motor2, "motor2")

    yield from bps.mv(motor1, x1)
    yield from bps.mv(motor2, x2)
    yield from bp.count([detector])
    yield from bps.sleep(10)
