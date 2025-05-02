#include <iostream>
#include <cuda_runtime.h>

__global__ void vectorAdd(int *a, int *b, int *c, int n) {
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    if (i < n)
        c[i] = a[i] + b[i];
}

int main() {
    const int N = 256;
    size_t size = N * sizeof(int);

    // Cấp phát bộ nhớ trên host
    int *h_a = new int[N];
    int *h_b = new int[N];
    int *h_c = new int[N];

    // Khởi tạo dữ liệu
    for (int i = 0; i < N; ++i) {
        h_a[i] = i;
        h_b[i] = 2 * i;
    }

    // Cấp phát bộ nhớ trên device
    int *d_a, *d_b, *d_c;
    cudaMalloc(&d_a, size);
    cudaMalloc(&d_b, size);
    cudaMalloc(&d_c, size);

    // Copy dữ liệu từ host sang device
    cudaMemcpy(d_a, h_a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, size, cudaMemcpyHostToDevice);

    // Gọi kernel (sử dụng nhiều block nếu cần)
    int threadsPerBlock = 128;
    int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, N);

    // Copy kết quả từ device về host
    cudaMemcpy(h_c, d_c, size, cudaMemcpyDeviceToHost);

    // In kết quả (tùy chọn)
    for (int i = 0; i < 10; ++i)
        std::cout << h_c[i] << " ";
    std::cout << std::endl;

    // Giải phóng bộ nhớ
    delete[] h_a;
    delete[] h_b;
    delete[] h_c;
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);

    return 0;
}
