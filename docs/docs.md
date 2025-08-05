# DOCUMENTACION

## Objetivo del proyecto

Se pretende estimar primero la si la respuesta a tiempo (algo que aparentemente fue bastante facil y solo se realizo un modelo) y luego usar este dadot para estimar la si el cliente disputo o no. 
Tras esto se pretende utilizar ambos modelose introducirlos o en una API de fast api o en una app de gradio (aunque finalmente e han hecho 2 una para cada modelo porque no se me ocurrio como meterlo en el mismo). 


## Fuente de Datos y resumen de EDA
 en carpeta data
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
    Se añade la etiqueta "Unknown or not speficied"    
     
* **Sub-product**: DEstro de un producto la parte concreta. La mayoria esta vacia. Solo los 'Debt collection', 'Mortgage', 'Consumer loan',
       'Bank account or service', 'Money transfers', 'Student loan',
       'Prepaid card', 'Other financial servicetienen subproductos. "Debt collection" tambien tiene alguna queja en la que no tiene subproducto.
       Se añade la etiqueta "Unlnow or not speficied"  
 El resto to tiene subproducto.(Ver celda de mas abajo)
* **Issue**	: Hay 90 categorias Auque creo que alguna esta repetida (mirar mas abajo para detalles)
* **Sub-issue**	:Solo 'Debt collection', 'Credit reporting' tienen esto y hay 47 distintas (mirar mas abajo para detalles). El resto es una categoria vacia. Se rellenara con una etiquta 
* **State**	: Son los 50 estados de EEUU, otros territorios controlados por el(	Puerto Rico, Islas Vírgenes, Guam, Samoa Americana, Islas Marshall, Palaos ) y dos designagiones militares (AE es europea, y AP del pacifico). Hay valores faltantes. Algunos de estos si que tienen codigo Zip.  Se va a ñadir el estado unknown y se intentara sacarSe usara label encoder debido a que solo hay unos 60 distintos
* **ZIP code**: Hay varias que que no tienen estado pero si postal. Se podria intentar sacar el estado e  ignorar esta variable para evitar problemas de prvaciad. Se usara laber encoder debido a que solo hay unos 60 distintos

* **Date received**	: Fecha que llego
* **Date sent to company**	:Fecha que llego a la compañia parece que en todos los casos llega y se recibe el mismo dia. Hay menos en fin de semana y no hay festivos.
Estos datos no son muy utiles a pesar de que se saco en los dias laborales (que son todos) y los dias de retraso(que no tiene ya que los dias no tiene).

    * dias de retraso: inutil porque parece que en todos es 0 no se pondra
    * weekday  a lo mejor el dia de la semana tiene importancia       
    * holiday lo  mismo

* **Company**:hay como 1500 y siemmpre hay. No parece importante. Ya que coeficiente de cramer para Consumer disputed? es de 0,188. los cual no es muy alto, sobre todo si tinemos en cuenta que hay 1500 que darian problemas para codificarlos en one hot. P.D.  timely tiene cramer de 0.732  on esto lo que aloemtos. Al mejors


* **Company response**:	Siempre tiene y son:
    * 'In progress' 
    * 'Closed with explanation'
    * 'Closed with non-monetary relief'
    * 'Closed'
    * 'Closed with monetary relief'
    * 'Untimely response'
    Un label encoder es adecuado. Esta b¡muy desbalanceado con 'Closed with explanation' siendo el mas frecuente
* **Timely response?**: Solo contiene Si y no. Pero solo hay como 700 quejas que no se han respondido a tiempo.  P.D.  timely tiene cramer de 0.732  on esto lo que aloemtos.
* **Consumer disputed?**:estan si , no, y nan. Desbalanceado. La inmensa mayoria es NaN. las que estan in progress tiene sentido ( posiblemente se rellene con la categoria in progress) pero en el resto no se sabe como intrepretarlo.

---
* La disputa del consumidor parece presionar a las empresas a dar explicaciones más detalladas, aunque no necesariamente mejora la probabilidad de recibir un alivio.

* En cambio, cuando el consumidor no disputa, es más común que haya habido alguna forma de compensación (sobre todo no monetaria).





## Modelos de timely response?

Para el modelo se elimianron la columna de compañia, y la respuesta de compañia in progress, Complaint ID,  Consumer disputed?, ZIP code,Date received, Date sent to company. No se metio feature engineering.
Se metio resampleo con ADASYN.
El modelo es un decision tree al que se optimizo con grid search buscando maxima accuracy. 



Se metio: criterion='entropy', max_depth=30, random_state=24.


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

Se considero el modelo como suficiente ya que este no es el modelo principal, y se urilizara el metodo los siguientes modelos. Si que se intento utilizar un modelo SVC pero no pudo terminar tras una 2 h de procesamiento.



| Nº | Característica   | Importancia |
| -- | ---------------- | ----------- |
| 5  | Company response | 0.3569      |
| 4  | State            | 0.1859      |
| 3  | Sub-issue        | 0.1505      |
| 0  | Product          | 0.1166      |
| 1  | Sub-product      | 0.1096      |
| 2  | Issue            | 0.0805      |

Este modelo tiene dos problemas:

* Realmente este modelo "hace trampas" ya que el factor mas importante es company response. Company respone dice si esta cerrado o si a tenido timely response asi que en cierta manera el modelo ya tiene el target incorporado
* La mera existendia de Company response como feature no tiene sentido fisico ya que para cuando la empresa sepa como responder no tiene importancia.


esta el modelo esta en models y se llama modelo_timely_tree_def.pkl .
## Modelo de timely response


## API

Se monto una API con tres funciones:
* Una funcion de prueba que que funciona la API
* Una funcion que llama el modelo de timely
A p
* Una funcion que llama el modelo de company response:
     tiene la opcion de meter manualmente timely se si se conoce pero si llamara el modelo timely.

Utiliza fast API para esto

PAra utilizar API en necesario consultar la documentacion de la API especifica. pero en resumen hay que introducr la numeros correspondientes de los label encoders del tool preprocess en src.

## APPS de gradio

Se hiciero dos apps uno para cada modelo.
Estas apps tienen precticamente el mismo front end. con u scroll con todas los opciones.
Por debajo utiliza lo mismo que la API pero codifican con los encoders
