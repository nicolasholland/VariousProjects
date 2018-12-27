FROM continuumio/anaconda3

WORKDIR /app

ADD . /app

RUN conda install flask numpy matplotlib pillow tensorflow 
RUN pip install -e .

ENV FLASK_APP merrychristmas

EXPOSE 5000

CMD flask run
