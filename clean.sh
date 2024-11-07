#!/bin/bash

echo "Iniciando limpieza específica para el proyecto Flask-Ollama..."

# Detener y eliminar contenedores usando docker-compose
echo "Deteniendo y eliminando contenedores..."
docker-compose down -v

# Eliminar imágenes específicas
echo "Eliminando imágenes específicas..."
docker rmi jose/ollama-flask:latest ollama/ollama:latest

# Eliminar redes específicas
echo "Eliminando red específica..."
docker network rm ollama-flask_app_network

# Eliminar volúmenes específicos
echo "Eliminando volúmenes específicos..."
docker volume rm ollama-flask_ollama_data

# Limpiar imágenes, contenedores y redes no utilizados
echo "Limpiando recursos no utilizados..."
docker system prune -f

echo "Limpieza específica completada."

# Verificar si quedan recursos
echo "Verificando recursos restantes..."

if [ -n "$(docker ps -a -q)" ]; then
    echo "Contenedores restantes:"
    docker ps -a
fi

if [ -n "$(docker images -q)" ]; then
    echo "Imágenes restantes:"
    docker images
fi

if [ -n "$(docker network ls --filter name=ollama-flask -q)" ]; then
    echo "Redes restantes:"
    docker network ls --filter name=ollama-flask
fi

if [ -n "$(docker volume ls --filter name=ollama-flask -q)" ]; then
    echo "Volúmenes restantes:"
    docker volume ls --filter name=ollama-flask
fi

echo "Verificación completada."
