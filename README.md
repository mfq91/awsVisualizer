# awsVisualizer
This is a python script that allows to make queries to an aws account

Usage:

docker pull mauro1991/aws-visualizer:v0.1

Volumes creation:

docker volume create visualizer # Put the script inside of this volume (/var/lib/docker/volumes/visualizer/_data/)

docker volume create [account-name]-config # Put credentials of the aws account here 

Launch the container:

docker run -td --name [Name] -v [account-name]-config:/root/.aws -v visualizer:/home mauro1991/aws-visualizer:v0.1

Execute the script:

docker exec mfq-container python /home/visualizer.py [options]
