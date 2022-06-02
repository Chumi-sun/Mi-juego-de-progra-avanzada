# Tarea 2: DCComando Espacial


## Consideraciones generales

La tarea hace todo lo que pide el enunciado excepto por los bonus. No hice ninguno de estos. También revisé y ninguna linea tiene más de 100 caractéres, (sin contar este README).
Un error que puede suceder es uno que me sucedió de forma muy infrecuente al testear.
Y es que si es que se mata a los dos últimos aliens de un nivel con una sola bala hay una baja probabilidad de que el juego crashee.
Mi teoría de por qué esto sucede es debido a que las 2 threads de explosión de los aliens inician muy cerca. Sin embargo como sucedió tan pocas veces,
me fue imposible debuggearlo de forma definitiva. Hice un cambio y luego no volvió a pasar, pero como es tan poco frecuente,
no podría asegurar que realmente lo solucioné. Y el último error del que estoy consiente es de la reproducción del sonido de disparo.
Por algún motivo que escapa de mi compresión al reproducirlo se pausa todo el juego, por eso le puse un if True antes para que lo desactives si te es incomodo (porque para mí lo es). Está en la linea 181 de lógica_juego.py.

Ah sí, cuando se gana el nivel, todos los aliens derrotados vuelven a explotar. Esto no es un error. Simplemente creí que se veía bacán. Me hubiera ahorrado varios problemas y horas por no implementarlo.
Pero quería que hubieran fuegos artificiales.

También puede que mi diseño de frontend y backend no sea el ideal. Particularmente siento que en mi ventana de juego delegué mucho procesamiento.

### Cosas implementadas y no implementadas

#### Ventana de Inicio: 4 pts (4%)
#### Ventana de Ranking: 5 pts (5%)
#### Ventana principal: 7 pts (7%)
#### Ventana de juego: 14 pts (13%)
#### Ventana de post-nivel: 5 pts (5%)
#### Mecánicas de juego: 47 pts (45%)
##### ✅ Arma <Todo bien aquí>
##### ✅ Aliens y Escenario de Juego <Todo bien aquí>
##### ✅ Fin de Nivel <Todo bien aquí>
##### ✅ Fin del juego <Todo bien aquí>
#### Cheatcodes: 8 pts (8%)
##### ✅ Pausa <Todo bien aquí>
##### ✅ O + V+ N + I <Todo bien aquí>
##### ✅  C + I + A <Todo bien aquí>
#### General: 14 pts (13%)
##### ✅ Modularización <Todo bien aquí>
##### ✅ Modelación <Todo bien aquí>
##### ✅ Archivos  <Todo bien aquí>
##### 🟠 Parametros.py <parametricé todo lo que pedían y un par de cosas más. Sin embargo no sé si parametricé todo lo necesario, porque honestamente no cacho.>
#### Bonus: 10 décimas máximo
##### ❌ Risa Dog 
##### ❌ Estrella 
##### ❌ Disparos extra
##### ❌ Bomba

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```DCComando Espacial.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```puntajes.txt``` en ```T2```
2. ```Sprites``` en ```T2```
3. ```Sonidos``` en ```T2```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```: ```no creo que esto requiera mucha explicación``` (debe instalarse)
2. ```math```: ```ceil```
3. ```random```: ```uniform, shuffle, sample```
4. ```time```: ```sleep```
5. ```os```
6. ```sys```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```backend```: Contiene a ```logica_juego.py```, ```logica_post_juego.py```, ```logica_principal.py```, ```logica_rankings.py``` y ```threads_juego.py```. Todas las lógicas se encargan de procesar información de sus respectivas ventana y el modulo de threas contiene todos los objetos, como el perro, los aliens o el sonido de disparo que requieran threads. Todos los módulos de lógica por su parte poseen una única clase, la cual tiene el mismo nombre del módulo.



2. ```frontend```: Contiene todas las ventanas ```ventana_inicio.py```, ```ventana_juego.py```, ```ventana_post_juego.py```, ```ventana_principal.py``` y ```ventana_rankings.py```. Opino que los nombres explican lo que son. Todas contienen una única clase de QWidget con el mismo nombre.

3. ```Extras```: Contiene un único png hecho por mí que se utiliza en la ventana de juego.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Ninguno