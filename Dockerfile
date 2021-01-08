
FROM python:3.8.5

WORKDIR /code

COPY . .

RUN pip install -r ./requirements.txt

RUN chmod a+x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000 





