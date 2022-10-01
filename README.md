# TP1-File-Transfer-UDP

Trabajo Práctico I - Introducción a los Sistemas Distribuidos - FIUBA

## Integrantes

| Nombre                                                        | Padrón |
| ------------------------------------------------------------- | ------ |
| [Opizzi, Juan Cruz](https://github.com/JuanOpizzi)            | 99807  |
| [Gomez, Joaquin](https://github.com/joaqogomez)               | 103735 |
| [Grassano, Bruno](https://github.com/brunograssano)           | 103855 |
| [Stancanelli, Guillermo](https://github.com/guillermo-st)     | 104244 |
| [Valdez, Santiago](https://github.com/SantiValdezUlzurrun)    | 103785 |

## Sistemas Operativos Compatibles y Versiones de Python Compatibles

VER

## Instrucciones de Ejecucion

### Archivo de Configuración Default

Al final del archivo src/lib/constants.py se encuentra una serie de constantes de configuración por default que puede ser modificada. Por ejemplo, esto incluye tiempos de timeout y numero de intentos por conexion.

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

download_file permite descargar un archivo del servidor, en caso de que éste esté corriendo. Para lograr esto se debe especificar la dirección del servidor, el puerto al cual conectarse y un archivo.
Opcionalmente, se puede elegir una carpeta destino para guardar el archivo donde se desee. El programa además soporta 3 modos de salida: silenciosa, normal y verbosa.

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


Este programa permite al usuario subir un nuevo archivo al servidor. Para hacer esto, necesitará indicar la dirección y puerto del servidor. Se debe indicar el nombre del archivo, puede indicar la ruta del archivo, si no se indica, se asume que el archivo se encuentra en la carpeta principal del proyecto. En caso de no existir el archivo, el programa terminará sin efecto alguno.
