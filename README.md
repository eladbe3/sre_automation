# BlueVine - AWS, Security And Automation Skills
Hello All,
Here I will describe my thought process, step by step, from the beginning to the solution.


## AWS Users Creation
**Created new IAM user on AWS Console:**

    UserName: ReadOnlyEc2User
    Password: Aa123qwe!@
	Login URL: https://073875213206.signin.aws.amazon.com/console
	Policy: AmazonEC2ReadOnlyAccess
	Tag: ReadOnlyEc2
**Created Another IAM user on AWS Console:**

    UserName: ReadOnlyUser
	Password: Bb456rty!@
	Login URL: https://073875213206.signin.aws.amazon.com/console
	Policy: ReadOnlyAccess
	Tag: ReadOnlyAccessUser

**Created new IAM ROLE on AWS Console:**
    
    Name: jenkins-master-role
    Role: AWS services- EC2
    Policies: AdministratorAccess

**Created new IAM user on AWS Console, called JenkinsUser,'Programmatic Access' accsess type**

    User: JenkinsUser
    Keys sent by mail.

## Accomplish the mission with Python Script using Boto3

My state of mind on this stage, was to verify I'm establishing AWS topology with my Python script, on my work station, then I will moving forward using Docker and Jenkins to accomplish that misssion.

In order to work only with linux OS, I've created new EC2 Ubuntu(20.04) (ami-022e8cc8f0d3c52fd), t2-medium instance type, as a work station, on my aws account.

**Dependencies**

```bash
sudo apt-get install python3-pip
pip3 install boto3
pip3 install awscli
```
With the command **awscli configure**, I've configured manually the keys and region parameters (secret & access key - credentials file, and region -config file).

**Writing some code**

Created python script with VIM editor (used "import boto3" library, to enable the functionality of working with AWS SDK)

After I've confirmed that my python script running and deploying my AWS VPC topology as i wish, its time to use Jenkins for that Automation proccess.

## Docker & Jenkins Installation

**installed Docker by following Docker official documentation - https://docs.docker.com/engine/install/ubuntu/**

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
 	         "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
                 $(lsb_release -cs) \
                 stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo mkdir /opt/jenkins
```
**Running new Jenkins container:**

```bash
cd /opt
chmod 777 jenkins/
docker run -d  --name jenkins  -p 8080:8080 -p 50000:50000 -v /opt/jenkins:/var/jenkins_home jenkins/jenkins:lts
```
I've Opened on my Workstation SecurityGroup, an inbound rule allowing port 8080.

## Automation With Jenkins

I've Connected with chrome explorer to work station public ip address port 8080

In my first login, I've to provide the Jenkins app a password, which I can find it on my WS with the command:
```bash
sudo docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Installed the suggestions plugins, and then created new admin user.

**I've decided to work with "Slave" machine, so I've created new Ubuntu machine on aws, and installed all the needed dependencies:**
```bash
sudo apt-get install python3-pip3
pip3 install boto3
pip3 install awscli
pip3 install --upgrade awscli
```

**I've created new GitHub account and a new repository called "sre_automation".**

There I've added 2 files:\
* Jenkinsfile - need to write a Declerative pipeline script.\
* AwsScript.py - Already written and tested.\

I am working with Intellij IDEA - I've sync it with my GitHub repo (push new commits etc.)

**Before I started to build the Jenkinsfile, I need to create a new Job on Jenkins that runs Jenkinsfile via my GitHub repo.**\
I've Created new pipeline Job called "deployec2".\
Configure the Job pipeline, to "script from SCM" (Source Code Managment)

--> SCM: Git
Repository URL: https://github.com/eladbe3/sre_automation.git \
Brunch: */main
Script Path: Jenkinsfile

**I've Created new Credentials for Jenkins to communicate with the Slave machine over SSH**
        
    Dashboard --> manage jenkins --> manage credentials --> global --> Add Credentials
    * Kind: SSH Username with private key
    * Scope: default
	* ID: awsslavessh
	* Description: awsslavessh
	* Username: ubuntu
	* Private Key: enter directly --> Copy from the WorkStation.pem file the text and paste here.
	* Save.

**Then I've created new Node to be the "Slave agent" that performs the pipeline on the Slave Machine.**\

    * Dashboard --> Build Executor Status --> New Node
    * Node Name: aws
    * Permanent Agent
    * Description: aws
    * Remote root directory: /home/ubuntu
    * Labels: aws
    * Launch method: Launch agents via SSH
        Host:172.31.0.62
        Add new credentials: awsslavessh
        Host Key Verification Strategy: Non verifying Verfication Srategy.

**I'm planning to use environment variables on my Declarative pipeline script, for the aws authentication stage,
for that I've created 2 new secret text credentials:**

    * Dashboard --> manage jenkins --> manage credentials --> global --> Add Credentials
    * Kind: Secret text
    * Scope: Global
    * Secret: ******AWS JenkinsUser Keys******
    * ID: aws_access_key_id / aws_secret_access_key
    * Description: aws_access_key_id / aws_secret_access_key

**I've configured the Jenkinsfile as Declarative pipeline - that runs on the Slave machine.**

    * First, we are telling to our Jenkins Master who is the "agent" that going to perform this Declerative pipeline.
    * Second, We have parameters that recieved input from the user, and saved them in 3 environment variables, that we are going to use them on our Python script.
    * Then there are 2 Stages:
        Authentication - Using the AWS Credentials (Keys) We've created before, we are configuring them on the build with environment variables.
        Run Python- Running our python script, with the parameters we've recieved from the user (Please be aware, there are 2 Phases for the Script, Phase 2 is for creating Instance Tags).

##Thank you BlueVine Team, for the learning experience.