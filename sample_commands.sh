#!/bin/bash

#Best-effort install script prerequisites, otherwise they will need to be installed manually.
if [[ -f /usr/bin/apt-get && ! -f /usr/bin/jq ]]
then
  sudo apt-get update
  sudo apt-get install -y jq
fi

# HOST="http://localhost:5000"
HOST="https://flask-bank.herokuapp.com"

TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzE4MjM2NzcsImlhdCI6MTU3MTM5MTY3NywibmJmIjoxNTcxMzkxNjc3LCJpZGVudGl0eSI6MX0.PnOHeWPvHBCPiNQzYtkfA9v2lGdXPPRpxAUMHIyyXQ0"

echo "Do you wish to refresh the JWT or use an existing one? (Yes/No)"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) printf "\nUsing the authenticate api for access token\n";
              TOKEN=$(curl -s ${HOST}/authenticate -XPOST \
                      -H "Content-type: application/json" \
                      -d '{"username":"default", "password":"iaMAStronGP@$$w0rd"}' | jq -r '.access_token');
              printf "Got token ${TOKEN}";break;;
        No ) break;;
    esac
done


printf "\nUsing access token ${TOKEN}\n"

IFSC="HDFC0000001"
printf "\nTrying bank details for IFSC ${IFSC}\n"
curl -H "Authorization: jwt ${TOKEN}" ${HOST}/bank_details?ifsc_code=${IFSC}

BANK="HDFC Bank"
CITY="Mumbai"

printf "\nTrying branch details for ${BANK} in ${CITY}\n"
curl -H "Authorization: jwt ${TOKEN}" -G \
    ${HOST}/branch_details?limit=10 --data-urlencode "bank_name=${BANK}" --data-urlencode "city=${CITY}" 
