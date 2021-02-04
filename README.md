# Chatbot infantil para Sonidos del Cielo

En este repositorio se recoge el código del chatbot para proyecto Sonidos del Cielo destinado a público infantil.

Para poder entrenar y arrancar el chatbot es necesario tener instalado:
- Python 
- Rasa

El código ha sido desarrollado y probado en una máquina virtual con sistema operativo Ubuntu 20.04.1 LTS que incluye por defecto Python 3.8. Por problemas de compatibilidad con las librerías que requiere Rasa, se utiliza un entorno virtual con Python 3.7. 

## Creación del entorno virtual:
Se recomienda seguir los siguientes pasos para crear el entorno virtual necesario. 

1. **Instalación de Python 3.7.0**

Python 3.7.0 disponible en: 
https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz

Si ya tienes una versión Python instalada:

- Actualiza e instala los paquetes necesarios para instalar el fuente de Python 3.7.0:

```
$ sudo apt update
$ sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev
```

- Descarga el código fuente de Python 3.7.0:
```
$ wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
```

- Extraer el archivo comprimido descargado:
```
$ tar -xf Python-3.7.0.tgz
```
- Hacer el build:
```
$ cd Python-3.7.0
$ ./configure --enable-optimizations
```
- Instalar la nueva versión de Python:
```
$ sudo make altinstall
```
2. **Creación y activación del entorno virtual**
```
$ python3.7 -m venv ./venv
$ source venv/bin/activate
```

3. **Instalación de Rasa**
Consulta la documentación de Rasa en:
https://rasa.com/docs/rasa/installation/

Los pasos seguidos en el desarrollo del proyecto fueron los siguientes:
```
$ pip3 install -U pip
$ pip3 install rasa
$ pip3 install rasa[full]
$ pip3 install rasa[spacy]
$ python3 -m spacy download es_core_news_md
$ python3 -m spacy link es_core_news_md es
```

## Entrenamiento

Para entrenar un nuevo modelo (si se realizan modificaciones en el código):
```
$ rasa train
```

Esto generará un nuevo fichero en el directorio /models

## Ejecución
Para poder utilizar el chatbot una vez entrenado habrá que lanzar el servidor.

Por un lado levantamos el servidor de acciones:
```
$ python -m rasa_sdk --actions actions
```
Por otro levantamos el servidor de Rasa con el modelo de NLU:
```
$ rasa run -m models --enable-api --cors “*” --debug --endpoints endpoint.yml
```

## Llamadas REST
Para utilizar el chatbot como según el modelo API REST se hace uso de la llamada POST a la URL http://localhost:5005/webhooks/rest/webhook

Ejemplo en Postman:
POST http://localhost:5005/webhooks/rest/webhook

Body (raw):
```
{"sender":"noe", "message":"hola"}
```
Este ejemplo devuelve a la llamada el siguiente JSON:
```
[
    {
        "recipient_id": "noe",
        "text": "¡Hola! Qué bien verte por el espacio, esto es Sonidos del Cielo,  el proyecto de Ciencia Ciudadana para la clasificación de meteoros a través de sus sonidos."
    },
    {
        "recipient_id": "noe",
        "text": "¿Qué te gustaría hacer, escuchar la explicación del juego o empezar a jugar?"
    }
]
```
