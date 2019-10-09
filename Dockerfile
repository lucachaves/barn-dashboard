FROM python:3.6.9
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN cp /usr/share/zoneinfo/Europe/Helsinki /etc/localtime
CMD python app.py