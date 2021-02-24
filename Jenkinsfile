pipeline {
  agent any
  environment {
     SERVER_CREDENTIALS = credentials('aws-account')
  }

  stage('deploy') {
      steps {
          withCredentials([[
             $class: 'AmazonWebServicesCredentialsBinding',
             credentialsId: 'aws-account',
             SERVER_CREDENTIALS: 'AWS_ACCESS_KEY_ID',
             SERVER_CREDENTIALS: 'AWS_SECRET_ACCESS_KEY'
          ]]) {
             sh 'AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=us-east-1 ${AWS_BIN} ecs update-service --cluster default --service test-deploy-svc --task-definition test-deploy:2 --desired-count 0'
             sh 'AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=us-east-1 ${AWS_BIN} ecs update-service --cluster default --service test-deploy-svc --task-definition test-deploy:2 --desired-count 1'
        }
    }
}
