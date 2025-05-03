import tensorflow as tf
print(tf.sysconfig.get_build_info()['cuda_version'])
print(tf.sysconfig.get_build_info()['cudnn_version'])
print("TensorFlow version:", tf.__version__)
gpus = tf.config.list_physical_devices('GPU')
print("GPUs:", gpus)

if gpus:
    print("✅ TensorFlow is using GPU.")
else:
    print("❌ TensorFlow is NOT using GPU.")
