pipeline {
  agent any
  environment {
     secret = credentials('aws-account')
  }
  stage('deploy') {
      steps {
          sh 'echo $secret'
    }
}
