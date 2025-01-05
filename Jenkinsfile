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
                docker network prune -f
                docker network create test-network

                # Debug: Check file existence and permissions
                ls -la "${WORKSPACE}/Scores.txt"
                ls -la "${WORKSPACE}/tests/e2e.py"

                # Cleanup any existing container
                docker stop test-container || true
                docker rm test-container || true

                # Run container with explicit port mapping
                docker run -d \
                    --network test-network \
                    -p 8777:8777 \
                    -v "${WORKSPACE}:/app" \
                    --name test-container \
                    ${IMAGE_NAME}:${IMAGE_TAG}

                # Wait for container to initialize
                echo "Waiting for container to initialize..."
                sleep 10

                # Check container status and logs
                docker ps
                echo "Container logs:"
                docker logs test-container

                # Test health endpoint from container
                echo "Testing from inside container..."
                docker exec test-container curl -v http://localhost:8777/health

                # Test health endpoint from host with absolute URL
                echo "Testing from host..."
                curl -v --connect-timeout 10 http://0.0.0.0:8777/health

                if [ $? -eq 0 ]; then
                    echo "Connection successful!"
                    curl -v http://0.0.0.0:8777/
                else
                    echo "Connection failed. Container status:"
                    docker ps
                    echo "Container logs:"
                    docker logs test-container
                    echo "Container network info:"
                    docker inspect test-container | grep -A 20 "NetworkSettings"
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