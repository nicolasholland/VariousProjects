FROM continuumio/anaconda3

ENV CONDA /opt/conda

RUN apt-get -y install make g++

RUN conda install -c anaconda protobuf=3.5.1

WORKDIR /root

ADD . /root

RUN make

CMD make run

