import numpy as np

from bluesky import RunEngine
from ophyd.sim import SynAxis
from tiled.client import from_uri

import bmm_nist_ml


def test_load_xafs_scans_json():
    xafs_scans_json = bmm_nist_ml.load_xafs_scans_json()
    assert "1b8eacd2-7caa-4099-8423-9cd138a41ce3" in xafs_scans_json


def test_load_xafs_scans():
    xafs_scans_array, xafs_scans_list = bmm_nist_ml.load_xafs_scans()

    assert xafs_scans_array.shape == (421, 2)
    assert len(xafs_scans_list) == 421

    assert xafs_scans_list[0]["x"] == xafs_scans_array[0, 0]
    assert xafs_scans_list[0]["y"] == xafs_scans_array[0, 1]

    max_x = np.max(xafs_scans_array[:, 0])
    print(f"max_x: {max_x}")
    assert np.round(max_x) == -15.0


def test_get_nearest_distance_and_index():
    motor1 = SynAxis(name="motor1", labels={"motors"})
    motor2 = SynAxis(name="motor2", labels={"motors"})

    det = bmm_nist_ml.BmmNistMlDetector("det", motor1, "motor1", motor2, "motor2")

    # should take these directly from the data
    motor1_position = -69.2998925
    motor2_position = 92.0999275

    motor1.set(motor1_position)
    motor2.set(motor2_position)

    nearest_distance, nearest_index = det.get_nearest_distance_and_index(motor1_position, motor2_position)
    assert nearest_distance == 0.0
    assert nearest_index == 1


def test_detector__compute():
    motor1 = SynAxis(name="motor1", labels={"motors"})
    motor2 = SynAxis(name="motor2", labels={"motors"})

    det = bmm_nist_ml.BmmNistMlDetector("det", motor1, "motor1", motor2, "motor2")

    motor1_position = 3
    motor2_position = 5

    motor1.set(motor1_position)
    motor2.set(motor2_position)

    assert det._compute() == 3*5


def test_the_whole_enchilada():
    RE = RunEngine()

    documents = []

    def accumulate_documents(name, doc):
        documents.append((name, doc))

    RE.subscribe(accumulate_documents)

    run_id = RE(bmm_nist_ml.the_plan(x1=-70.0, x2=92.0))
    assert run_id is not None
    assert len(documents) > 0


def test_the_whole_enchilada_with_db():
    RE = RunEngine()
    RE.subscribe(bmm_nist_ml.serializer)
    catalog = from_uri("http://localhost:8000/bmm")

    documents = []

    def accumulate_documents(name, doc):
        documents.append((name, doc))

    RE.subscribe(accumulate_documents)

    run_id = RE(bmm_nist_ml.the_plan(x1=-70.0, x2=92.0))
    assert run_id is not None
    assert len(documents) > 0

    assert catalog[-1] is not None
