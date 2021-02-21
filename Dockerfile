FROM python:3.8

COPY dist/shepherd-1.0.0-py3-none-any.whl shepherd-1.0.0-py3-none-any.whl

RUN pip install shepherd-1.0.0-py3-none-any.whl

RUN pip install 'connexion[swagger-ui]'

ENV FLASK_APP=shepherd

COPY tests/data.sql data.sql

RUN flask init-db

RUN flask write-test-data data.sql

EXPOSE 8081

CMD flask run --port=8081