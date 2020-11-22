FROM balenalib/raspberrypi3-python:build

ENV HOSTNAME="docker_test_env"
ENV INFLUX_HOST="https://eu-central-1-1.aws.cloud2.influxdata.com"
# FIXME ADD TOKEN INPUT
ENV INFLUX_TOKEN="pIbl-CNv5q6onoqnev6VzDrYPw3U2ATHjmntsgkoD4OnYDy0hW1X9IWYqhvhCNjU5VJEG9VAiuKfUOb3zKsG0g=="
ENV INFLUX_ORG="swiftblade1982@gmail.com"
ENV INFLUX_BUCKET="Sensor_data"

RUN useradd -m pi

COPY . /home/pi

WORKDIR /home/pi

RUN ./install_telegraf_docker.sh

CMD ["telegraf", "--once"]

