DATABASE_DIR=~/IPOPS-db
mkdir -p $DATABASE_DIR/config
cat database-config.yaml > $DATABASE_DIR/config/database-config.yaml
docker run \
  -d \
  --network=host \
  --name seamless-database-container \
  -v $DATABASE_DIR:/data \
  -u `id -u` \
  --group-add users \
  rpbs/seamless start.sh python3 -u /home/jovyan/seamless-tools/database.py /data/config/database-config.yaml