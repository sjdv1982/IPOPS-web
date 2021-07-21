rm -rf attract-test
mkdir attract-test
cp attract-script/attract.sh attract-test
cp examples/1AVXA.pdb attract-test/receptor.pdb
cp ligands/7CEIB.pdb attract-test/ligand.pdb
cd attract-test

docker run --rm \
  --shm-size=8gb \
  -v `pwd`:/cwd \
  --workdir /cwd \
  -u `id -u`:`id -g` \
  --gpus all \
  rpbs/attract ./attract.sh