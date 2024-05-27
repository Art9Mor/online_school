FROM python:3

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

COPY . .
COPY ./entrypoint /

RUN sed -i 's/\r$//g' /entrypoint
RUN chmod u+x /entrypoint

ENTRYPOINT ["/entrypoint"]

CMD ["python3", "manage.py", "runserver"]
