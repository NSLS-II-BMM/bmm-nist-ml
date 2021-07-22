source /home/vagrant/miniconda3/etc/profile.d/conda.sh
conda activate bluesky_queueserver
uvicorn bluesky_queueserver.server.server:app --host 0.0.0.0 --port 60610
