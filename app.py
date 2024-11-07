from flask import Flask, request, jsonify, render_template
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage, AIMessage
import os
import requests

app = Flask(__name__)

ollama_url = os.environ.get('OLLAMA_URL', 'http://ollama-container:11434')
default_model = "phi3:mini"

def get_available_models():
    try:
        response = requests.get(f"{ollama_url}/api/tags")
        if response.status_code == 200:
            return [model['name'] for model in response.json()['models']]
        else:
            print(f"Error al obtener modelos: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al conectar con Ollama: {e}")
        return []

def initialize_llm(model_name):
    try:
        return Ollama(model=model_name, base_url=ollama_url)
    except Exception as e:
        print(f"Error al inicializar el modelo {model_name}: {e}")
        return None

llm = initialize_llm(default_model)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['prompt']
    model_name = data.get('model', default_model)
    
    global llm, conversation
    if llm is None or llm.model != model_name:
        llm = initialize_llm(model_name)
        if llm is None:
            return jsonify({'error': f"No se pudo inicializar el modelo {model_name}"}), 500
        conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
    
    try:
        response = conversation.predict(input=user_message)
        
        # Convertir el historial de mensajes a un formato serializable
        serializable_history = []
        for message in memory.chat_memory.messages:
            if isinstance(message, HumanMessage):
                serializable_history.append({"role": "human", "content": message.content})
            elif isinstance(message, AIMessage):
                serializable_history.append({"role": "ai", "content": message.content})
        
        return jsonify({
            'response': response,
            'history': serializable_history
        })
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    global memory, conversation
    memory = ConversationBufferMemory()
    conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
    return jsonify({'status': 'success', 'message': 'Conversation reset'})

@app.route('/models', methods=['GET'])
def get_models():
    models = get_available_models()
    return jsonify({'models': models})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)