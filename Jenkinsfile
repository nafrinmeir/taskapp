pipeline {
    agent {
        node {
            label 'meirpc'
        }
    }

    parameters {
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Enter the version tag for the Docker image.')
        choice(name: 'REUSE_EXISTING', choices: ['yes', 'no'], description: 'Reuse existing image from Docker Hub?')
    }

    stages {
        stage('Checkout Code') {
            steps {
                //git branch: 'main', url: 'https://github.com/nafrinmeir/taskapp.git'
                sh '''
                git config --global http.sslVerify false
                '''
                checkout scm
            }
        }

        stage('Check Existing Images') {
            steps {
                script {
                    def frontExists = sh(script: "docker pull nafrin/python:front-${VERSION} || echo 'Not Found'", returnStatus: true) == 0
                    def backExists = sh(script: "docker pull nafrin/python:back-${VERSION} || echo 'Not Found'", returnStatus: true) == 0
                    def mongoExists = sh(script: "docker pull nafrin/python:mongo-${VERSION} || echo 'Not Found'", returnStatus: true) == 0
                    
                    env.FRONT_BUILD = (!frontExists || params.REUSE_EXISTING == 'no') ? 'yes' : 'no'
                    env.BACK_BUILD = (!backExists || params.REUSE_EXISTING == 'no') ? 'yes' : 'no'
                    env.MONGO_BUILD = (!mongoExists || params.REUSE_EXISTING == 'no') ? 'yes' : 'no'
                }
            }
        }

        stage('Build and Push Docker Images') {
            parallel {
                stage('Front Image') {
                    when {
                        expression { env.FRONT_BUILD == 'yes' }
                    }
                    steps {
                        sh """
                        docker build -t nafrin/python:front-${VERSION} -f Dockerfile.front .
                        docker push nafrin/python:front-${VERSION}
                        """
                    }
                }

                stage('Back Image') {
                    when {
                        expression { env.BACK_BUILD == 'yes' }
                    }
                    steps {
                        sh """
                        docker build -t nafrin/python:back-${VERSION} -f Dockerfile.back .
                        docker push nafrin/python:back-${VERSION}
                        """
                    }
                }

                stage('MongoDB Image') {
                    when {
                        expression { env.MONGO_BUILD == 'yes' }
                    }
                    steps {
                        sh """
                        docker pull mongo:latest
                        docker tag mongo:latest nafrin/python:mongo-${VERSION}
                        docker push nafrin/python:mongo-${VERSION}
                        """
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                sed -i 's/<TAG>/${VERSION}/g' front-deployment.yaml
                sed -i 's/<TAG>/${VERSION}/g' back-deployment.yaml
                sed -i 's/<TAG>/${VERSION}/g' mongo-deployment.yaml

                kubectl apply -f front-deployment.yaml
                kubectl apply -f back-deployment.yaml
                kubectl apply -f mongo-deployment.yaml
                """
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh """
                docker run --rm nafrin/python:front-${VERSION} pytest tests/
                docker run --rm nafrin/python:back-${VERSION} pytest tests/
                kubectl exec -it \$(kubectl get pod -l app=mongo -o jsonpath='{.items[0].metadata.name}') -- mongo --eval 'db.stats()'
                """
            }
        }
    }
}
