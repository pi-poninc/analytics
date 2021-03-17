FROM amazonlinux:latest
ARG GITHUB_TOKEN
ARG FLASK_APP

RUN yum -y install which aws-cli git 
RUN yum -y install curl tar rpm

RUN yum -y install python3
RUN pip3 install --upgrade pip setuptools
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN git clone https://$GITHUB_TOKEN:x-oauth-basic@github.com/pi-poninc/elastic_search.git
ADD . /elastic_search
WORKDIR /elastic_search/src
CMD ["flask", "run"]