FROM eclipse-temurin:21-jre-jammy

RUN groupadd --system antar \
    && useradd --system --gid antar --home-dir /app --shell /usr/sbin/nologin antar

WORKDIR /app

COPY target/antar-*.jar app.jar

RUN chown antar:antar /app/app.jar

USER antar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
