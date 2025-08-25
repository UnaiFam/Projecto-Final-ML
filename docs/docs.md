# DOCUMENTACION
librerias en requirements.txt
## Objetivo del proyecto

Se pretende estimar primero la si la respuesta a tiempo (algo que aparentemente fue bastante facil) y luego usar este dato para estimar la si el cliente disputo o no. 
Tras esto se pretende utilizar ambos modelose introducirlos o en una API de fast api o en una app de gradio (aunque finalmente e han hecho 2 una para cada modelo porque no se me ocurrio como meterlo en el mismo). 


## Fuente de Datos y resumen de EDA
 en carpeta data
 En ocasiones se añade una etiquta aunque no haga falta
* **Complaint ID**: ID de la queja
* **Product**:	Producto al que hace referencia la queja. Hay 11 productos en total. No esta equilibrado. 
    * Debt collection            
    * Mortgage                   
    * Credit reporting           
    * Credit card               
    * Bank account or service    
    * Consumer loan              
    * Student loan               
    * Payday loan                 
    * Money transfers            
    * Prepaid card               
    * Other financial service 
    Se añade la etiqueta "Unknown or not speficied"   para los datos faltantes 
    Muy relacionado con subproducto
* **Sub-product**: DEstro de un producto la parte concreta. La mayoria esta vacia. Solo los :
    * 'Debt collection', 
    * 'Mortgage', 
    * 'Consumer loan',
    * 'Bank account or service', 
      'Money transfers', 
    * 'Student loan',
    * 'Prepaid card', 
    * 'Other financial service 
    tienen subproductos. "Debt collection" tambien tiene alguna queja en la que no tiene subproducto.
    Se añade la etiqueta "Unknown or not speficied"   para los datos faltantes  
    El resto no tiene subproducto.Para mas info consulat categorias.md

* **Issue**	: Hay 90 categorias Aunque creo que algunas son muy similares. Aun asi para evitar problemas no se va a tocar. Se añade la etiqueta "Unknown or not speficied"   para los datos faltantes

* **Sub-issue**	:Solo 'Debt collection', 'Credit reporting' tienen esto y hay 47 distintas (mirar mas abajo para detalles). El resto es una categoria vacia. 
Se rellenara con una etiqueta "Unknown or not specified", para la facilidad de uso. Para mas info consulat categorias.md

* **State**	: Son los 50 estados de EEUU,  otros territorios controlados por el(	Puerto Rico, Islas Vírgenes, Guam, Samoa Americana, Islas Marshall, Palaos ) y dos designagiones militares (AE Armed Forces Europe, y AP Armed Forces Pacific). Hay valores faltantes.Se intentara rellenar con el 

* **ZIP code**: Hay varias que que no tienen estado pero si postal. Se puede intentar sacar el estado e  ignorar esta variable para evitar problemas de prvaciad. Pero viendo que los modelos de dispute 

* **Date received**	: Entre 2015-01-01 hasta 2015-03-15
* **Date sent to company**	:Fecha que llego a la compañia parece que en todos los casos llega y se recibe el mismo dia.
     Hay menos en fin de semana y       no    hay festivos.

    Estos datos no son muy utiles a pesar de que se saco en los dias laborales (que son todos) y los dias de retraso(que no tiene ya que los dias no tiene).

    * dias de retraso: inutil porque parece que en todos es 0 no se pondra
    * weekday:  dia de la semana los fines de smana hay menos qujas       
    * holiday: todos los dias son laborables y el siguiente tambien al parecer

* **Company**:hay como 1500 y siemmpre hay. No parece importante. Ya que coeficiente de cramer para Consumer disputed? es de 0,188. los cual no es muy alto, sobre todo si tinemos en cuenta que hay 1500 que darian problemas para codificarlos en one hot. P.D.  timely tiene cramer de 0.732  on esto lo que aloemtos. Al mejors


* **Company response**:	Siempre tiene y son:
    * 'In progress' 
    * 'Closed with explanation'
    * 'Closed with non-monetary relief'
    * 'Closed'
    * 'Closed with monetary relief'
    * 'Untimely response'
    Esta muy desbalanceado con 'Closed with explanation' siendo el mas frecuente. Sin embargo dependiendo del modelo onehot  es mu

* **Timely response?**: Solo contiene Si y no. Pero solo hay como 700 quejas que no se han respondido a tiempo.  P.D.  timely tiene cramer de 0.732  on esto lo que aloemtos.

