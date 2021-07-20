from bluesky import RunEngine

from bmm_nist_ml import serializer, the_plan

RE = RunEngine()
RE.subscribe(serializer)

