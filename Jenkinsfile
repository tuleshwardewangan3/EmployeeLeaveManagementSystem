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
                    test -f backend/init.sql
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
                    docker images employee-leave-backend:${BUILD_NUMBER}
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying exact Docker Image built by Jenkins..'

                withCredentials([
                    string(
                        credentialsId: 'employee-leave-db-password',
                        variable: 'DB_PASSWORD'
                    )
                ]) {

                    withEnv([
                        'DB_USER=root',
                        'DB_NAME=employee_leave_db'
                        "IMAGE_TAG=${BUILD_NUMBER}"
                    ]) {

                        sh '''
                            docker compose down || true
                            docker compose up -d
                        '''
                    }
                }
            }
        }

        stage('Initialize Database') {
                steps {
                    echo 'Creating database tables and initial data...'

                    sh '''
                        docker exec -i employee-leave-mysql \
                        sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" employee_leave_db' \
                        < backend/init.sql
                    '''
                }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Checking deployed containers...'

                sh '''
                    docker ps --filter "name=employee-leave"
                '''
            }
        }
    }

    post {

        success {
            echo 'CI/CD pipeline completed successfully.'
        }

        failure {
            echo 'CI/CD pipeline failed. Check the console logs.'
        }
    }
}