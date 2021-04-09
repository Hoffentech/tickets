FROM python:3

RUN mkdir -p /config
COPY deploy/odbc.sh /config/
COPY requirements.txt /config/
RUN sh ./config/odbc.sh 
RUN pip3 install --no-cache-dir -r ./config/requirements.txt