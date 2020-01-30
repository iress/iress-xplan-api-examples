FROM python:3.8.1-alpine

RUN apk add bash
RUN pip install pipenv

ADD . /app

WORKDIR /app
RUN pipenv install --dev --system --deploy --ignore-pipfile

CMD ["./ci/_test.sh"]
