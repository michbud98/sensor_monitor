FROM python:3
WORKDIR /machine
ADD . /machine
RUN pip install -e .
ENTRYPOINT [ "python", "-m", "dummy_machines" ]
CMD [ "-h" ]
# docker run --rm --network="host" dummy-machines -s 5 -url http://localhost:8000 Thermometer 1