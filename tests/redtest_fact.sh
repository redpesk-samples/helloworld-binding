#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

RP_REMOTE_FACTORY_PROJECT=$1

# Run the redtest for the hello-world-binding application
rp-cli applications test helloworld-binding --project "$RP_REMOTE_FACTORY_PROJECT"
