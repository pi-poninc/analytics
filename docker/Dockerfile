FROM amazonlinux:latest
ENV FLASK_APP=application.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /usr/src/elastic_search/src

RUN yum -y install which aws-cli git 
RUN yum -y install curl tar rpm

RUN yum -y install python3
RUN pip3 install --upgrade pip setuptools
ADD ./docker/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./src /usr/src/elastic_search/src

EXPOSE 5000
CMD ["flask", "run"]
