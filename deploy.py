import os
import subprocess
import sys
import time
import requests

# Definir la URL de la API de Ollama
OLLAMA_API_URL = os.environ.get('OLLAMA_API_URL', 'http://localhost:11434')

def run_command(command, show_output=True):
    print(f"\n----- Ejecutando: {command} -----")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        if show_output:
            print(line.strip(), flush=True)
    
    rc = process.wait()
    if rc != 0:
        print(f"Error ejecutando el comando: {command}")
        print(f"Código de salida: {rc}")
        return False
    return True

def check_docker_image(image_name):
    print(f"\nVerificando si la imagen {image_name} existe...")
    result = subprocess.run(["docker", "images", "-q", image_name], capture_output=True, text=True)
    exists = bool(result.stdout.strip())
    print(f"La imagen {image_name} {'existe' if exists else 'no existe'}.")
    return exists

def check_docker_container(container_name):
    print(f"\nVerificando si el contenedor {container_name} existe y está en ejecución...")
    result = subprocess.run(["docker", "ps", "-q", "-f", f"name={container_name}"], capture_output=True, text=True)
    running = bool(result.stdout.strip())
    if running:
        print(f"El contenedor {container_name} está en ejecución.")
    else:
        print(f"El contenedor {container_name} no está en ejecución o no existe.")
    return running

def check_required_files():
    required_files = ['Dockerfile', 'docker-compose.yml', 'app.py', 'requirements.txt']
    missing_files = [file for file in required_files if not os.path.exists(file)]
    if missing_files:
        print(f"Error: Los siguientes archivos requeridos no se encuentran en el directorio actual: {', '.join(missing_files)}")
        return False
    return True

def build_flask_image():
    if not check_required_files():
        print("No se puede construir la imagen de Flask debido a archivos faltantes.")
        sys.exit(1)

    print("\nConstruyendo la imagen de Flask...")
    if not run_command("docker build -t jose/ollama-flask ."):
        print("Error al construir la imagen de Flask.")
        sys.exit(1)
    print("Imagen de Flask construida exitosamente.")

def pull_ollama_image():
    if not check_docker_image("ollama/ollama"):
        print("\nDescargando la imagen de Ollama...")
        if not run_command("docker pull ollama/ollama"):
            print("Error al descargar la imagen de Ollama.")
            sys.exit(1)
    else:
        print("La imagen de Ollama ya existe. Omitiendo la descarga.")

def run_docker_compose():
    if not (check_docker_container("ollama-flask-ollama-container-1") and 
            check_docker_container("ollama-flask-flask-app-1")):
        print("\nIniciando los servicios con docker-compose...")
        if not run_command("docker-compose up -d"):
            print("Error al iniciar los servicios con docker-compose.")
            sys.exit(1)
        
        print("\nEsperando a que los servicios estén listos...")
        time.sleep(10)  # Espera 10 segundos para que los servicios se inicien completamente
    else:
        print("\nLos contenedores ya están en ejecución. Omitiendo docker-compose up.")

def download_llm_model():
    model = input("\nIntroduce el nombre del modelo LLM a descargar (por defecto 'phi3:mini'): ") or "phi3:mini"
    print(f"\nDescargando el modelo {model}...")
    
    api_url = f"{OLLAMA_API_URL}/api/pull"
    
    try:
        with requests.post(api_url, json={"name": model}, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    print(line.decode('utf-8'), flush=True)
        print(f"\nModelo {model} descargado exitosamente.")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el modelo {model}: {e}")
        sys.exit(1)

def main():
    print("=== Iniciando el proceso de configuración de Ollama y Flask ===")
    
    pull_ollama_image()
    build_flask_image()
    run_docker_compose()
    download_llm_model()

    print("\n=== Todos los pasos se han completado exitosamente ===")
    keep_resources = input("\n¿Deseas mantener los recursos creados? (s/n): ").lower() == 's'

    if not keep_resources:
        print("\nEliminando los recursos...")
        run_command("docker-compose down -v")
        run_command("docker rmi jose/ollama-flask ollama/ollama")
        print("Recursos eliminados.")
    else:
        print("\nLos recursos se mantendrán para futuras ejecuciones.")
    
    print("\n=== Proceso finalizado ===")

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    main()
