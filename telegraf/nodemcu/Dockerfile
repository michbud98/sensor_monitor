FROM telegraf

RUN mkdir /home/root
WORKDIR /home/root
# TODO USE VOLUME
COPY get_weather_data_nodemcu.py /etc/telegraf/
#COPY telegraf_sensor_data_nodemcu.conf /etc/telegraf/telegraf.conf

RUN apt-get update && apt-get install python3 python3-pip -y
RUN pip3 install requests beautifulsoup4

#CMD [ "/bin/bash" ]

ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "telegraf" ]