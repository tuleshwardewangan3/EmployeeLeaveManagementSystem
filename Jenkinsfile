pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checked out from GitHub.'
            }
        }

        stage('Validate') {
            steps {
                echo 'Validating required project files...'

                sh '''
                    test -f backend/app.py
                    test -f backend/Dockerfile
                    test -f backend/requirements.txt
                    test -f docker-compose.yml
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Flask backend Docker image...'

                sh '''
                    docker build \
                    -t employee-leave-backend:${BUILD_NUMBER} \
                    ./backend
                '''
            }
        }

        stage('Verify Image') {
            steps {
                echo 'Verifying Docker image...'

                sh '''
                    docker images \
                    employee-leave-backend:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully.'
        }

        failure {
            echo 'CI pipeline failed. Check the console logs.'
        }
    }
}