#!/bin/bash

# Kiểm tra protoc có sẵn và đúng phiên bản chưa
if ! command -v protoc &> /dev/null || [ "$(protoc --version)" != "libprotoc 3.19.6" ]; then
    # Cài đặt wget và unzip nếu chưa có
    apt-get install -y wget unzip
    
    # Tải và giải nén protoc phiên bản 3.19.6
    wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.6/protoc-3.19.6-linux-x86_64.zip
    
    # Giải nén và di chuyển protoc vào thư mục /usr/local/bin
    unzip protoc-3.19.6-linux-x86_64.zip -d $HOME/protoc
    mv $HOME/protoc/bin/protoc /usr/local/bin/protoc
    
    echo "install successfully protoc 3.19.6"
    
    # Xóa file zip đã tải về
    rm -r protoc-3.19.6-linux-x86_64.zip
else
    echo "protoc 3.19.6 installed, skip"
fi
