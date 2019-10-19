# Propeller Aero

## Prerequisites

### Mac OSX/Unix System Based
Please ensure that you have the following on your machine

* brew
* pyenv

#### System Requirements
* pip        19.0.3
* python     3.7.3
* Pillow     6.2.0

#### Suggested Installation

Please first install brew if you do not have it. You can follow the commands here:
https://brew.sh/

Then use brew to install python version manager:

$ brew install pyenv

pyenv will help with managing different versions of python on your machine.

Once this has been completed, you will be able to start using pip to manage individual python packages.

In order for the processing script to work, we require the Pillow library. Please install it via the following command:

$ pip install Pillow


## To Run

To run this script, you need run the following command:

$ python process_image.py [inputFile]

the resultant output will be placed in './output' directory under a folder named with 'inputFile' name.


## To Run UnitTests

To run unittests built for this, please run:

$ PYTHONPATH=. python test/process_image_test.py

The above command is relative to the current folder you are in. I am assuming you are running the command where this README file is.


## Improvement Considerations
* Continue to look into whether it is feasible to deploy this into Docker containers
    - Currently have basic Dockerfile, but was unable to output the files into the shared volume
    - Current commands that is semi working:

        $ docker build -t process-image-app .

        $ docker run -d -it --volume "$(pwd)/output:/output" process-image-app:latest [inputFile]

* Explore more into other libraries, perhaps PyTorch or TensorFlow