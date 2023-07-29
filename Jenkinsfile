def img

pipeline {
    environment {
        registry = "dvorkinguy/second-simple-flask-app"
        registryCredential = 'docker-hub-credentials'
        dockerImage = ''
    }
    agent {
        label 'jenkins_worker'
    }
    stages {
        stage('checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/dvorkinguy/second-simple-flask-app.git'
            }
        }

        stage ('Stop previous running container'){
            steps{
                sh returnStatus: true, script: 'docker stop ${JOB_NAME}'
                sh returnStatus: true, script: 'docker rmi $(docker images | grep ${registry} | awk \'{print $3}\') --force'
                sh returnStatus: true, script: 'docker rm ${JOB_NAME}'
            }
        }

        stage('Build Image') {
            steps {
                script {
                    // Tag the image with the build number
                    img = registry + ":build-${env.BUILD_NUMBER}"
                    println ("${img}")
                    dockerImage = docker.build("${img}")
                }
            }
        }

        stage('Test - Run Docker Container on Jenkins node') {
            steps {
                sh label: '', script: "docker stop second-simple-flask-app || true"
                sh label: '', script: "docker rm second-simple-flask-app || true"
                sh label: '', script: "docker run -d --name second-simple-flask-app -p 5001:5000 ${img}"
            }
        }

        stage('Push To DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                        // Push the image tagged with the build number
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Build Latest Image') {
            steps {
                script {
                    // Tag the image with 'latest'
                    img = registry + ":latest"
                    println ("${img}")
                    dockerImage = docker.build("${img}")
                }
            }
        }

        stage('Push Latest To DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                        // Push the image tagged as 'latest'
                        dockerImage.push()
                    }
                }
            }
        }
    }
}
