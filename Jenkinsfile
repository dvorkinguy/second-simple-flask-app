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
        stage('Checkout') {
            steps {
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Checkout' started", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
                git branch: 'main', url: 'https://github.com/dvorkinguy/second-simple-flask-app.git'
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Checkout' completed", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
            }
        }

        stage('Stop Previous Container'){
            steps{
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Stop Previous Container' started", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
                sh returnStatus: true, script: 'docker stop ${JOB_NAME}'
                sh returnStatus: true, script: 'docker rmi $(docker images | grep ${registry} | awk \'{print $3}\') --force'
                sh returnStatus: true, script: 'docker rm ${JOB_NAME}'
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Stop Previous Container' completed", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
            }
        }

        stage('Build Image') {
            steps {
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Build Image' started", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
                script {
                    // Tag the image with the build number
                    img = registry + ":build-${env.BUILD_NUMBER}"
                    println ("${img}")
                    dockerImage = docker.build("${img}")
                }
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Build Image' completed", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
            }
        }

        stage('Test - Run Docker Container on Jenkins node') {
            steps {
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Test - Run Docker Container on Jenkins node' started", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
                sh label: '', script: "docker stop second-simple-flask-app || true"
                sh label: '', script: "docker rm second-simple-flask-app || true"
                sh label: '', script: "docker run -d --name second-simple-flask-app -p 5000:5000 ${img}"
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Test - Run Docker Container on Jenkins node' completed", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
            }
        }

        stage('Push To DockerHub') {
            steps {
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Push To DockerHub' started", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                        // Push the image tagged with the build number
                        dockerImage.push()
                    }
                }
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Push To DockerHub' completed", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
            }
        }

        stage('Build Latest Image') {
            steps {
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Build Latest Image' started", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
                script {
                    // Tag the image with 'latest'
                    img = registry + ":latest"
                    println ("${img}")
                    dockerImage = docker.build("${img}")
                }
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Build Latest Image' completed", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
            }
        }

        stage('Push Latest To DockerHub') {
            steps {
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Push Latest To DockerHub' started", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                        // Push the image tagged as 'latest'
                        dockerImage.push()
                    }
                }
                slackSend(channel: '#jenkins-second-simple-flask-app', message: "Stage 'Push Latest To DockerHub' completed", teamDomain: 'not-just-devops', tokenCredentialId: 'slack-jenkins-second-simple-flask-app')
            }
        }
    }
    post {
        always {
            script {
                currentBuild.result = currentBuild.result ?: 'SUCCESS'
                slackSend(
                    channel: '#jenkins-second-simple-flask-app',  // Slack channel name
                    color: currentBuild.result == 'SUCCESS' ? 'good' : 'danger',
                    message: "Pipeline '${env.JOB_NAME}' (${env.BUILD_NUMBER}) status: ${currentBuild.result}",
                    teamDomain: 'not-just-devops',  // Slack workspace domain
                    tokenCredentialId: 'slack-jenkins-second-simple-flask-app'  // Slack credential name
                )
            }
        }
        success {
            script {
                slackSend(
                    channel: '#jenkins-second-simple-flask-app',  // Slack channel name
                    color: 'good',
                    message: "Pipeline '${env.JOB_NAME}' (${env.BUILD_NUMBER}) was successful! :tada:",
                    teamDomain: 'not-just-devops',  // Slack workspace domain
                    tokenCredentialId: 'slack-jenkins-second-simple-flask-app'  // Slack credential name
                )
            }
        }
        unstable {
            script {
                slackSend(
                    channel: '#jenkins-second-simple-flask-app',  // Slack channel name
                    color: 'warning',
                    message: "Pipeline '${env.JOB_NAME}' (${env.BUILD_NUMBER}) is unstable.",
                    teamDomain: 'not-just-devops',  // Slack workspace domain
                    tokenCredentialId: 'slack-jenkins-second-simple-flask-app'  // Slack credential name
                )
            }
        }
        failure {
            script {
                slackSend(
                    channel: '#jenkins-second-simple-flask-app',  // Slack channel name
                    color: 'danger',
                    message: "Pipeline '${env.JOB_NAME}' (${env.BUILD_NUMBER}) failed. :x:",
                    teamDomain: 'not-just-devops',  // Slack workspace domain
                    tokenCredentialId: 'slack-jenkins-second-simple-flask-app'  // Slack credential name
                )
            }
        }
        fixed {
            script {
                slackSend(
                    channel: '#jenkins-second-simple-flask-app',  // Slack channel name
                    color: 'good',
                    message: "Pipeline '${env.JOB_NAME}' (${env.BUILD_NUMBER}) is back to normal.",
                    teamDomain: 'not-just-devops',  // Slack workspace domain
                    tokenCredentialId: 'slack-jenkins-second-simple-flask-app'  // Slack credential name
                )
            }
        }
    }
}
