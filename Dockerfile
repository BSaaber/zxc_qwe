# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --dev

COPY ./app /code/app

EXPOSE 3030

# set in docker-compose.yml
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]