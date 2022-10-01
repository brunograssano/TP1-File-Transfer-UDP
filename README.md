# TP1-File-Transfer-UDP

Trabajo Práctico I - Introducción a los Sistemas Distribuidos - FIUBA
## Introducción
El presente trabajo práctico tiene como objetivo la creación de una aplicación de red que transfiera archivos entre cliente-servidor. 
Para tal finalidad, será necesario comprender cómo se comunican los procesos a través de la red, y cuál es el modelo de servicio que la capa de transporte le ofrece a la capa de aplicación.
Además, para poder lograr el objetivo planteado, se aprenderá el uso de la interfaz de sockets y los principios básicos de la transferencia de datos confiable.

## Integrantes

| Nombre                                                        | Padrón |
| ------------------------------------------------------------- | ------ |
| [Gomez, Joaquin](https://github.com/joaqogomez)               | 103735 |
| [Grassano, Bruno](https://github.com/brunograssano)           | 103855 |
| [Opizzi, Juan Cruz](https://github.com/JuanOpizzi)            | 99807  |
| [Stancanelli, Guillermo](https://github.com/guillermo-st)     | 104244 |
| [Valdez, Santiago](https://github.com/SantiValdezUlzurrun)    | 103785 |

## Sistemas Operativos Compatibles y Versiones de Python Compatibles
* Las aplicaciones fueron ejecutadas en versiones de `Python` `3.8`, `3.9.X` y `3.10`

## Instrucciones de Ejecución

### Archivo de Configuración Default

Al final del archivo src/lib/constants.py se encuentra una serie de constantes de configuración por default que puede ser modificada. Por ejemplo, esto incluye tiempos de timeout y numero de intentos por conexion.

Por defecto las aplicaciones estan configuradas para utilizar `localhost` y el puerto `12000`.

### Logging
Todas las aplicaciones ofrecen tres modos de log, `quiet`, `verbose`, y por defecto.
* `quiet`: Muestra solo mensajes de error
* `verbose`: Muestra mensajes de error, info, debug
* Por defecto muestra mensajes de error e info

Estos mensajes son impresos por pantalla y agregados a su correspondiente archivo.

#### start-server.py

```
python3 src/start-server.py -h
usage: start-server.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-s STORAGE]

description: Starts the server

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -q, --quiet           decrease output verbosity
  -H ADDR, --host ADDR  server IP address
  -p PORT, --port PORT  server port
  -s STORAGE, --storage STORAGE
                        specify the storage path
```

Inicia un servidor, si no se indica el `storage` se guardará en `/storage` 

#### download_file.py

```
python3 src/download_file.py -h
usage: download_file.py [-h] [-v | -q] [-saw | -gbn GO_BACK_N] [-H ADDR] [-p PORT] [-d FILEPATH] [-n FILENAME]

description: Downloads a specific file from the server

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -q, --quiet           decrease output verbosity
  -saw, --stop_and_wait
                        choose stop and wait transfer
  -gbn GO_BACK_N, --go_back_n GO_BACK_N
                        choose go back N transfer
  -H ADDR, --host ADDR  server IP address
  -p PORT, --port PORT  server port
  -d FILEPATH, --dst FILEPATH
                        destination file path
  -n FILENAME, --name FILENAME
                        file name
```

Este programa permite descargar un archivo del servidor. Es necesario indicar el nombre del archivo (`file name`)

Se permite no incluir la direccion, el puerto, y la dirección `dst` (Guarda en `.`).

#### upload.py

```
python3 src/upload.py -h

usage: upload.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-saw | -gbn GO_BACK_N] [-s FILEPATH]
                 [-n FILENAME]

description: Uploads a file to the server

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -q, --quiet           decrease output verbosity
  -H ADDR, --host ADDR  server IP address
  -p PORT, --port PORT  server port
  -saw, --stop_and_wait
                        choose Stop and Wait transfer
  -gbn GO_BACK_N, --go_back_n GO_BACK_N
                        choose Go Back N transfer
  -s FILEPATH, --src FILEPATH
                        source file path
  -n FILENAME, --name FILENAME
                        file name
```


Este programa permite al usuario subir un nuevo archivo al servidor, en caso de que ya exista será remplazado. . Es necesario indicar el nombre del archivo (`file name`)

Se permite no incluir la direccion, el puerto, y la dirección `src` (Busca en `.`).
