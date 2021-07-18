all: ./data/presas_ags_prod.tif ./resultados/labeled_image.tif

./resultados/labeled_image.tif: ./src/segmentacion.otb.sh ./data/presas_ags_prod.tif
	./src/./src/segmentacion.otb.sh

./data/presas_ags_prod.tif: ./src/WaterBodiesImgProcess.py
	[ -d ./resultados ] || mkdir ./resultados
	python3 ./src/WaterBodiesImgProcess.py

clean:
	rm -f ./data/presas_ags_prod.tif