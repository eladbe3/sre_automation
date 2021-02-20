FROM jenkins/jenkins:lts
USER root
RUN apt-get update
RUN apt-get install python-boto3
USER jenkins
RUN jenkins-plugin-cli --plugins blueocean:1.24.4
