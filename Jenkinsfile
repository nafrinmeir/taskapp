pipeline {
    agent any

    parameters {
        string(name: 'VERSION', defaultValue: '2.0.0', description: 'Docker image and Kubernetes version')
    }

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        DOCKER_IMAGE_PREFIX = 'nafrin/python'
        DOCKER_REGISTRY = 'https://index.docker.io/v1/'
        KUBE_CONFIG_PATH = 'C:/Users/MyPc/.kube/config'
        SONAR_PROJECT_KEY = 'taskapp'
        SONAR_HOST_URL = 'http://localhost:9000'
        SONAR_AUTH_TOKEN = credentials('jenkinssonar')
        
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/nafrinmeir/taskapp.git'
            }
        }

//        stage('SonarQube Analysis') {
//
//            steps {
//                bat 'mvn sonar:sonar -Dsonar.projectKey=%SONAR_PROJECT_KEY% -Dsonar.host.url=%SONAR_HOST_URL% -Dsonar.login=%SONAR_AUTH_TOKEN%'
//            }
//        }
        
        
//        stage('SonarQube Analysis') {
//            steps {
//                script {
//                    if (!env.JAVA_HOME) {
//                        error "JAVA_HOME is not set. Please configure JAVA_HOME on the Jenkins agent."
//                   }
//                    withSonarQubeEnv('sonar_srv') {
//                        bat 'mvn sonar:sonar -Dsonar.projectKey=%SONAR_PROJECT_KEY% -Dsonar.host.url=%SONAR_HOST_URL% -Dsonar.login=%SONAR_AUTH_TOKEN%'
//                    }
//                }                
//            }
//        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar_srv') {
                        bat """
                        mvn sonar:sonar ^
                            -Dsonar.projectKey=%SONAR_PROJECT_KEY% ^
                            -Dsonar.host.url=%SONAR_HOST_URL% ^
                            -Dsonar.login=%SONAR_AUTH_TOKEN%
                        """
                    }
                }
            }
        }



        stage('Build Docker Images and Launch Application') {
            steps {
                script {
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

        stage('Unit Test') {
            steps {
                bat """
                echo Running unit tests
                """
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
