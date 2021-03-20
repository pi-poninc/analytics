FROM amazonlinux:latest
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /usr/src/elastic_search/src

RUN yum -y install which aws-cli git 
RUN yum -y install curl tar rpm

RUN yum -y install python3
RUN pip3 install --upgrade pip setuptools
ADD ./docker/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# RUN git clone https://$GITHUB_TOKEN:x-oauth-basic@github.com/pi-poninc/elastic_search.git
COPY ./src /usr/src/elastic_search/src

EXPOSE 5000
# ADD . /elastic_search
# WORKDIR /elastic_search/src
CMD ["flask", "run"]
