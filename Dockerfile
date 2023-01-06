# base image
FROM python:3.12.0a3-bullseye

# add the statically compiled IPFS binary to the image
ADD ./ipfs /usr/local/bin/ipfs

# copy the pip requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install python dependencies with pip
RUN pip install -r requirements.txt

# copy project to the image
COPY . /app

# set entrypoint & run
ENTRYPOINT [ "python" ]
CMD ["IPFSEnricher_API.py" ]
