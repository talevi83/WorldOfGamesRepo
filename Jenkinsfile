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
                # Create a dedicated network for the test
                docker network create test-network || true

                # Debug: Check file existence and permissions
                ls -la "${WORKSPACE}/Scores.txt"
                ls -la "${WORKSPACE}/tests/e2e.py"

                # Cleanup any existing container
                docker stop test-container || true
                docker rm test-container || true

                # Run container with explicit port mapping and network
                docker run -d \
                    --network test-network \
                    -p 0.0.0.0:8777:8777 \
                    --name test-container \
                    ${IMAGE_NAME}:${IMAGE_TAG}

                # Wait for container to initialize
                echo "Waiting for container to initialize..."
                sleep 5

                # Check container details
                echo "Container network details:"
                docker inspect test-container | grep -A 20 "NetworkSettings"

                echo "Container IP address:"
                docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test-container

                # Copy required files
                docker cp "${WORKSPACE}/Scores.txt" test-container:/app/Scores.txt
                docker cp "${WORKSPACE}/tests/e2e.py" test-container:/app/e2e.py
                docker cp "${WORKSPACE}/requirements.txt" test-container:/app/requirements.txt

                # Verify files
                echo "Verifying files in container:"
                docker exec test-container ls -la /app/

                # Test from inside container
                echo "Testing from inside container..."
                docker exec test-container curl -v http://localhost:8777/health

                # Test from host with IP
                CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test-container)
                echo "Testing from host using container IP: ${CONTAINER_IP}"
                curl -v http://${CONTAINER_IP}:8777/health

                # Test from host with localhost
                echo "Testing from host using localhost:"
                curl -v http://localhost:8777/health

                # Test main endpoint
                echo "Testing main endpoint:"
                curl -v http://localhost:8777/
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