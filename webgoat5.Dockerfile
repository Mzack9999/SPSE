FROM anapsix/alpine-java:jdk8

ENV APP /

RUN apk update && apk add ca-certificates && update-ca-certificates && apk add openssl

RUN  wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/webgoat/WebGoat-5.4.war

WORKDIR $APP
  
EXPOSE 8080

CMD ["java","-jar","WebGoat-5.4.war"]
