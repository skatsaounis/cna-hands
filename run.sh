set -xe

unset http_proxy
unset https_proxy
unset HTTP_PROXY
unset HTTPS_PROXY

echo "Starting gorb"
docker run --name gorb --privileged --net=host -itd kobolog/gorb -f -i enp0s3 &
sleep 5s
echo "Create gorb service"
curl -i -X PUT -H "Content-Type: application/json" -d '{"host":"10.0.2.15", "port":4444, "protocol":"tcp", "method":"rr", "persistent": true}' http://10.0.2.15:4672/service/0


echo "Starting 1st server worker"
docker run -tid --name server-0 cna-server &
sleep 5s

echo "Register server to gorb"
curl -i -X PUT -H "Content-Type: application/json" -d '{"host":"172.17.0.2", "port":4444, "method":"nat", "weight":100 }' http://localhost:4672/service/0/0

sleep 5s

echo "Start client"
go run client-deterministic/main.go 10.0.2.15 > client.log 2>&1 &
sleep 3s
echo "Start orchestrator"
python orchestrator/python/main.py

