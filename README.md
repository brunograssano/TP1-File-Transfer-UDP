# TP1-File-Transfer-UDP



## download_file.py

```
python download_file.py -h
usage: download_file.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-d FILEPATH] [-n FILENAME]

description: Downloads a specific file from the server

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -q, --quiet           decrease output verbosity
  -H ADDR, --host ADDR  server IP address
  -p PORT, --port PORT  server port
  -d FILEPATH, --dst FILEPATH
                        destination file path
  -n FILENAME, --name FILENAME
                        file name
```

download_file permite descargar un archivo del servidor, en caso de que éste esté corriendo. Para lograr esto se debe especificar la dirección del servidor, el puerto al cual conectarse y un archivo.
Opcionalmente, se puede elegir una carpeta destino para guardar el archivo donde se desee. El programa además soporta 3 modos de salida: silenciosa, normal y verbosa.