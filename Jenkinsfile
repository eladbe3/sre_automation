pipeline {
  agent any
  environment {
     SERVER_CREDENTIALS = credentials('aws-account')
  }

  stage('deploy') {
      steps {
          sh 'echo $SERVER_CREDENTIALS'
    }
}
