import tensorflow.compat.v2 as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from object_detection import model_lib_v2
record_summaries = True
checkpoint_every_n = 1000
pipeline_config_path = 'z_datasets_test/pipeline.config'
num_train_steps = None
eval_on_train_data = False
sample_1_of_n_eval_examples = None
sample_1_of_n_eval_on_train_examples = 5
model_dir = 'z_datasets_test/ssd320'
checkpoint_dir = None
eval_timeout = 3600
use_tpu = False
tpu_name = None
num_workers= 1


def main(unused_argv):
  tf.config.set_soft_device_placement(True)

  if checkpoint_dir:
    model_lib_v2.eval_continuously(
        pipeline_config_path=pipeline_config_path,
        model_dir=model_dir,
        train_steps=num_train_steps,
        sample_1_of_n_eval_examples=sample_1_of_n_eval_examples,
        sample_1_of_n_eval_on_train_examples=(
            sample_1_of_n_eval_on_train_examples),
        checkpoint_dir=checkpoint_dir,
        wait_interval=300, timeout=eval_timeout)
  else:
    if use_tpu:
      resolver = tf.distribute.cluster_resolver.TPUClusterResolver(
          tpu_name)
      tf.config.experimental_connect_to_cluster(resolver)
      tf.tpu.experimental.initialize_tpu_system(resolver)
      strategy = tf.distribute.experimental.TPUStrategy(resolver)
    elif num_workers > 1:
      strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
    else:
      strategy = tf.compat.v2.distribute.MirroredStrategy()

    with strategy.scope():
      model_lib_v2.train_loop(
          pipeline_config_path=pipeline_config_path,
          model_dir=model_dir,
          train_steps=num_train_steps,
          use_tpu=use_tpu,
          checkpoint_every_n=checkpoint_every_n,
          record_summaries=record_summaries)

if __name__ == '__main__':
  tf.compat.v1.app.run()
