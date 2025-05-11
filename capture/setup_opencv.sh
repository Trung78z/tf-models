sudo apt update
sudo apt install gcc-12 g++-12
sudo apt install libgtk2.0-dev pkg-config
sudo apt install ffmpeg
sudo apt install libcanberra-gtk-module libcanberra-gtk3-module
cd build

cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules -DWITH_CUDA=ON -DCUDA_ARCH_BIN="7.5" -DWITH_NVCUVID=OFF -DWITH_NVCUVENC=OFF -DWITH_OPENGL=ON ../opencv

echo "Done generate"
echo "Make build..."
make -j$(nproc) 
echo "Make builded!!!"

echo "Make install opencv..."
sudo make install 
echo "Installed opencv done!!!"


echo 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH' >> ~/.bashrc
source ~/.bashrc