pipeline {
    agent any

    environment {
        JENKINS_URL = 'http://localhost:8080'
        JENKINS_USER = 'admin'
        JENKINS_TOKEN = credentials('token_admin')    // Jenkins Credentials ID
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/latypovavictoria/masters_degree.git', branch: 'main'
            }
        }

        stage('Install Python Requirements') {
            steps {
                sh 'pip install requests'
            }
        }

        stage('Run Security Check') {
            steps {
                sh '''
                python3 security_check.py "$JENKINS_URL" "$JENKINS_USER" "$JENKINS_TOKEN"
                '''
            }
        }

        stage('Publish Report') {
            steps {
                archiveArtifacts artifacts: 'security_report.json', fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
