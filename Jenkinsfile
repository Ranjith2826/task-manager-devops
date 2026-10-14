
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'task-manager'
        IMAGE_TAG = 'ci'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/workspace" \
                      -w /workspace \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt && pytest -v"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t task-manager:ci .'
            }
        }
    }
}
