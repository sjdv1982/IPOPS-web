docker run \
  -d \
  --network=host \
  --name seamless-database-container \
  -v ~/IPOPS-db:/data \
  -u `id -u` \
  --group-add users \
  rpbs/seamless start.sh python3 -u /home/jovyan/seamless-tools/database.py /data/config/database-config.yaml