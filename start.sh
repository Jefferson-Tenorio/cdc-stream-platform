sudo docker compose up -d
sleep 5 
sleep 10
echo "Waiting for connectors to start..."
./debezium/post.sh
gnome-terminal -- bash -c "sudo docker exec -it lab-postgres bash"

curl -s http://localhost:8083/connectors/postgres-connector/status | jq .

sleep 5

xdg-open http://localhost:8888
xdg-open http://localhost:5050