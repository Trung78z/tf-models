sudo apt update
sudo apt install -y build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev



sudo apt install gcc-12 g++-12
sudo apt install libgtk2.0-dev pkg-config
sudo apt install ffmpeg
sudo apt install libcanberra-gtk-module

cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_C_COMPILER=/usr/bin/gcc-12 \
      -D CMAKE_CXX_COMPILER=/usr/bin/g++-12 \
      -D CUDA_NVCC_FLAGS="-allow-unsupported-compiler" \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_GENERATE_PKGCONFIG=ON \
      -D OPENCV_EXTRA_MODULES_PATH=/home/trung/opencv_config/opencv/opencv_contrib/modules \
      -D WITH_CUDA=ON \
      -D CUDA_ARCH_BIN="7.5" \
      -D CUDA_ARCH_PTX="" \
      -D WITH_CUBLAS=ON \
      -D WITH_CUFFT=ON \
      -D WITH_NVCUVID=OFF \
      -D WITH_NVCUVENC=OFF \
      -D BUILD_opencv_cudacodec=OFF \
      -D ENABLE_FAST_MATH=ON \
      -D WITH_TBB=ON \
      -D WITH_GTK=ON \
      -D WITH_OPENMP=ON \
      -D WITH_FFMPEG=ON \
      -D BUILD_EXAMPLES=ON \
      -D BUILD_opencv_python3=ON \
      -D PYTHON3_EXECUTABLE=$(which python3) \
      -D BUILD_JAVA=OFF \
      -D BUILD_opencv_java=OFF \
      -D WITH_VTK=OFF \
      -D BUILD_PERF_TESTS=OFF \
      -D BUILD_TESTS=OFF \
      ..

echo "Done generate"
echo "Make build..."
make -j$(nproc) 
echo "Make builded!!!"

echo "Make install opencv..."
sudo make install 
echo "Installed opencv done!!!"


echo 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH' >> ~/.bashrc
source ~/.bashrc