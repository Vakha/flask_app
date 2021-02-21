FROM python:3.8

COPY dist/shepherd-1.0.0-py3-none-any.whl shepherd.whl

RUN pip install shepherd.whl

RUN pip install 'connexion[swagger-ui]'

COPY tests/data.sql data.sql

RUN flask init-db

RUN flask write-test-data data.sql

CMD flask run
