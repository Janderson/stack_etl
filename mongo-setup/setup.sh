#!/bin/bash

MONGODB1=mongodb

echo "${MONGODB1}"

curl http://${MONGODB1}:27017/serverStatus?text\=1

until curl http://${MONGODB1}:27017/serverStatus?text\=1 2>&1 | grep uptime | head -1; do
    printf "."
    sleep 1
done

echo SETUP.sh time now: `date +"%T"`
mongo --host ${MONGODB1}:27017 <<EOF
var cfg = {
    "_id": "rs0",
    "members": [
        {
            _id: 0,
            host: "${MONGODB1}:27017"
        }
    ]
};
rs.initiate(cfg);
EOF