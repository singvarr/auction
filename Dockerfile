FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./Pipfile* .
RUN pip install --upgrade pipenv
RUN pipenv install

COPY . .

CMD [ "pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:$PORT"]
EXPOSE $PORT
