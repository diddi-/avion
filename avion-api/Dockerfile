FROM python:3.10

ENV FLASK_APP=avion.api.app
ENV FLASK_DEBUG=true

EXPOSE 5000
COPY entrypoint.sh /
RUN mkdir /db \
    && chmod +x /entrypoint.sh \
    && wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.4.0/flyway-commandline-9.4.0-linux-x64.tar.gz | tar xvz && ln -s `pwd`/flyway-9.4.0/flyway /usr/local/bin
ENTRYPOINT /entrypoint.sh