* **Consumer disputed?**:estan si , no, y nan. Muy desbalanceado. La inmensa mayoria es NaN. las que estan in progress tiene sentido ( posiblemente se rellene con la categoria in progress) pero en el resto no se sabe como intrepretarlo.
Esto se debe muy probablemente segun a la muy problable base de [datos original](https://cfpb.github.io/api/ccdb/fields.htmhttps://cfpb.github.io/api/ccdb/fields.html) descontinuo estavariable en 2017 (aunque los datos son de 2015). 
Nan se sintepreta como no informacion y se eliminara cuando haga falta

---

Parece para la mayoria de variables no hay una diferencia de poblacion segun comsumer response quitando las fechas, aunque esto seguramente se deba a que aun no se ha confirmado que el consumidor vaya a disputar.

---
* La disputa del consumidor parece presionar a las empresas a dar explicaciones más detalladas, aunque no necesariamente mejora la probabilidad de recibir un alivio.

* En cambio, cuando el consumidor no disputa, es más común que haya habido alguna forma de compensación (sobre todo no monetaria).



incidente :tras una semana trabajanod me he dado cuenta que la funcion de zip cunaod se llama po py elimina todos los estado por lo que todos los modelos que estado haciendo son inutiles excepto los timely. Esto me ha dado la idea limpiar los datos en limpieza copy.ipynb y guardalo como csv

## Feature engineerig y limpieza de los datos
Limpiador.ipynb 
* Para los casos en los que se tenia el ZIP code pero no el estado de procedencia se ha utilizado la API (zippotam)[https://api.zippopotam/] para buscar el ZIP. El estado se paso a las iniciales y se queda en el dataframe.

* Para los zip vacios se relleno con el codigo Zip 0
* Para los estados desconocidos se relleno con la etiqueta Unknown
* Para el el resto de variables se relleno con la etiqueta Unknown or not specified

Para feature engineering se las fechas se sacaron 3 variables adicionales:
* dias de retraso (que no se uso porque en todos los casos es 0, y no se acabo usando)
* weekday (En forma de texto)
* holiday (si es dia de fiesta o no. No se acabo usando porque todos son laborables )

Tammbie se eliminaros los casos con company response in progres o untimley respone porque es un dato sobrante o inconlcuso.


## Modelos de timely response?
En el nb de entrenamiento intentara sacar el estado si no tiene el a pesar de que el modelo no lo use como tal.

Para el modelo se elimianron la columna de compañia, y la respuesta de compañia in progress, Complaint ID,  Consumer disputed?, ZIP code,Date received, Date sent to company. No se metio feature engineering.
Se metio resampleo con ADASYN.
El primero se miro cp
El modelo es un decision tree al que se optimizo con grid search buscando maxima accuracy . 
El modelo NO TIENE PRERPROCESADO. Es necesario alimentarle directamente los ID. consultar los ID




Se metio: 

DecisionTreeClassifier(criterion='entropy', max_depth=30, min_samples_leaf=1)


| Clase                  | Precisión | Recall | F1-Score | Soporte |
| ---------------------- | --------- | ------ | -------- | ------- |
| No                     | 0.93      | 0.94   | 0.93     | 4971    |
| Yes                    | 0.94      | 0.93   | 0.93     | 4924    |
| **Accuracy Total**     |           |        | **0.93** | 9895    |
| **Promedio Macro**     | 0.93      | 0.93   | 0.93     | 9895    |
| **Promedio Ponderado** | 0.93      | 0.93   | 0.93     | 9895    |


| Verdadero \ Predicho | No     | Yes    |
| -------------------- | ------ | ------ |
| No                   | 0.9366 | 0.0634 |
| Yes                  | 0.0737 | 0.9263 |

0.9315 acuraccy medio

Se considero el modelo como suficiente ya que este no es el modelo principal



| Nº | Característica   | Importancia |
| -- | ---------------- | ----------- |
| 5  | Company response | 0.3569      |
| 4  | State            | 0.1859      |
| 3  | Sub-issue        | 0.1505      |
| 0  | Product          | 0.1166      |
| 1  | Sub-product      | 0.1096      |
| 2  | Issue            | 0.0805      |

Este modelo tiene tres problemas:
* Realmente este modelo "hace trampas" ya que el factor mas importante es company response. Company respone dice si esta cerrado o si a tenido timely response asi que en cierta manera el modelo ya tiene el target incorporado.  
La mera existendia de Company response como feature no tiene sentido fisico ya que para cuando la empresa sepa como responder no tiene importancia. aunuqe se elimine y se reentrene . 

* Esta algo sobreajustado (por alta profundidad) (normall en los tree), y ademas es algo dificil de interpretar ()
Asi que vamos a eliminar el company responnse (03_Entrenamiento_Evaluacion forest timely sin company res.ipynb)

Se utilizara  modelo sin el company response 



Para sin company response:
| Metric   | Value    |
|----------|----------|
| Accuracy | 0.8922   |
| AUC-ROC  | 0.8918   |

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| No    | 0.86      | 0.94   | 0.90     | 4990    |
| Yes   | 0.93      | 0.84   | 0.89     | 4923    |

| Average Type  | Precision | Recall | F1-Score | Support |
|---------------|-----------|--------|----------|---------|
| Macro Avg     | 0.90      | 0.89   | 0.89     | 9913    |
| Weighted Avg  | 0.90      | 0.89   | 0.89     | 9913    |

| Confusion Matrix | Predicted No | Predicted Yes |
|-----------------|--------------|---------------|
| Actual No       | 0.9407       | 0.0593        |
| Actual Yes      | 0.1570       | 0.8430        |

|| Feature  Importance
|-----------------|--------------|
|Sub-product   | 0.241308|
|      Product   | 0.236710|
|        State   | 0.218347|
|        Issue   | 0.157413|
|    Sub-issue  |  0.146222|


No hay tanta diferencia asi que no es como si todo el modelo dependa de esa variable. Ademas se cambi el  'min_samples_leaf' de 15 a 30 en vez de1 15 aun asi intentara dar el minimo ( mejora el acuraccy pero aumenta el riesgo de sobreajuste)

Sigue no t (cv score 0.9  o asi y no hay mucha std) y interpretabilidad
optimizado por auc-roc (equilibiro) (mas general que accuracy aunque no deberia d¡importar tanto con un oversamples)
guardado como modelo modelo_timely_rf_sin_company.pkl 
{'criterion': 'entropy', 'max_depth': 25, 'min_samples_leaf': 15}

ligeramente mejor (roc acue de .90 vs 0.89) que un arbol normal aunque mas lento, se pierde mas interpretablidad, y es masmas sobreajustado por lo que no se usara (aun asi las apps v3 usan el modelo)

| Metric        | Value             |
|---------------|-----------------|
| Accuracy      | 0.9056          |
| AUC-ROC       | 0.9054          |

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| No    | 0.89      | 0.93   | 0.91     | 4990    |
| Yes   | 0.92      | 0.88   | 0.90     | 4923    |

| Average Type  | Precision | Recall | F1-Score | Support |
|---------------|-----------|--------|----------|---------|
| Macro Avg     | 0.91      | 0.91   | 0.91     | 9913    |
| Weighted Avg  | 0.91      | 0.91   | 0.91     | 9913    |


       Feature  Importance
1  Sub-product    0.235141
0      Product    0.204629
4        State    0.203752
3    Sub-issue    0.191250
2        Issue    0.165228




## Modelo de Company Response
Esto modelo se esta intentando que guardarlo como pipeline pero tengo problemas de guardado por lo que es necesario 


<code>
sys.path.append(os.path.abspath("../src"))  

import __main__



def convert_to_str(X):
    return X.astype(str)
__main__.convert_to_str = convert_to_str



os.chdir("../src")´
<code>

Por algun problema que tuve con formato pickle  ponerlo en la pipeline y es necesario engañar a python de que es una funcion base y no custom.

Todos estos se ha intentado seguir el mismo formato en forma de pipeline para que solo haya que llamarlo (y que no pase como con timely)

SE utilizara onehot encoders
Se han intentado varios modelos entre ellos SVC, KNN, XBClassifier, gradient boost , clustering y (redes neuronales a pesar de que la pipelineno consigo integrarla). Pero sin feature engineering no dan un ninguno da un accuracy que llegue ni al 60%, y suelen rondar algo por encima del 50 %(mejor que tirar una moneda al aire) o solo predicen un valor para todos los casos. Por lo que no se va hablar de estos modelos.

Despues se intento meter compañia y el dia de la semana y con random forest. Parece que ha mejordo ligeramente  ya que 


| Clase                  | Precisión | Recall | F1-Score | Soporte |
|------------------------|-----------|--------|----------|---------|
| 0                      | 0.29      | 0.55   | 0.38     | 1045    |
| 1                      | 0.83      | 0.62   | 0.71     | 3760    |
| **Accuracy Total**     |           |        | **0.60** | 4805    |
| **Promedio Macro**     | 0.56      | 0.58   | 0.54     | 4805    |
| **Promedio Ponderado** | 0.71      | 0.60   | 0.64     | 4805    |


Confusion Matrix:


| Clase Verdadera \ Predicha | 0       | 1       |
|----------------------------|---------|---------|
| 0                          | 0.5493  | 0.4507  |
| 1                          | 0.3819  | 0.6181  |


Apenas es mejor que una moneda pero a fecha de 6/8 es el mejor mdelo

Mire que se si se unen  issue y subsisser parece que reduce el tiempo de entrenamiento ya quey en un onehot encoder no hace falta codificar los issues (a pesar de que luego se vaya a olvidar esto cuando lo necesito urgentemente) pero no se hasta que punto es fiable

Me sospecho que lo que limita los modelos son la falta de datos (solo 6000 utiles) y de variables relacionadas (Ninguna de las variables tienen una diferencia poblacional clara para consumer disputed).
SE necesitan mas datos y mas features.

Se ha intentado generar mas datos segun las pruebas:
* CTGANSynthesizer 78%
* GaussianCopulaSynthesizer 90%
* TVAESynthesizer 79,33%
* CopulaGANSynthesizer 78.74%

GaussianCopulaSynthesizer en teoria es el mas similar aunque el CTGANSynthesizer hace que los modelos aprendan identifcar solo 1 de los dos. Esto no es la solucion de mi problema.

---

### **Modelo definitivo red neuronal**

Finalmete uso una red neuronal que prioriza accuracy y AUC-ROC. (Red neuronal_def.ipynb en carpeta notebook dispute y y el modelo_dispute_red.keras utiliza el preprocesado preprocesador_red.pkl")

He tenido que guardar el preprocesador y el modelo por separado porque no conseguia meterlo todo en una pipeline
He usado un oversapler adasyn, ya que parece que mejora los estadisticos ligeramente frente a smote(0,85 vs 0,82 de accuracy)

Las variabbles que se han usado son:
* Product
* Sub-product
* Issue
* Sub-issue
* State
* Company response
* Timely response?
* weekday
* Company

Las variables tienen un preprocesado onehot (preprocesador_red.pkl en src)

500 epoch, batch 64 validation split

* input
* hidden layer x4 256, 128, 64 32
    * relu l2 0,001
    * batch normalizaion
    * dropoutr
* Salida sigmoidea
early stopping 20
ReduceLROnPlateau
tarda 24 s en entrenar

se m¡puede mejorar usando otras arquitecturas
Dificil de interpretar por muchas features

## APPS de gradio
en la carpeta de app se usaran las v4
* v1 prototipo
* v2 prototipo con modelos mas avanzados (basicamente v3 con los modelos que se usaron en v4)
* v3 prototipo con otros modelos que no se acabarosn usando
* v4 mejora de json, ahora da mas info
Se hiciero dos apps (uno pata timely response y otro para el otro)uno para cada modelo.
Estas apps tienen precticamente el mismo front end. con un scroll con todas los opciones categoricas (sacadas de los encoder de la carpeta src)

Por debajo pasan a df
* Timely pasa todo a label y predidce de alli
* dispute soporta el texto con el preprocesador ademas devuelve la probabilidad y
Por debajo utiliza lo mismo que la API pero tienen condificarla por debajo ya que timely no lo hace de base y el modelo de company response depende de este. Solo en la de timely.


Tuve muchos problemas con gradio ya que gradio asigna las variables en orden de aparicion sin importar el nombre. Afortunadamente pude solucionarlo  y se puede meter valores por defecto.
Si no se da timely response lo predice y da los reslutado
    Devuelve:
        "response":Yes/No
        "response01": 1/0
        "prob": %
        timely:
            "response":Yes/No
            "response01": 1/0
            "prob": %



## API
La API la realice antes de las primeras apps. 

el nb de api son pruebas para comprobar el buen funcionamiento de las funciones de forma mas sencilla, pero no es el entorno 1:1 porque en el archivo main da errores distintos
Ambas implementaciones las hice antes de tener los modelos definivos, mas como una prueba de concepto solo tener que cambiar el modelo definivo cuando este listo.

Archivo main.py en carpeta app 
Se monto una API con tres funciones:
* Una funcion de prueba que que funciona la API
* Una funcion que llama el modelo de timely
* Una funcion que llama el modelo de company response:
    * tiene la opcion de meter manualmente timely se si no se conoce pero si llamara el modelo timely y lo calculara.
Las predicciones devuelven
* response: Yes/No
* response01: 1/0
* prob: %

El threshol para la decision es de 0.5.
Utiliza fast API, y solo corre en la maquina que lo ejecute, y realmente todo esto sobra ya que las apps ya tienen opcion de integracion de API. 

Todos ellos cogen ID directamente por lo que es necesario codificar las variables antes de usarlo. Esto resulta mas comodo para el uso de la API que poner el valor completo
PAra utilizar API en necesario consultar la documentacion de la API especifica. Pero en resumen hay que introducr la numeros correspondientes de los label encoders del tool preprocess en src. consultar el ID.md.
El modelo de dispute necesita decodificarlo por debajo porque tiene una pipeline integrada y utliza onehot encoding lo que obliga

Para activar la API activar el entorno virtual y activar terminal y meter fastapi dev main.py.

Se va ha dejar de soportar el 22/8/2025 por falta de tiempo si se quiere API gradio lo soporta





## Cosas que hacer en el futuro

encontrar umbral
predecir company respone? (no haria esto para casos reales)