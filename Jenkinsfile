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
                # Cleanup networks
                docker network prune -f
                docker network create test-network

                # Debug: Check file existence and permissions
                ls -la "${WORKSPACE}/Scores.txt"
                ls -la "${WORKSPACE}/tests/e2e.py"

                # Cleanup any existing container
                docker stop test-container || true
                docker rm test-container || true

                # Run container with specific file mounts instead of whole workspace
                docker run -d \
                    --network test-network \
                    -p 8777:8777 \
                    --name test-container \
                    ${IMAGE_NAME}:${IMAGE_TAG}

                # Copy required files into the container
                docker cp "${WORKSPACE}/Scores.txt" test-container:/app/Scores.txt
                docker cp "${WORKSPACE}/tests/e2e.py" test-container:/app/e2e.py
                docker cp "${WORKSPACE}/tests/requirements.txt" test-container:/app/requirements.txt

                echo "Waiting for container to initialize..."
                sleep 10

                # Install test requirements
                docker exec test-container pip install -r /app/requirements.txt

                # Debug: Check container status
                docker ps
                echo "Container logs:"
                docker logs test-container

                # Test container health
                echo "Testing from inside container..."
                docker exec test-container curl -v http://localhost:8777/health
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