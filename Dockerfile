FROM mundialis/esa-snap:ubuntu
WORKDIR /workdir
COPY . .
RUN pip install \
    numpy \
    pyshp \
    pygeoif \
    matplotlib
RUN apt-get update && apt-get install --yes \
    file
RUN wget https://www.orfeo-toolbox.org/packages/OTB-7.3.0-Linux64.run
RUN chmod +x OTB-7.3.0-Linux64.run
RUN ./OTB-7.3.0-Linux64.run
RUN rm ./OTB-7.3.0-Linux64.run
RUN source ./workdir/OTB-7.3.0-Linux64/otbenv.profile