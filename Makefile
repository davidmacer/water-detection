all: ./data/presas_ags_prod.tif

./data/presas_ags_prod.tif: ./src/WaterBodiesImgProcess.py
	[ -d ./resultados ] || mkdir ./resultados
	python3 ./src/WaterBodiesImgProcess.py

clean:
	rm -f ./data/presas_ags_prod.tif