FROM ubuntu:22.04

# Установка базовых пакетов
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    curl wget unzip git openjdk-11-jre-headless \
    ca-certificates gnupg lsb-release \
    docker.io \
    file \
    && apt-get clean

# Установка Trivy
RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor -o /usr/share/keyrings/trivy.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/trivy.list \
    && apt-get update \
    && apt-get install -y trivy

# Установка OWASP Dependency-Check
RUN wget https://github.com/jeremylong/DependencyCheck/releases/download/v12.1.0/dependency-check-12.1.0-release.zip \
    && unzip dependency-check-12.1.0-release.zip -d /opt/ \
    && ln -s /opt/dependency-check/bin/dependency-check.sh /usr/local/bin/dependency-check \
    && rm dependency-check-12.1.0-release.zip

# Установка Allure (CLI для локального прогона)
RUN wget https://github.com/allure-framework/allure2/releases/download/2.34.0/allure-2.34.0.tgz \
    && tar -zxvf allure-2.34.0.tgz -C /opt/ \
    && ln -s /opt/allure-2.34.0/bin/allure /usr/local/bin/allure \
    && rm allure-2.34.0.tgz

# Установка Python-зависимостей
COPY scanner/requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Создание рабочего каталога
WORKDIR /home/jenkins/agent

# Установка агента Jenkins Remoting
RUN curl -L -o /home/jenkins/agent/remoting.jar https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/320/remoting-320.jar && file /home/jenkins/agent/remoting.jar

# Переменные
ENV AGENT_WORKDIR=/home/jenkins/agent

# Команда запуска: ожидание подключения
ENTRYPOINT ["java", "-jar", "/home/jenkins/agent/remoting.jar"]
