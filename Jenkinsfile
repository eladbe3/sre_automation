pipeline {
  agent any
  environment {
    SERVER_CREDENTIALS = credentials('aws-account')
  }
  stages("test") {
    steps {
      echo "deploying with ${SERVER_CREDENTIALS}"
    }
  }
}
