FROM python:3.7
ENV PYTHONUNBURRERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /code
