pipeline {
    agent {
        label "aws"
    }
    options {
        timestamps()
    }
    parameters {
           string(name: 'VPC_NAME', defaultValue: "", description: "VPC_Name")
           string(name: 'VPN_SRV_NAME', defaultValue: "", description: "OpenVpn_Sever_Name")
           string(name: 'APP_SRV_NAME', defaultValue: "", description: "APP_Server_Name")
    }
    stages {
        stage('authentication') {
            steps {
                withCredentials([string(credentialsId:"aws_access_key_id", variable: 'aws_access_key_id'), string(credentialsId: "aws_secret_access_key", variable: 'aws_secret_access_key')])
                        {
                            sh """
                            aws configure set aws_access_key_id $aws_access_key_id
                            aws configure set aws_secret_access_key $aws_secret_access_key
                            aws configure set region eu-west-1
                               """
                }
            }
        }
        stage('runpython') {
            steps {
                    sh """
                		    python3 AwsScript.py
                       """
            }
        }
    }
}
