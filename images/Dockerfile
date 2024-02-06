
FROM maven:latest as BUILD

WORKDIR /app

COPY .. .

RUN mvn clean package assembly:single


FROM openjdk:latest as RUN

COPY --from=BUILD ./app/target/madissues-backend-1-jar-with-dependencies.jar app1.jar

CMD ["java", "-cp", "./app1.jar", "org.madissues.apps.restApi.Main"]

