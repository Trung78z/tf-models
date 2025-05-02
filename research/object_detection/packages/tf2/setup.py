"""Setup script for object_detection with TF2.0."""
import os
from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    'avro-python3',                    # For reading AVRO file formats
    'apache-beam',                    # Required for TFRecord creation with Beam pipelines
    'pillow',                         # Image handling (PIL)
    'lxml',                           # For parsing XML annotations (e.g., Pascal VOC)
    'matplotlib',                     # Plotting and visualizations
    'Cython',                         # Used to compile pycocotools
    'contextlib2',                    # Compatibility layer for contextlib
    'tf-slim',                        # Lightweight TF model definition library
    'six',                            # Python 2 and 3 compatibility
    'pycocotools',                    # COCO evaluation tools
    'lvis',                           # LVIS dataset evaluation support
    'scipy',                          # Scientific computations, used in data pipelines
    'pandas',                         # Data handling and manipulation
    'tensorflow==2.14.0',             # Main deep learning framework (version 2.14)
    'tensorflow_io==0.34.0',          # TF IO extensions, 0.34.0 compatible with TF 2.14
    'keras==2.14.0',                  # Keras library version matching TF 2.14
    'pyparsing==2.4.7',               # Prevents parsing issues in older matplotlib versions
    'sacrebleu<=2.2.0',               # BLEU score evaluation (used in NLP models)
    'tf-models-official>=2.14.0,<2.15.0'  # Official TF model implementations, match TF version
]


# REQUIRED_PACKAGES = [
#     # Required for apache-beam with PY3
#     'avro-python3',
#     'apache-beam',
#     'pillow',
#     'lxml',
#     'matplotlib',
#     'Cython',
#     'contextlib2',
#     'tf-slim',
#     'six',
#     'pycocotools',
#     'lvis',
#     'scipy',
#     'pandas',
#     'tf-models-official >2.10.0, <2.16.0',
#     'tensorflow_io',
#     'keras',
#     'pyparsing==2.4.7',  # TODO(b/204103388)
#     'sacrebleu<=2.2.0'  # https://github.com/mjpost/sacrebleu/issues/209
# ]

setup(
    name='object_detection',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    packages=(
        [p for p in find_packages() if p.startswith('object_detection')] +
        find_packages(where=os.path.join('.', 'slim'))),
    package_dir={
        'datasets': os.path.join('slim', 'datasets'),
        'nets': os.path.join('slim', 'nets'),
        'preprocessing': os.path.join('slim', 'preprocessing'),
        'deployment': os.path.join('slim', 'deployment'),
        'scripts': os.path.join('slim', 'scripts'),
    },
    description='Tensorflow Object Detection Library',
    python_requires='>3.6',
)
