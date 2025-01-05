pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        IMAGE_NAME = 'talevi83/flask-scores'
        IMAGE_TAG = 'latest'
    }

    options {
        // This will help ensure cleanup even if the pipeline fails
        skipDefaultCheckout(false)
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Run') {
            steps {
                script {
                    sh '''
                        # Debug: Check file existence and permissions
                        ls -la "${WORKSPACE}/Scores.txt"
                        ls -la "${WORKSPACE}/tests/e2e.py"

                        # Cleanup any existing container
                        docker stop test-container || true
                        docker rm test-container || true

                        # Run container with additional logging
                        docker run -d \
                            -p 8777:8777 \
                            --name test-container \
                            ${IMAGE_NAME}:${IMAGE_TAG}

                        # Wait a moment for container to start
                        sleep 5

                        # Check container status and logs
                        docker ps -a | grep test-container
                        echo "Container logs:"
                        docker logs test-container

                        # If container is running, proceed with file copies
                        if docker ps | grep -q test-container; then
                            # Copy files into container
                            docker cp "${WORKSPACE}/Scores.txt" test-container:/app/Scores.txt
                            docker cp "${WORKSPACE}/tests/e2e.py" test-container:/app/e2e.py
                            docker cp "${WORKSPACE}/requirements.txt" test-container:/app/requirements.txt

                            # Verify files are copied
                            docker exec test-container ls -la /app/Scores.txt
                            docker exec test-container ls -la /app/e2e.py
                            docker exec test-container ls -la /app/requirements.txt

                            # Wait for app to be fully ready
                            echo "Waiting for application to start..."
                            sleep 10

                            # Test if app is responding
                            curl -v http://localhost:8777/
                        else
                            echo "Container failed to start properly"
                            docker logs test-container
                            exit 1
                        fi
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    try {
                        sh 'docker exec test-container python3 /app/e2e.py'
                    } catch (Exception e) {
                        error "Tests failed: ${e.message}"
                    }
                }
            }
        }

        stage('Finalize') {
            steps {
                script {
                    // Stop and remove test container
                    sh 'docker stop test-container || true'
                    sh 'docker rm test-container || true'

                    // Login to DockerHub
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        // Push image
                        sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh '''
                        docker stop test-container || true
                        docker rm test-container || true
                        docker logout || true
                    '''
                }
            }
        }
    }
}