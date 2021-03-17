FROM amazonlinux:latest
ARG GITHUB_TOKEN
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN yum -y install which aws-cli git 
RUN yum -y install curl tar rpm

RUN yum -y install python3
RUN pip3 install --upgrade pip setuptools
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN git clone https://$GITHUB_TOKEN:x-oauth-basic@github.com/pi-poninc/elastic_search.git
EXPOSE 5000
ADD . /elastic_search
WORKDIR /elastic_search/src
CMD ["flask", "run"]