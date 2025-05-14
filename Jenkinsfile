pipeline {
    agent { label 'linux-docker-agent' }

    environment {
        JENKINS_URL = 'http://host.docker.internal:8080'
        JENKINS_USER = 'admin'
        JENKINS_TOKEN = credentials('token_admin')
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/latypovavictoria/masters_degree.git', branch: 'main'
            }
        }

        stage('Install Python Requirements') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m pip install --upgrade pip
                            pip3 install requests
                        '''
                    } else {
                        bat '''
                            python -m pip install --upgrade pip
                            pip install requests
                        '''
                    }
                }
            }
        }

        stage('Run Security Check') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 security_check.py "$JENKINS_URL" "$JENKINS_USER" "$JENKINS_TOKEN"
                        '''
                    } else {
                        bat '''
                            python security_check.py "%JENKINS_URL%" "%JENKINS_USER%" "%JENKINS_TOKEN%"
                        '''
                    }
                }
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
