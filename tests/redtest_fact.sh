#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Run the redtest for the hello-world-binding application
rp-cli applications test helloworld-binding --project hello-world-binding
