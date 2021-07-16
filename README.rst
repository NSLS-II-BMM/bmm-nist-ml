===========
bmm-nist-ml
===========

* Free software: 3-clause BSD license

Prerequisites
-------------
  * Vagrant
  * VirtualBox

Installation
------------

Clone this repository and change to the top-level directory. Build the VM::

  $ vagrant up
  ...

SSH into the VM and install the demonstration code::

  $ vagrant ssh
  ...
  vagrant@vagrant:~$ conda activate bluesky_queueserver
  (bluesky_queueserver) vagrant@vagrant:~$ cd /vagrant
  (bluesky_queueserver) vagrant@vagrant:/vagrant$ pip install -e .
  ...

Run the Demonstration Plan
--------------------------

From the same terminal start the RunEngine manager::

  (bluesky_queueserver) vagrant@vagrant:/vagrant$ start-re-manager --startup-dir /vagrant/bmm_nist_ml_startup
  INFO:bluesky_queueserver.manager.manager:Starting ZMQ server at 'tcp://*:60615'
  INFO:bluesky_queueserver.manager.manager:ZMQ control channels: encryption disabled
  INFO:bluesky_queueserver.manager.manager:Starting RE Manager process
  INFO:bluesky_queueserver.manager.manager:Loading the lists of allowed plans and devices ...
  INFO:bluesky_queueserver.manager.manager:Starting ZeroMQ server ...
  INFO:bluesky_queueserver.manager.manager:ZeroMQ server is waiting on tcp://*:60615

Open a new terminal (or the equivalent) and SSH into the VM. Start uvicorn::

  $ vagrant ssh
  Last login: Fri Jul 16 20:21:01 2021 from 10.0.2.2
  vagrant@vagrant:~$ conda activate bluesky_queueserver
  (bluesky_queueserver) vagrant@vagrant:~$ uvicorn bluesky_queueserver.server.server:app --host localhost --port 60610
  INFO:     Started server process [17483]
  INFO:uvicorn.error:Started server process [17483]
  INFO:     Waiting for application startup.
  INFO:uvicorn.error:Waiting for application startup.
  INFO:bluesky_queueserver.manager.comms:Connected to ZeroMQ server 'tcp://localhost:60615'
  INFO:bluesky_queueserver.manager.comms:ZMQ encryption: disabled
  INFO:bluesky_queueserver.server.server:Bluesky HTTP Server started successfully
  INFO:     Application startup complete.
  INFO:uvicorn.error:Application startup complete.
  INFO:     Uvicorn running on http://localhost:60610 (Press CTRL+C to quit)
  INFO:uvicorn.error:Uvicorn running on http://localhost:60610 (Press CTRL+C to quit)

Open a third terminal and SSH into the VM. Check the status of the queueserver::

  $ vagrant ssh
  Last login: Fri Jul 16 19:58:44 2021 from 10.0.2.2
  vagrant@vagrant:~$ conda activate bluesky_queueserver
  (bluesky_queueserver) vagrant@vagrant:~$ qserver status
  Arguments: ['status']
  20:08:57 - MESSAGE: {'devices_allowed_uid': 'db485474-988f-4367-b57c-a1df3b11889d',
   'items_in_history': 0,
   'items_in_queue': 0,
   'manager_state': 'idle',
   'msg': 'RE Manager',
   'plan_history_uid': '0fef2a51-af99-43ec-8fbb-75dc97995946',
   'plan_queue_mode': {'loop': False},
   'plan_queue_uid': '9854c453-8d4a-4f50-a444-eb6329344030',
   'plans_allowed_uid': '719a80ac-9b7b-42d4-84d0-f9c28fb063f2',
   'queue_stop_pending': False,
   're_state': None,
   'run_list_uid': '0e5a5be5-d07d-4d3c-af4c-28912caeb2ac',
   'running_item_uid': None,
   'worker_environment_exists': False}

