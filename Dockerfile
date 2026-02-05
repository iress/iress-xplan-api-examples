FROM jetpackio/devbox:latest

USER root:root

ADD . /app

WORKDIR /app

CMD ["./ci/_test.sh"]
