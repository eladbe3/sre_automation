pipeline {
    agent {
                    label "aws"
           }
    options {
        timestamps()
    }
//     parameters {
//         string(name: 'pram1', defaultValue: "", description: " address ")
//         string(name: 'param2', defaultValue: "", description: " name ")
//
//     }
    stages {
        stage('create bash sh   ') {

            steps {


withCredentials([string(credentialsId:"aws_access_key_id", variable: 'aws_access_key_id'), string(credentialsId: "aws_secret_access_key", variable: 'aws_secret_access_key')])
                        {

                                sh """
                     ls -ltrh
                     aws configure set aws_access_key_id $aws_access_key_id
                     aws configure set aws_secret_access_key $aws_secret_access_key
                     aws configure set aws_default_region eu-west-1
                     aws ec2 describe-instances
                    """


}


//                     sh """
// 					pwd
// 					ls -ltrh
//                 """
//
            }
        }



    }
}






//
// pipeline {
//   agent any
//   environment {
//      SERVER_CREDENTIALS = credentials('aws-account')
//   }
//
//   stage('deploy') {
//       steps {
//           withCredentials([[
//              $class: 'AmazonWebServicesCredentialsBinding',
//              credentialsId: 'aws-account',
//              SERVER_CREDENTIALS: 'AWS_ACCESS_KEY_ID',
//              SERVER_CREDENTIALS: 'AWS_SECRET_ACCESS_KEY'
//           ]]) {
//              sh 'AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=us-east-1 ${AWS_BIN} ecs update-service --cluster default --service test-deploy-svc --task-definition test-deploy:2 --desired-count 0'
//              sh 'AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=us-east-1 ${AWS_BIN} ecs update-service --cluster default --service test-deploy-svc --task-definition test-deploy:2 --desired-count 1'
//         }
//     }
// }
