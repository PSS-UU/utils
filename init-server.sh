#!/bin/sh
set -x

SERVER="$1.platform-spanning.systems"
USERNAME=$2
SSH_KEY=$3

echo Setting up ${SERVER} for ${USERNAME}

ssh ${SERVER} "sudo adduser ${USERNAME}"
ssh ${SERVER} "sudo usermod -aG sudo ${USERNAME}"

cat ${SSH_KEY} | \
  ssh ${SERVER} \
  "sudo su - ${USERNAME} -c 'mkdir -p ~/.ssh && tee -a ~/.ssh/authorized_keys'"

ssh ${SERVER} "sudo passwd --expire ${USERNAME}" 

echo "Set up account for ${USERNAME}@${SERVER}"
