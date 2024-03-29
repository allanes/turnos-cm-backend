# turnos-cm-backend

Este es el backend de la aplicación de turnos "turnos-cm". Siga estas instrucciones para instalar y configurar el backend en su sistema.

## Requisitos

- Sistema operativo Windows o Linux
- Python 3.6 o posterior

## Instalación

Para instalar el backend en su sistema, siga estos pasos:

1. Abra una ventana de comandos y vaya al directorio raíz del backend ejecutando el siguiente comando:
    ```    
    cd turnos-cm-backend
    ```

2. Cree un entorno virtual de Python e instale las dependencias necesarias ejecutando los siguientes comandos:
    - Windows:
        ```    
        python3 -m venv .venv
        .venv\scripts\activate
        python -m pip install -U pip
        pip install -r requirements.txt
        ```
    - Linux:
        ```    
        python -m venv .venv
        source .venv/bin/activate
        python3 -m pip install -U pip
        pip install -r requirements.txt
        ```

## Actualización de la base de datos

Estos pasos se deben seguir si hubo cambios en los modelos de la db.

Para actualizar la base de datos (realizar migraciones), siga estos pasos:

1. Detenga el servicio backend.
2. Borre el archivo "database.db" ejecutando el siguiente comando:
    - Windows:
        ```
        del database.db
        ```
    - Linux:
        ```
        rm database.db
        ```
3. Borre el contenido de la carpeta "sql_app/alembic/versions" ejecutando el siguiente comando:
    - Windows:
        ```
        del /Q sql_app\alembic\versions\*.*
        ```
    - Linux:
        ```
        rm -r sql_app/alembic/versions/*
        ```
4. Vuelva a crear las revisiones de la base de datos ejecutando los siguientes comandos:
    ```
    cd sql_app
    alembic revision
    cd ..
    ```

## Inicio del servicio backend

Para iniciar el backend, ejecute el siguiente comando ***desde el entorno virtual***:
```
uvicorn main:app --reload
```

Luego, puede acceder a la documentación de la API en `http://localhost:8000/docs/`.


## Carga de datos iniciales

Para cargar datos iniciales en la base de datos ***vacía***, acceder a `http://localhost:8000/inicializar_db`.

## Carga de turnos del día

Si se desea usar la db, cada nuevo día se deben cargar turnos. Para cargar ejemplos del día, ir a `http://localhost:8000/cargar-turnos-ejemplo/`.

## Automatización

Para automatizar el inicio de los servicios de backend y frontend en el sistema operativo (Ubuntu):

1. Ejecutar el archivo `setup_services.sh` desde la carpeta:
    ```
    cd scripts
    sudo bash setup_services.sh
    ```

2. Sin maximizar, abrir chrome y arrastrarlo hacia la pantalla mas incómoda. 

3. Configurarlo para que abra por defecto la url de esa sala con todos los permisos necesarios.

4. Cerrarlo

5. Repetir pasos 3-5 con firefox.

6. Reiniciar y comprobar que los servicios se iniciaron automaticamente.

7. En las computadoras de administracion, crear un acceso directo a <http://{ip-servidor-backend}:8000/iniciar-vistas-teles>

## Abrir ventanas de televisores

Para abrir las vistas de los televisores de todas las salas, usar desde cualquier computadora el siguiente enlace:

    http://{ip-servidor-backend}:8000/iniciar-vistas-teles

NOTA: Revisar que en los televisores ya se vea el escritorio

## Exponer endpoint de medicos a internet

1. Opcionalmente se puede usar la integración de ngrok para exponer la vista de medicos a internet. Para eso, es necesario instalar nginx:

    ```
    sudo apt-get update
    sudo apt-get install nginx
    ```

2. Usar la carpeta ngrok_app para guardar la configuracion. Crear los siguientes archivos reemplazando el auth_token:

    - .env
        ```
        NGROK_AUTH_TOKEN=auth_token
        NGROK_SERVER_PORT=8001
        NGINX_REVERSE_PROXY_PORT=3006
        ```

    - ngrok.yml
        ```
        tunnels:
            tunel_cm_esperanza:
                proto: http
                hostname: cm-esperanza.ngrok.app
                host_header: rewrite
                bind_tls: true
        ```

3. Configurar NginX como servidor proxy inverso:

    ```
    sudo sh scripts/setup_nginx.sh
    ```