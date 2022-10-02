# Tests

Para crear los archivos se puede usar.
```
truncate -s 100K 100.o
truncate -s 1M 1.o
truncate -s 5M 5.o
```

Iniciar el servidor (usa configuración default, `localhost`, puerto `12000`, destino `./storage`, muestra `error` e `info`)
```
python3 src/start-server.py
```

## Subir archivos


En el cliente (usa configuración default, `localhost`, puerto `12000`, muestra `error` e `info`).
Para probar el multithreading se pueden correr en simultaneo.

```
## Stop and Wait
python3 src/upload.py -n 100.o -saw -s .
python3 src/upload.py -n 1.o -saw -s .
python3 src/upload.py -n 5.o -saw -s .

```

Se pisan los archivos anteriores en el servidor.
```
## GBN
python3 src/upload.py -n 100.o -s .
python3 src/upload.py -n 1.o -s .
python3 src/upload.py -n 5.o -s .
```

## Descarga de archivos


En el cliente (usa configuración default, `localhost`, puerto `12000`, muestra `error` e `info`).
Para probar el multithreading se pueden correr en simultaneo.
Tienen que estar en `./storage` los archivos subidos en la prueba anterior

```
## Stop and Wait
python3 src/download.py -n 100.o -saw -d download
python3 src/download.py -n 1.o -saw -d download
python3 src/download.py -n 5.o -saw -d download

```

Se pisan los archivos anteriores en el servidor.
```
## GBN
python3 src/download.py -n 100.o -d download
python3 src/download.py -n 1.o -d download
python3 src/download.py -n 5.o -d download
```

### Descarga de archivo inexistente

```
python3 src/download.py -n inexistente.o -d download
```