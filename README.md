# awsVisualizer
This is a python script that allows to make simple queries to an aws account (you can code more queries if you want. There are many possibilities)

Downloading the docker image:

docker pull mauro1991/aws-visualizer:v0.1

Creating volumes:

docker volume create visualizer # Put the script inside of this volume (/var/lib/docker/volumes/visualizer/_data/)

docker volume create [account1-name]-config # Put credentials of the aws account here 

Launching the container:

docker run -td --name container-name -v [account1-name]-config:/root/.aws -v visualizer:/home mauro1991/aws-visualizer:v0.1

Executing the script:

docker exec container-name python /home/visualizer.py [options]
