# Projecto Final ML
El proyecto se realizo en python 3.12.11 con gestor de librerias conda.

El proyecto esta dividido en 6 carpetas:
* **app:** Contiene las apps y la API (en main.py) del proyecto.
* **data:** Contiene las bases de datos (los datos originales y los limpios)
* **docs:** Contiene explicaciones mas detalladas y otros datos a tener en cuenta. 
    * docs.md es el archivo donde se debe mirar la informacion. 
    * ID.md es donde mirar los ID de cada feature
    * ID.ipynb es donde se saco los ID
    * categorias.md es una lista como se relacionan las categorias entre si (que sub-issues tiene un issue por ejemplo )
* **models:** Contiene todos los modelos que se han entrenado. Los nombres consisten en que predicen (si timely response o consumer dispute), tipo de modelo(tree, knn,  random forest), en ocasiones el tipo de codificacion si se para ese modelo se han intentado ambas, si se han usado datos sinteticos para el entrenamiento (synth), y si ese modelo esta en uso. Todos los modelos se entrenaros en la carpeta de notebook en las carpetas DISPUTE o TIMELY. los modelo def son los que usan las apps(tambien las versiones antiguas)
* **Notebooks:**
    * Fuentes: donde se hizo el EDA
    * Limpiados: feature engineering y limpieza
    * Limpieza copy: version antigua de limpiador
    * Carpetas de Dispute Timely: carpetas con los nb donde se entrenaros los modelos de models con su evaluacion de rendimiento

* **src:** funciones y variables custom (como los codificadores label para los modelos de timely) pruebas con las funciones para su funcionamiento adecuado
* **requirements:**   requeimeientos del proyecto
* **enviroments:** lo mismo pero en yaml
