# HoloRepository 2023 - Monai neural network container<a href="https://dev.azure.com/Holo-Repository/OrganSegmentation/_build/results?buildId=75&view=results"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloStorageAccessor" alt="HoloStorageAccessor build status" align="right" /></a>
This repository is for the HoloRepository 2023 project, an update from the 2019 version. The project is deployed as a webapp on Azure. The webapp is a Flask app that uses a Docker container to run a [Monai Zoo](https://monai.io/model-zoo.html) model. The model is a neural network that segments abdominal CT scans. The webapp will process the inputs from the pipeline webapp and send the result back to the pipeline webapp.

Main changes from the 2019 version:
- The model is now a Monai Zoo model instead of a NiftyNet model, the docker file and model.py is updated to reflect this change, with new files for the model added
- The webapp is now deployed on Azure individually instead of being deployed as a part of the pipeline

## Build Docker image from the Docker file

```
# example
docker build -t monai .
```

This instruction will create the monai docker image with the flask server endpoint. to run the image you create you need to run the other command


## Run docker and connect docker to the port 5000 
```
# example
docker run --rm -d -p 5000:5000 --name="monai" monai
```


This instruction will link your local port 5000 with the port 5000 in the container and the container has been set to run the server when you run the docker image

### API
The container runs on the ```http://localhost:5000```
To send a request for the segmentation, We provide a ```/model``` endpoint to do the segmentation.

Here are the requirements for the segmentation request:
* request must be sent to this address ```http://localhost:5000/model```
* request must be a post-request
* request should contain the nifiti file for segmentation
* The format for the nifiti file should end with .nii format


### Testing for the flask script
To run the test, you need to make sure that your docker container is running and you can run this command, however, this test is left by the original developer using resources that are no longer available, so some tests will result in failure unless updated

```
docker exec monai python3 test.py
```
