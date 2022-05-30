FROM python:3.8.3

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./Pipfile* /usr/src/app/
RUN pip install --no-cache-dir pipenv \
    && pipenv install --deploy --system --ignore-pipfile

COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
