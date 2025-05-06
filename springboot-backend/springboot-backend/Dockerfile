FROM openjdk:21-jdk-slim
COPY target/springboot-backend-1.0.0.jar app.jar
ENV SPRING_PROFILES_ACTIVE=prod
ENTRYPOINT ["java", "-jar", "/app.jar"]
