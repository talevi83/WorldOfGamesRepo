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

                       # Cleanup any existing container
                       docker stop test-container || true
                       docker rm test-container || true

                       # First run the container without the volume
                       docker run -d \
                           -p 8777:8777 \
                           --name test-container \
                           ${IMAGE_NAME}:${IMAGE_TAG}

                       # Then copy the file into the container
                       docker cp "${WORKSPACE}/Scores.txt" test-container:/app/Scores.txt
                       docker cp "${WORKSPACE}/tests/e2e.py" test-container:/app/e2e.py

                       # Debug: Verify file is copied
                       docker exec test-container ls -la /app/Scores.txt
                       docker exec test-container ls -la /app/e2e.py

                       # Wait for container to be ready
                       sleep 10

                       # Verify container is running and check logs
                       docker ps | grep test-container
                       docker logs test-container
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