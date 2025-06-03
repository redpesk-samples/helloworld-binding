#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Check the number of arguments
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <FACTORY_NAME> <FACTORY_TOKEN> <FACTORY_PROJECT> <FACTORY_URL>"
    exit 1
fi

# Assign arguments to variables
RP_REMOTE_FACTORY_NAME=$1
RP_REMOTE_FACTORY_TOKEN=$2
RP_REMOTE_FACTORY_URL=$3
RP_REMOTE_FACTORY_PROJECT=$4
CI_MERGE_REQUEST_SOURCE_BRANCH_NAME=$5

# Install rp-cli
dnf install -y https://download.redpesk.bzh/redpesk-ci/armel-update/tools/AlmaLinux_9/x86_64/redpesk-cli-3.20.1-60.8.x86_64.rpm

# Install iotbzh-internal-ca package
dnf install -y http://obs.lorient.iot:82/iotbzh:/infra-common:/master/AlmaLinux_9/noarch/iotbzh-internal-ca-1.1-16.7.noarch.rpm

# Update the system's trusted CA certificates
update-ca-trust

# Add the remote factory connection using the provided token and URL
rp-cli connections add "${RP_REMOTE_FACTORY_NAME}" -t "${RP_REMOTE_FACTORY_TOKEN}" -u "${RP_REMOTE_FACTORY_URL}"

# Set the specified factory connection as the active one
rp-cli connections use "${RP_REMOTE_FACTORY_NAME}"

rp-cli applications update helloworld-binding --project "${RP_REMOTE_FACTORY_PROJECT}" --source-rev "${CI_MERGE_REQUEST_SOURCE_BRANCH_NAME}"

rp-cli applications build helloworld-binding --project "${RP_REMOTE_FACTORY_PROJECT}"
