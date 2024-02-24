pipeline {
    agent any
    options {
        disableConcurrentBuilds() // 禁止并发构建
        timeout(time: 2, unit: 'HOURS') // 设置构建超时时间为1小时
        buildDiscarder(logRotator(numToKeepStr: '5')) // 保留最近的 5 次构建
    }

    stages {
        stage('Build') {
            steps{
            echo 'hello guardian'
            }
        }


		stage('Cleanup') {
            steps {
			sh '''
            echo "delete file"
            ls | grep -v venv | xargs rm -rf
            echo "delete success"
			'''
          }
        }


        stage('get guardian code') {
            steps {
                retry(3) {
                git branch: 'master',
                credentialsId: 'chaoying',
                url: 'git@github.com:yingzhixiaochaoren/guardian.git'
				}

            }
        }

		stage('init') {
            steps {
			sh '''
			python3 -m venv ./venv
			source venv/bin/activate
			pip3 install -r requirements.txt -i https://pypi.douban.com/simple/


			deactivate
			'''

            }
        }

		stage('execute') {
            steps {
			sh '''
			source venv/bin/activate

			venv/bin/pytest

			deactivate
			'''
          }
        }
    }


	post{
		always{
		    sh '''
			python3 utils/emails.py
			'''
		}
	}
}
