```
    python partition_dataset.py -x -i z_datasets_test/images -o z_datasets_test -r 0.1
    python generate_label_map.py

    python generate_tfrecord.py -x z_datasets_test/train -l z_datasets_test/annotations/label_map.pbtxt -o z_datasets_test/annotations/train.record
    python generate_tfrecord.py -x z_datasets_test/test -l z_datasets_test/annotations/label_map.pbtxt -o z_datasets_test/annotations/test.record

    python model_main_tf2.py --model_dir=z_datasets_test/ssd320 --pipeline_config_path=z_datasets_test/pipeline.config

    tensorboard --logdir=training/ssd320 

```
apt-get update && apt-get install -y libgl1

export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/slim
echo $PYTHONPATH
# wget http://download.tensorflow.org/models/object_detection/tf2/20200711/faster_rcnn_resnet101_v1_640x640_coco17_tpu-8.tar.gz

