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
                        'DB_NAME=employee_leave_db',
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

        stage('Health Check') {
            steps {
                echo 'Checking application health...'

                sh '''
                    MAX_RETRIES=10
                    RETRY_COUNT=1

                    while [ $RETRY_COUNT -le $MAX_RETRIES ]
                    do
                        echo "Health check attempt $RETRY_COUNT of $MAX_RETRIES"

                        if curl -fsS http://host.docker.internal:5000/employees
                        then
                            echo "Application health check passed."
                            exit 0
                        fi

                        echo "Application not ready yet. Waiting 5 seconds..."
                        sleep 5

                        RETRY_COUNT=$((RETRY_COUNT + 1))
                    done

                    echo "Application health check failed."
                    exit 1
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