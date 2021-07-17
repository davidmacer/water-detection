# Para calcular los estadísticos de segundo orden
otbcli_ComputeImagesStatistics -il ./data/presas_ags_prod.tif -out ./resultados/EstimateImageStatistics.xml

# Para realizar el entrenamiento. Se utiliza la imagen de interés y el shapefile con los datos para el entrenamiento. La salida es el modelo svmModelQB1.txt
otbcli_TrainImagesClassifier -io.il ./data/presas_ags_prod.tif -io.vd ./data/datos_entrenamiento/puntos_entreno.shp -io.imstat ./resultados/EstimateImageStatistics.xml -sample.mv 100 -sample.mt 100 -sample.vtr 0.5 -sample.vfn label -classifier libsvm -classifier.libsvm.k linear -classifier.libsvm.c 1 -classifier.libsvm.opt false -io.out ./resultados/svmModel.txt -io.confmatout ./resultados/svmConfusionMatrix.csv

# Clasificación de la imagen
otbcli_ImageClassifier -in ./data/presas_ags_prod.tif -imstat ./resultados/EstimateImageStatistics.xml -model ./resultados/svmModel.txt -out ./resultados/labeled_image.tif