In the same terminal open an environment, add the plan to the queue, and process the queue::

  (bluesky_queueserver) vagrant@vagrant:~$ qserver environment open
  Arguments: ['environment', 'open']
  20:25:18 - MESSAGE: {'msg': '', 'success': True}
  (bluesky_queueserver) vagrant@vagrant:~$ qserver queue add plan '{"name":"the_plan", "args":[-70.0, 92.0]}'
  Arguments: ['queue', 'add', 'plan', '{"name":"the_plan", "args":[-70.0, 92.0]}']
  20:25:44 - MESSAGE: {'item': {'args': [-70.0, 92.0],
            'item_type': 'plan',
            'item_uid': '9cef8636-640c-4a07-952f-0846da79a3e1',
            'name': 'the_plan',
            'user': 'qserver-cli',
            'user_group': 'admin'},
   'msg': '',
   'qsize': 1,
   'success': True}
  (bluesky_queueserver) vagrant@vagrant:~$ qserver queue start
  Arguments: ['queue', 'start']
  20:26:03 - MESSAGE: {'msg': '', 'success': True}

The first terminal will show the results of the plan execution::

  INFO:bluesky_queueserver.manager.manager:Adding new item to the queue ...
  INFO:bluesky_queueserver.manager.manager:Item added: success=True item_type='plan' name='the_plan' item_uid='9cef8636-640c-4a07-952f-0846da79a3e1' qsize=1.
  INFO:bluesky_queueserver.manager.worker:Starting execution of a plan ...
  INFO:bluesky_queueserver.manager.worker:Starting a plan 'the_plan'.
  INFO:bluesky_queueserver.manager.manager:Starting queue processing ...
  INFO:bluesky_queueserver.manager.manager:Processing the next queue item: 1 plans are left in the queue.
  INFO:bluesky_queueserver.manager.manager:Starting the plan:
  {'args': [-70.0, 92.0],
   'item_uid': '9cef8636-640c-4a07-952f-0846da79a3e1',
   'kwargs': {},
   'meta': {},
   'name': 'the_plan',
   'user': 'qserver-cli',
   'user_group': 'admin'}.
  loaded 421 scans from /vagrant/data/xafs_scans.json
  nearest distance to 0,0 is 61.4121701865929
  scan_info for nearest point is {'x': -33.300155, 'y': 51.599945, 'element': 'Nb', 'edge': 'K', 'sample': 'NbTiTaV_wisc_V3 (1803016-k2-2 lib2)', 'filename': 'Nb_NbTiTaV_wisc_V3_063_044.001', 'uuid': '85dec0d6-9f69-4866-a298-a1af784fa1ff'}


  Transient Scan ID: 1     Time: 2021-07-16 20:26:04
  Persistent Unique Scan ID: '88129da2-e2f0-4f3d-a168-eea4ff8401f2'
  INFO:bluesky_queueserver.manager.plan_monitoring:New run was open: '88129da2-e2f0-4f3d-a168-eea4ff8401f2'
  nearest distance to -70.0,92.0 is 0.7072029530569732
  scan_info for nearest point is {'x': -69.2998925, 'y': 92.0999275, 'element': 'Ta', 'edge': 'K', 'sample': 'NbTiTaV_wisc_V3 (1803016-k2-2 lib2)', 'filename': 'Ta_NbTiTaV_wisc_V3_018_014.001', 'uuid': 'a8688680-2de5-4c77-85a3-6a9431613643'}
  New stream: 'primary'
  +-----------+------------+------------+
  |   seq_num |       time |        det |
  +-----------+------------+------------+
  |         1 | 20:26:04.4 |  -6440.000 |
  +-----------+------------+------------+
  generator count ['88129da2'] (scan num: 1)



  Run was closed: '88129da2-e2f0-4f3d-a168-eea4ff8401f2'
  INFO:bluesky_queueserver.manager.manager:No items are left in the queue.
  INFO:bluesky_queueserver.manager.manager:Queue is empty.
