pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Validate') {
            steps {
                echo 'Validating project files...'
                sh 'ls -la'
            }
        }

        stage('Build') {
            steps {
                echo 'Build stage completed successfully.'
            }
        }
    }
}