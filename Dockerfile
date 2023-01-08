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
# ARG role
# ENV ROLE $role

COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}
RUN apt-get update && apt-get -y install default-libmysqlclient-dev
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD . /app
WORKDIR /app
COPY conf/prod/.env-docker .env

# # Run the application:
# ENTRYPOINT ["/bin/sh"]
# CMD ["docker-entrypoint.sh"]
