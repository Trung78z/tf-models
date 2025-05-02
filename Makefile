install:
	if ! command -v protoc &> /dev/null || [ "$(protoc --version)" != "libprotoc 3.19.6" ]; then
		apt-get install -y wget unzip
		wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.6/protoc-3.19.6-linux-x86_64.zip
		unzip protoc-3.19.6-linux-x86_64.zip -d $HOME/protoc
		mv $HOME/protoc/bin/protoc /usr/local/bin/protoc
		echo "install successfully protoc 3.19.6"
		rm -r protoc-3.19.6-linux-x86_64.zip
	else
		echo "protoc 3.19.6 installed, skip"
	fi