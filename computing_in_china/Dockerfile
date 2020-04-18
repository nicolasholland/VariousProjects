FROM daocloud.io/python:3

ENV mirror mirrors.aliyun.com
ENV pypi http://$mirror/pypi/simple/

#TODO this is just for the dummy file
RUN mkdir -p /tmp

# Install external dependencies
ADD dependencies.txt /tmp/dependencies.txt

RUN pip install --upgrade pip -i $pypi --trusted-host $mirror
RUN pip install -r /tmp/dependencies.txt -i $pypi --trusted-host $mirror

CMD jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
