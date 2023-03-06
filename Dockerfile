FROM python:3.11.2-slim-buster
WORKDIR /app
COPY . /app
RUN pip3 install memory_profiler matplotlib
ENTRYPOINT []
