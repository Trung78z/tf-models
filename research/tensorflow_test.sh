echo "Starting...."


protoc object_detection/protos/*.proto --python_out=.
echo "Protoc generate successfully!"



echo "Copy file setup..."
cp object_detection/packages/tf2/setup.py .

echo "Install Library...."
pip install .
echo "Done install library!"

echo "Running test...."
python object_detection/builders/model_builder_tf2_test.py
echo "Run test successfully"