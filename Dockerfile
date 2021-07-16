FROM mundialis/esa-snap:ubuntu
WORKDIR /workdir
COPY . .
RUN pip install \
    numpy \
    pyshp \
    pygeoif \
    matplotlib