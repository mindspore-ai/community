FROM python:3.8

RUN apt-get update
RUN apt-get install vim --yes

WORKDIR /OpenDataology

COPY . .

# install env
RUN pip install -r requirements.txt --no-cache-dir

RUN sed -i '5i from werkzeug.utils import cached_property' /usr/local/lib/python3.8/site-packages/werkzeug/__init__.py


EXPOSE 8080

CMD python app.py