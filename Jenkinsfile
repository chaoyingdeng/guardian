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
                credentialsId: 'root',
                url: 'git@github.com:chaoyingdeng/guardian.git'
				}

            }
        }

		stage('init') {
            steps {
			sh '''
			pwd
			whoami
			python3 -m venv
			source venv/bin/activate
			pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


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
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                report: 'allure-report',
                results: [[path: 'report/allure-results']]
            ])



            echo "${BUILD_URL}"

            sh "python3 utils/emails.py ${BUILD_URL}allure/"


		}


	}
}
