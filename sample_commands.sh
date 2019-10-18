#!/bin/bash

#Best-effort install script prerequisites, otherwise they will need to be installed manually.
if [[ -f /usr/bin/apt-get && ! -f /usr/bin/jq ]]
then
  sudo apt-get update
  sudo apt-get install -y jq
fi


# HOST="http://localhost:5000"
HOST="https://flask-bank.herokuapp.com"

echo "Trying the authenticate api for access token"
TOKEN=$(curl ${HOST}/authenticate -XPOST \
 -H "Content-type: application/json" \
 -d '{"username":"default", "password":"iaMAStronGP@$$w0rd"}' | jq -r '.access_token')

echo "access token" $TOKEN

echo 'Trying bank details for IFSC HDFC0000001'
curl -H "Authorization: jwt ${TOKEN}" ${HOST}/bank_details?ifsc_code=HDFC0000001

echo 'Trying branch details for State bank of india in Mumbai' 
curl -H "Authorization: jwt ${TOKEN}" \
    ${HOST}/branch_details?bank_name=State%20Bank%20of%20India\&city=MUMBAI\&limit=10\&offset=100
