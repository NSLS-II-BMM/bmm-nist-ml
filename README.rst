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

Start Services
--------------

Open a terminal and SSH into the VM. Start the qserver, uvicorn, and tiled services::

    $ vagrant ssh
    ...
    vagrant@vagrant:~$ systemctl --user start bluesky_qserver_re_manager.service
    vagrant@vagrant:~$ systemctl --user status bluesky_qserver_re_manager.service
    ● bluesky_qserver_re_manager.service - Bluesky Queueserver RunEngine Manager
         Loaded: loaded (/home/vagrant/.config/systemd/user/bluesky_qserver_re_manager.service; disabled; ve>
         Active: active (running) since Thu 2021-07-22 00:43:37 UTC; 8s ago
       Main PID: 17222 (bash)
         CGroup: /user.slice/user-1000.slice/user@1000.service/bluesky_qserver_re_manager.service
                 ├─17222 /usr/bin/bash /home/vagrant/bluesky_qserver_re_manager.sh
                 ├─17232 /home/vagrant/miniconda3/envs/bluesky_queueserver/bin/python /home/vagrant/minicond>
                 └─17238 /home/vagrant/miniconda3/envs/bluesky_queueserver/bin/python /home/vagrant/minicond>

    Jul 22 00:43:37 vagrant systemd[17163]: Started Bluesky Queueserver RunEngine Manager.
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Starting ZMQ server at 'tc
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:ZMQ control channels: encr
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Starting RE Manager proces
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Loading the lists of allow
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Starting ZeroMQ server ..
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:ZeroMQ server is waiting o

    vagrant@vagrant:~$ systemctl --user start bluesky_qserver_uvicorn.service
    vagrant@vagrant:~$ systemctl --user status bluesky_qserver_uvicorn.service
    ● bluesky_qserver_uvicorn.service - Bluesky Queueserver Uvicorn
         Loaded: loaded (/home/vagrant/.config/systemd/user/bluesky_qserver_uvicorn.service; disabled; vendo>
         Active: active (running) since Thu 2021-07-22 00:43:57 UTC; 7s ago
       Main PID: 17252 (bash)
         CGroup: /user.slice/user-1000.slice/user@1000.service/bluesky_qserver_uvicorn.service
                 ├─17252 /usr/bin/bash /home/vagrant/bluesky_qserver_uvicorn.sh
                 └─17260 /home/vagrant/miniconda3/envs/bluesky_queueserver/bin/python /home/vagrant/minicond>

    Jul 22 00:43:57 vagrant bash[17260]: INFO:uvicorn.error:Started server process [17260]
    Jul 22 00:43:57 vagrant bash[17260]: INFO:     Waiting for application startup.
    Jul 22 00:43:57 vagrant bash[17260]: INFO:uvicorn.error:Waiting for application startup.
    Jul 22 00:43:57 vagrant bash[17260]: INFO:bluesky_queueserver.manager.comms:Connected to ZeroMQ server '>
    Jul 22 00:43:57 vagrant bash[17260]: INFO:bluesky_queueserver.manager.comms:ZMQ encryption: disabled
    Jul 22 00:43:57 vagrant bash[17260]: INFO:bluesky_queueserver.server.server:Bluesky HTTP Server started >
    Jul 22 00:43:57 vagrant bash[17260]: INFO:     Application startup complete.
    Jul 22 00:43:57 vagrant bash[17260]: INFO:uvicorn.error:Application startup complete.
    Jul 22 00:43:57 vagrant bash[17260]: INFO:     Uvicorn running on http://0.0.0.0:60610 (Press CTRL+C to >
    Jul 22 00:43:57 vagrant bash[17260]: INFO:uvicorn.error:Uvicorn running on http://0.0.0.0:60610 (Press C>

    vagrant@vagrant:~$ systemctl --user start tiled.service
    vagrant@vagrant:~$ systemctl --user status tiled.service
    ● tiled.service - Tiled
         Loaded: loaded (/home/vagrant/.config/systemd/user/tiled.service; disabled; vendor preset: enabled)
         Active: active (running) since Thu 2021-07-22 00:44:16 UTC; 4s ago
       Main PID: 17269 (bash)
         CGroup: /user.slice/user-1000.slice/user@1000.service/tiled.service
                 ├─17269 /usr/bin/bash /home/vagrant/tiled.sh
                 └─17277 /home/vagrant/miniconda3/envs/bluesky_queueserver/bin/python /home/vagrant/minicond>

    Jul 22 00:44:16 vagrant systemd[17163]: Started Tiled.
    Jul 22 00:44:17 vagrant bash[17277]:     Tiled server is running in "public" mode, permitting open, anon>
    Jul 22 00:44:17 vagrant bash[17277]:     Any data that is not specifically controlled with an access pol>
    Jul 22 00:44:17 vagrant bash[17277]:     will be visible to anyone who can connect to this server.
    Jul 22 00:44:17 vagrant bash[17277]: INFO:     Started server process [17277]
    Jul 22 00:44:17 vagrant bash[17277]: INFO:     Waiting for application startup.
    Jul 22 00:44:17 vagrant bash[17277]: INFO:     Application startup complete.
    Jul 22 00:44:17 vagrant bash[17277]: INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to q>


Run the Demonstration Plan
--------------------------

In the same terminal follow the qserver's output::

    vagrant@vagrant:~$ journalctl --user -af -u bluesky_qserver_re_manager
    -- Logs begin at Thu 2021-07-22 00:38:58 UTC. --
    Jul 22 00:43:37 vagrant systemd[17163]: Started Bluesky Queueserver RunEngine Manager.
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Starting ZMQ server at 'tcp://*:60615'
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:ZMQ control channels: encryption disabled
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Starting RE Manager process
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Loading the lists of allowed plans and devices ...
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Starting ZeroMQ server ...
    Jul 22 00:43:38 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:ZeroMQ server is waiting on tcp://*:60615

Open a new terminal and SSH to the VM. Open an environment, add the plan to the queue, and process the queue::

    $ vagrant ssh
    ...
    vagrant@vagrant:~$ conda activate bluesky_queueserver
    (bluesky_queueserver) vagrant@vagrant:~$ qserver environment open
    Arguments: ['environment', 'open']
    00:57:40 - MESSAGE: {'msg': '', 'success': True}
    (bluesky_queueserver) vagrant@vagrant:~$ qserver queue add plan '{"name":"the_plan", "args":[-70.0, 92.0]}'
    Arguments: ['queue', 'add', 'plan', '{"name":"the_plan", "args":[-70.0, 92.0]}']
    00:58:58 - MESSAGE: {'item': {'args': [-70.0, 92.0],
              'item_type': 'plan',
              'item_uid': 'a484d720-0848-48fa-a6d9-f7460a98b387',
              'name': 'the_plan',
              'user': 'qserver-cli',
              'user_group': 'admin'},
     'msg': '',
     'qsize': 1,
     'success': True}
    (bluesky_queueserver) vagrant@vagrant:~$ qserver queue start
    Arguments: ['queue', 'start']
    00:59:18 - MESSAGE: {'msg': '', 'success': True}

The first terminal will show the results of the plan execution::

    vagrant@vagrant:~$ journalctl --user -af -u bluesky_qserver_re_manager
    ...
    Jul 22 00:57:40 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Opening the new RE environment ...
    Jul 22 00:57:40 vagrant bash[17232]: INFO:bluesky_queueserver.manager.start_manager:Starting RE Worker ...
    Jul 22 00:57:40 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Waiting for RE worker to start ...
    Jul 22 00:57:41 vagrant bash[17232]: INFO:bluesky_queueserver.manager.profile_ops:Loading RE Worker startup code from directory '/vagrant/bmm_nist_ml_startup' ...
    Jul 22 00:57:41 vagrant bash[17232]: INFO:bluesky_queueserver.manager.profile_ops:Startup directory: '/vagrant/bmm_nist_ml_startup'
    Jul 22 00:57:41 vagrant bash[17232]: INFO:bluesky_queueserver.manager.profile_ops:Loading startup file '/vagrant/bmm_nist_ml_startup/00-base.py' ...
    Jul 22 00:57:41 vagrant bash[17232]: INFO:bluesky_queueserver.manager.worker:Startup code loading was completed
    Jul 22 00:57:41 vagrant bash[17232]: INFO:bluesky_queueserver.manager.worker:Loading the lists of allowed plans and devices ...
    Jul 22 00:57:41 vagrant bash[17232]: INFO:bluesky_queueserver.manager.worker:Instantiating and configuring Run Engine ...
    Jul 22 00:57:41 vagrant bash[17232]: INFO:bluesky_queueserver.manager.worker:RE Environment is ready
    Jul 22 00:57:42 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Worker started successfully.
    Jul 22 00:58:58 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Adding new item to the queue ...
    Jul 22 00:58:58 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Item added: success=True item_type='plan' name='the_plan' item_uid='a484d720-0848-48fa-a6d9-f7460a98b387' qsize=1.
    Jul 22 00:59:18 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Starting queue processing ...
    Jul 22 00:59:18 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Processing the next queue item: 1 plans are left in the queue.
    Jul 22 00:59:18 vagrant bash[17232]: INFO:bluesky_queueserver.manager.manager:Starting the plan:
    Jul 22 00:59:18 vagrant bash[17232]: {'args': [-70.0, 92.0],
    Jul 22 00:59:18 vagrant bash[17232]:  'item_uid': 'a484d720-0848-48fa-a6d9-f7460a98b387',
    Jul 22 00:59:18 vagrant bash[17232]:  'kwargs': {},
    Jul 22 00:59:18 vagrant bash[17232]:  'meta': {},
    Jul 22 00:59:18 vagrant bash[17232]:  'name': 'the_plan',
    Jul 22 00:59:18 vagrant bash[17232]:  'user': 'qserver-cli',
    Jul 22 00:59:18 vagrant bash[17232]:  'user_group': 'admin'}.
    Jul 22 00:59:18 vagrant bash[17232]: INFO:bluesky_queueserver.manager.worker:Starting execution of a plan ...
    Jul 22 00:59:18 vagrant bash[17232]: INFO:bluesky_queueserver.manager.worker:Starting a plan 'the_plan'.
    Jul 22 00:59:19 vagrant bash[17232]: loaded 421 scans from /vagrant/data/xafs_scans.json
    Jul 22 00:59:19 vagrant bash[17232]: nearest distance to 0,0 is 61.4121701865929
    Jul 22 00:59:19 vagrant bash[17232]: scan_info for nearest point is {'x': -33.300155, 'y': 51.599945, 'element': 'Nb', 'edge': 'K', 'sample': 'NbTiTaV_wisc_V3 (1803016-k2-2 lib2)', 'filename': 'Nb_NbTiTaV_wisc_V3_063_044.001', 'uuid': '85dec0d6-9f69-4866-a298-a1af784fa1ff'}
    Jul 22 00:59:19 vagrant bash[17232]: INFO:bluesky_queueserver.manager.plan_monitoring:New run was open: 'f0dfce85-5e94-46cf-a783-b4e34d95b89c'
    Jul 22 00:59:19 vagrant bash[17232]: nearest distance to -70.0,92.0 is 0.7072029530569732
    Jul 22 00:59:19 vagrant bash[17232]: scan_info for nearest point is {'x': -69.2998925, 'y': 92.0999275, 'element': 'Ta', 'edge': 'K', 'sample': 'NbTiTaV_wisc_V3 (1803016-k2-2 lib2)', 'filename': 'Ta_NbTiTaV_wisc_V3_018_014.001', 'uuid': 'a8688680-2de5-4c77-85a3-6a9431613643'}
    Jul 22 00:59:19 vagrant bash[17232]: Run was closed: 'f0dfce85-5e94-46cf-a783-b4e34d95b89c'


