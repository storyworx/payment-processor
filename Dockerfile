ARG PYTHON_MAJOR_VER=3
ARG PYTHON_MINOR_VER=10
ARG VIRTUAL_ENV=/opt/venv/py${PYTHON_MAJOR_VER}${PYTHON_MINOR_VER}



FROM python:${PYTHON_MAJOR_VER}.${PYTHON_MINOR_VER}-slim as build
ARG PYTHON_MAJOR_VER
ARG PYTHON_MINOR_VER
ARG VIRTUAL_ENV
RUN apt-get update && apt-get -y install gcc default-libmysqlclient-dev
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir



FROM python:${PYTHON_MAJOR_VER}.${PYTHON_MINOR_VER}-slim
ARG VIRTUAL_ENV

# DB args
# ARG DB_HOST
# ARG DB_PORT
# ARG MYSQL_PASSWORD
# ARG MYSQL_USER
# ARG MYSQL_DATABASE

COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}
RUN apt-get update && apt-get -y install default-libmysqlclient-dev
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD . /app
WORKDIR /app

# RUN python manage.py migrate

# Run the application:
#ENTRYPOINT ["python"]
#CMD ["manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["docker-entrypoint.sh"]
