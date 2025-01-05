pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        IMAGE_NAME = 'talevi83/flask-scores'
        IMAGE_TAG = 'latest'
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
                    // Add error handling for docker build
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    sh '''
                        # Cleanup any existing container first
                        docker stop test-container || true
                        docker rm test-container || true
                        
                        docker run -d \
                            -p 8777:8777 \
                            -v ${WORKSPACE}/Scores.txt:/app/Scores.txt \
                            --name test-container \
                            ${IMAGE_NAME}:${IMAGE_TAG}
                        # Wait for container to be ready
                        sleep 10
                        # Verify container is running
                        docker ps | grep test-container || (echo "Container failed to start" && exit 1)
                    '''
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    try {
                        sh 'python3 e2e.py'
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
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        // Push image
                        sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
            post {
                always {
                    sh 'docker logout'
                }
            }
        }
    }
    post {
        failure {
            script {
                // Cleanup on failure
                sh 'docker stop test-container || true'
                sh 'docker rm test-container || true'
            }
        }
    }
}