pipeline {
    agent {
        label "aws"
           }
    options {
        timestamps()
    }
//     parameters {
//         string(name: 'pram1', defaultValue: "", description: "VPC_NAME")
//         string(name: 'param2', defaultValue: "", description: "OpenVPN_Sever_Name")
//         string(name: 'param3', defaultValue: "", description: "APP_Sever_Name")
//     }
    stages {
        stage('authentication') {
            steps {
                withCredentials([string(credentialsId:"aws_access_key_id", variable: 'aws_access_key_id'), string(credentialsId: "aws_secret_access_key", variable: 'aws_secret_access_key')])
                        {
                            sh """
                            ls -ltrh
                            aws configure set aws_access_key_id $aws_access_key_id
                            aws configure set aws_secret_access_key $aws_secret_access_key
                            aws configure set region eu-west-1
                            aws ec2 describe-instances
                               """
                }
            }
        }
        stage('runpython') {
            steps {
                    sh """
                			pwd
                			ls -ltrh
                			python3 AwsScript.py
                       """
            }
        }
    }
}