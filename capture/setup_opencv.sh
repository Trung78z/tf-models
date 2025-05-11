sudo apt update
sudo apt install gcc-12 g++-12
sudo apt install libgtk2.0-dev pkg-config
sudo apt install ffmpeg
sudo apt install libcanberra-gtk-module libcanberra-gtk3-module
sudo apt install libavcodec-dev libavformat-dev libavutil-dev libswscale-dev
# sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

mkdir -p build
cd build

cmake \
  -D CMAKE_BUILD_TYPE=Release \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules \
  -D OPENCV_GENERATE_PKGCONFIG=ON \
  -D WITH_FFMPEG=ON \
  -D WITH_GSTREAMER=OFF \
  -D WITH_CUDA=ON \
  -D CUDA_ARCH_BIN="7.5" \
  -D WITH_NVCUVID=OFF \
  -D WITH_NVCUVENC=OFF \
  -D WITH_OPENGL=ON \
  -D WITH_V4L=ON \
  -D WITH_QT=OFF \
  -D BUILD_opencv_python3=OFF \
  -D BUILD_opencv_java=OFF \
  -D BUILD_EXAMPLES=OFF \
  ../opencv
echo "Done generate"
echo "Make build..."
make -j$(nproc) 
echo "Make builded!!!"

echo "Make install opencv..."
sudo make install 
echo "Installed opencv done!!!"


echo 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH' >> ~/.bashrc
source ~/.bashrc