
# Ollama Flask Project

Este repositorio contiene una aplicación desarrollada con Flask que incluye un entorno Dockerizado para facilitar su despliegue y ejecución.

## Contenido del Proyecto

- `app.py`: Archivo principal de la aplicación Flask, donde se configura la lógica principal de la aplicación.
- `clean.sh`: Script para limpiar archivos o datos temporales del proyecto.
- `deploy.py`: Archivo para el despliegue de la aplicación, configurado para facilitar el despliegue automático o en servidores.
- `docker-compose.yml`: Archivo de configuración de Docker Compose para levantar los servicios necesarios para la aplicación.
- `Dockerfile`: Instrucciones para crear la imagen Docker de la aplicación, lo que permite una configuración rápida y consistente en cualquier entorno.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar la aplicación Flask.
- `static`: Carpeta que contiene los archivos estáticos (CSS, JavaScript, imágenes) utilizados en la aplicación.
- `templates`: Carpeta con las plantillas HTML para la aplicación Flask.

## Requisitos Previos

- **Docker** y **Docker Compose**: Para ejecutar la aplicación en un contenedor.
- **Python 3**: Para ejecutar y desarrollar la aplicación localmente.

## Instalación y Configuración

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/ollama-flask.git
   cd ollama-flask
   ```

2. **Instala las dependencias**:
   Si deseas ejecutar la aplicación localmente sin Docker, instala las dependencias con:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Ejecutar con Docker

1. Asegúrate de tener Docker y Docker Compose instalados.
2. Ejecuta el siguiente comando para levantar los servicios:
   ```bash
   docker-compose up --build
   ```

### Ejecutar Localmente

Si prefieres ejecutar la aplicación localmente sin Docker:

1. Asegúrate de tener un entorno virtual activo (opcional, pero recomendado).
2. Ejecuta la aplicación Flask:
   ```bash
   python app.py
   ```

### Desplegar la Aplicación

Para desplegar la aplicación, puedes usar el archivo `deploy.py`, que contiene configuraciones específicas para el entorno de despliegue.

## Limpiar el Proyecto

Para limpiar archivos o datos temporales, puedes usar el script `clean.sh`:

```bash
bash clean.sh
```

## Estructura de Carpetas

- **static/**: Archivos estáticos como CSS, JavaScript e imágenes.
- **templates/**: Archivos HTML utilizados como plantillas en la aplicación.

## Contribuciones

Si deseas contribuir a este proyecto, por favor realiza un fork del repositorio y envía un pull request con tus cambios.

## Licencia

Este proyecto está licenciado bajo la licencia MIT.
