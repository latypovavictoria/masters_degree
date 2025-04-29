FROM ubuntu:22.04

# Установка базовых пакетов
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    curl wget unzip git openjdk-11-jre-headless \
    ca-certificates gnupg lsb-release \
    docker.io \
    && apt-get clean

# Установка Trivy
RUN wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.50.0_Linux-64bit.deb \
    && dpkg -i trivy_0.50.0_Linux-64bit.deb \
    && rm trivy_0.50.0_Linux-64bit.deb

# Установка OWASP Dependency-Check
RUN wget https://github.com/jeremylong/DependencyCheck/releases/latest/download/dependency-check-8.4.0-release.zip \
    && unzip dependency-check-8.4.0-release.zip -d /opt/ \
    && ln -s /opt/dependency-check/bin/dependency-check.sh /usr/local/bin/dependency-check

# Установка Allure (если нужен CLI для локального прогона)
RUN wget https://github.com/allure-framework/allure2/releases/latest/download/allure-2.21.0.tgz \
    && tar -zxvf allure-2.21.0.tgz -C /opt/ \
    && ln -s /opt/allure-2.21.0/bin/allure /usr/local/bin/allure

# Установка Python-зависимостей
COPY scanner/requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Создание рабочего каталога
WORKDIR /home/jenkins/agent

# Установка агента Jenkins Remoting
RUN curl --create-dirs -o /home/jenkins/agent/remoting.jar https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/320/remoting-320.jar

# Переменные
ENV AGENT_WORKDIR=/home/jenkins/agent

# Команда запуска: ожидание подключения
ENTRYPOINT ["java", "-jar", "/home/jenkins/agent/remoting.jar"]
