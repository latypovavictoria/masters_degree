# Руководство пользователя

#### Получение плагинов Jenkins через скрипт jenkins_plugins.py
  ```python3 jenkins_plugins.py --url https://jenkins.ya-dev.miem.vmnet.top --user ****** --token ******* ```

#### Настройка агента Jenkins
  ```cd node``` --- перейти в дирректорию
  
  ```docker-compose up -d --build``` - собрать агент для Jenkins, далее увидеть в самом Jenkins, что он подключился, рекомендуется выполнять все пайплайны с этого узла.

#### Настройка пайплайнов Jenkins.

Все скрипты уже разработаны и готовы к использованию, необходимо только применить сам Jenkinsfile для джобы.

Необходимо получить API NVD KEY, сделать это можно на сайте - https://nvd.nist.gov/developers/api-key-requested

Для джобы загрузки всех плагинов используется скрипт прям в корне проекта - ```Jenkinsfile```.

Для джобы с проверкой всех уязвимых плагинов при помощи NVD KEY и выгрузки отчетов используется скрипт - ```scripts_reports/Jenkinsfile``.

#### Сборка собственного плагина в hpi.

Данный плагин уже написан и есть в репозитории.

Если требуется собрать заново с указанием своих зависимостей:

# Сборка `.hpi`-плагина Jenkins в Windows

## Необходимые компоненты
- **Java JDK** (8 или 11)
- **Apache Maven**
- **Git для Windows** (опционально)
- **Исходный код плагина**

## 1. Установка необходимого ПО

### 1.1. Установка Java JDK
1. Скачайте JDK с [официального сайта Oracle](https://www.oracle.com/java/technologies/javase-downloads.html)
2. Запустите installer и следуйте инструкциям
3. Проверьте установку:
```cmd
java -version
javac -version
```

### 1.2. Установка Maven
Скачайте Maven с официального сайта

Распакуйте архив в C:\Program Files\apache-maven-3.x.x

Добавьте в переменные среды:

M2_HOME = C:\Program Files\apache-maven-3.x.x

В Path добавьте %M2_HOME%\bin

Проверьте установку:

```cmd
mvn -version
```

## 2. Сборка плагина

### 2.1. Получение исходного кода

```cmd
git clone https://github.com/jenkinsci/your-plugin-repo.git
cd your-plugin-repo
```

### 2.2. Сборка плагина

```cmd
mvn clean package
```

После сборки файл your-plugin.hpi будет в папке target\

### 3. Установка плагина в Jenkins
Откройте Jenkins в браузере

Перейдите: ```Управление Jenkins → Управление плагинами → Дополнительно```

В разделе "Загрузить плагин" выберите ваш .hpi-файл

Перезапустите Jenkins

### 4. Создание нового плагина (если нужно)

#### 4.1. Генерация шаблона
```cmd
mvn archetype:generate -Dfilter=io.jenkins.archetypes:hello-world
```
Затем укажите:

groupId (например, com.mycompany)

artifactId (название плагина)

Остальные параметры (можно оставить по умолчанию)

### 4.2. Сборка нового плагина

```cmd
cd ваш-плагин
mvn clean package
```

#### Полезные советы
Для работы с кодом рекомендуется использовать IntelliJ IDEA или Eclipse

Если возникают проблемы с зависимостями, попробуйте:
```
cmd
mvn clean install -U
```

### Для отладки можно использовать:

```
cmd
mvn hpi:run
```

#### После того, как установлен plugin, можно воспользоваться скриптом:

```Jenkinsfile_plugin```

Далее написан скрипт по деплою nginx: ```nginx_deploy/Jenkinsfile```





