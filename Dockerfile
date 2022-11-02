ARG PYHHON_MAJOR_VER=3
ARG PYTHON_MINOr_VER=9

FROM python:${PYTHON_MAJOR_VER}.${PYTHON_MINOR_VER}-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv/py${PYTHON_MAJOR_VER}${PYTHON_MINOR_VER}
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir

# Run the application:
COPY . /app 
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
