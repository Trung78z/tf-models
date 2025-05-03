#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Check if protoc is installed and the correct version
if ! command -v protoc &> /dev/null || [ "$(protoc --version)" != "libprotoc 3.19.6" ]; then
    echo "Installing protoc 3.19.6..."

    # Install wget and unzip if they are not installed
    apt-get update
    apt-get install -y wget unzip

    # Download and extract protoc version 3.19.6
    wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.6/protoc-3.19.6-linux-x86_64.zip
    unzip protoc-3.19.6-linux-x86_64.zip -d $HOME/protoc

    # Move protoc binary to /usr/local/bin
    mv $HOME/protoc/bin/protoc /usr/local/bin/protoc
    chmod +x /usr/local/bin/protoc

    # Confirm installation
    echo "protoc 3.19.6 installed successfully"

    # Clean up
    rm -rf protoc-3.19.6-linux-x86_64.zip $HOME/protoc
else
    echo "protoc 3.19.6 already installed, skipping"
fi
