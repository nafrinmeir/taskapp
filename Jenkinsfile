pipeline {
    agent any
    
    //agent {
    //    node {
    //        label 'meirpc'
    //    }
    //}

    parameters {
        string(name: 'VERSION', defaultValue: '2.0.0', description: 'Docker image and Kubernetes version')
    }

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        DOCKER_IMAGE_PREFIX = 'nafrin/python'
        DOCKER_REGISTRY = 'https://index.docker.io/v1/'
        KUBE_CONFIG_PATH = 'C:/Users/MyPc/.kube/config'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/nafrinmeir/taskapp.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    //bat "docker-compose -f %DOCKER_COMPOSE_FILE% build --no-cache"
                    bat "docker-compose -f %DOCKER_COMPOSE_FILE% build"
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    withDockerRegistry([credentialsId: 'docker_hub_user', url: DOCKER_REGISTRY]) {
                        bat """
                            docker-compose config --services | for /f "delims=" %%I in ('more') do (
                                docker tag %DOCKER_IMAGE_PREFIX%-%%I %DOCKER_IMAGE_PREFIX%-%%I:%VERSION%
                                docker push %DOCKER_IMAGE_PREFIX%-%%I:%VERSION%
                            )
                        """
                    }
                }
            }
        }
        
        stage('unit test') {
            steps {
                script {
                        bat """
                        echo test
                        """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withEnv(["KUBECONFIG=${KUBE_CONFIG_PATH}"]) {
                        bat """
                            helm install chatapp ./helm
                            ping localhost -4 -n 5
                            kubectl get all
                            ping localhost -4 -n 5
                            kubectl get pods -o wide
                        """
                    }
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
