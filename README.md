# TP1-File-Transfer-UDP



## download_file.py

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