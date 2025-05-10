echo "Starting...."


protoc object_detection/protos/*.proto --python_out=.
echo "Protoc generate successfully!"



echo "Copy file setup..."
cp object_detection/packages/tf2/setup.py .

echo "Install Library...."
pip install .
echo "Done install library!"