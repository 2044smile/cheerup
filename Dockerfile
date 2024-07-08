FROM python:3.11-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install linux dependencies 
RUN apk update && apk upgrade && \
    apk add --no-cache gcc g++ musl-dev curl libffi-dev postgresql-dev zlib-dev jpeg-dev freetype-dev

# install poetry to manage python dependencies
RUN curl -sSL https://install.python-poetry.org | python3 -
# add poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# install python dependencies
COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN poetry install

# copy project
COPY . .

# run at port 8000
EXPOSE 8000
CMD ["poetry", "run", "python3", "manage.py", "runserver", "0.0.0.0:8000"]
