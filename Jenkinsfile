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

                # Run container with explicit port mapping
                docker run -d \
                    -p 8777:8777 \
                    --name test-container \
                    ${IMAGE_NAME}:${IMAGE_TAG}

                # Wait for container to initialize
                echo "Waiting for container to initialize..."
                sleep 5

                # Check container status
                if ! docker ps | grep -q test-container; then
                    echo "Container failed to start properly"
                    docker logs test-container
                    exit 1
                fi

                # Copy files into container
                docker cp "${WORKSPACE}/Scores.txt" test-container:/app/Scores.txt
                docker cp "${WORKSPACE}/tests/e2e.py" test-container:/app/e2e.py
                docker cp "${WORKSPACE}/requirements.txt" test-container:/app/requirements.txt

                # Verify files are copied
                docker exec test-container ls -la /app/Scores.txt
                docker exec test-container ls -la /app/e2e.py
                docker exec test-container ls -la /app/requirements.txt

                # Test health endpoint from inside container
                echo "Testing health endpoint from inside container..."
                if ! docker exec test-container curl -f http://localhost:8777/health; then
                    echo "Health check failed inside container"
                    exit 1
                fi

                # Wait a bit more for the app to be fully ready
                sleep 2

                # Test health endpoint from host
                echo "Testing health endpoint from host..."
                MAX_RETRIES=3
                RETRY_COUNT=0

                while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
                    if curl -f http://localhost:8777/health; then
                        echo "Health check passed from host"

                        # Now test the main endpoint
                        echo "Testing main endpoint..."
                        curl -v http://localhost:8777/
                        exit 0
                    fi

                    RETRY_COUNT=$((RETRY_COUNT + 1))
                    echo "Health check attempt $RETRY_COUNT failed, retrying..."
                    sleep 2
                done

                echo "Health check failed after $MAX_RETRIES attempts"
                docker logs test-container
                exit 1
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