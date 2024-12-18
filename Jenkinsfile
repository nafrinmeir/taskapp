pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        DOCKER_IMAGE_PREFIX = 'nafrin/python'
        DOCKER_REGISTRY = 'https://index.docker.io/v1/'
        VERSION = 'v1.0.0'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/nafrinmeir/taskapp.git'
            }
        }

        stage('Build and Tag Images') {
            steps {
                script {
                    // Build images using Docker Compose
                    bat "docker-compose -f %DOCKER_COMPOSE_FILE% build --no-cache"

                    // Verify built images
                    bat "docker-compose images"

                    // Tag images with the version
                    bat """
                        FOR /F "tokens=*" %%I IN ('docker-compose config --services') DO (
                            docker tag %DOCKER_IMAGE_PREFIX%-%%I %DOCKER_IMAGE_PREFIX%-%%I:%VERSION%
                        )
                    """
                }
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                script {
                    // Log in to Docker Hub and push images
                    withDockerRegistry([credentialsId: 'docker_hub_user', url: DOCKER_REGISTRY]) {
                        bat """
                            FOR /F "tokens=*" %%I IN ('docker-compose config --services') DO (
                                docker push %DOCKER_IMAGE_PREFIX%-%%I:%VERSION%
                            )
                        """
                    }
                }
            }
        }
        
        stage('Launch Application') {
            steps {
                script {
                    // Run the Docker Compose to launch the application (frontend, backend, mongodb)
                    bat """
                        docker-compose -f %DOCKER_COMPOSE_FILE% up -d
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
