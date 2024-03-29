# Budget App 
## based on Java Quarkus Webapp Template
<https://github.com/joshroche1/projects/tree/master/templates/java-quarkus>

<http://quarkus.io>

Contains:
 - RESTEasy Reactive Jackson
 - Qute templating
 - Agroal
 - Hibernate ORM with Panache
 - Quarkus JPA Security
 - JDBC PostgreSQL/H2 driver/module

## Directory Structure

- mvnw
- pom.xml
- /src/
- - /main/
- - - /resources/
- - - - application.properties
- - - - import.sql
- - - - /META-INF/resources/css|img|js/
- - - - /templates/
- - - - - base.html
- - - - - base-user.html
- - - - - /PublicResouce/
- - - - - - index.html
- - - - - - login.html
- - - - - /UserResource/
- - - - - - list.html
- - - - - /AccountResource/
- - - - - - list.html
- - - - - - detail.html
- - - - - - create.html
- - - /java/net/jar/quarkus/budgetapp/
- - - - - - - - AdminResource.java
- - - - - - - - PublicResource.java
- - - - - - - - Startup.java
- - - - - - - - UserEntity.java
- - - - - - - - UserResource.java
- - - - - - - - AccountEntity.java
- - - - - - - - AccountResource.java

## Web/REST Endpoints:

<http://localhost:8080/>

<http://localhost:8080/login>

<http://localhost:8080/users/list>

<http://localhost:8080/users/me>

## To Run in Developer Mode:

> quarkus dev

### Build JAR file

> quarkus build

### Run Application:

> java -jar ./target/quarkus-app/quarkus-run.jar
