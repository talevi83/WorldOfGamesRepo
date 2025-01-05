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
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Run') {
            steps {
                script {
                    // Run container using image built from our Dockerfile
                    sh '''
                        docker run -d \
                            -p 8777:8777 \
                            -v ${WORKSPACE}/Scores.txt:/app/Scores.txt \
                            --name test-container \
                            ${IMAGE_NAME}:${IMAGE_TAG}

                        # Wait for container to be ready
                        sleep 10

                        # Verify container is running
                        docker ps | grep test-container
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
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'

                    // Push image
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
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
            node{
                script {
                    // Cleanup on failure
                    sh 'docker stop test-container || true'
                    sh 'docker rm test-container || true'
                }    
            }
        }
    }
}