**Asistente de IA con Recuperación Aumentada por Generación (RAG)**

## **Objetivo**  
El objetivo de este proyecto es desarrollar un asistente de inteligencia artificial basado en técnicas de generación aumentada por recuperación (RAG). Este asistente está diseñado para procesar un archivo Excel como base de conocimiento y responder preguntas de los usuarios basándose en el contenido del archivo.  

El asistente es capaz de interpretar preguntas en lenguaje natural, recuperar información relevante del Excel y proporcionar respuestas precisas y contextualmente correctas. Además, el sistema registra todas las interacciones y preguntas de los usuarios en una base de datos para su seguimiento y análisis.  


## **Estructura del Proyecto**  

### **Frontend**  
El frontend utiliza **Streamlit** para proporcionar una interfaz interactiva donde los usuarios pueden cargar un archivo Excel, hacer preguntas y visualizar las respuestas del asistente.

#### **Tecnologías**  
- **Streamlit**: Framework para crear aplicaciones web interactivas en Python.
- **Requests**: Biblioteca para enviar solicitudes HTTP al backend.

#### **Características**  
- Los usuarios pueden hacer consultas en lenguaje natural sobre el contenido del archivo.
- Visualización en tiempo real de las respuestas generadas por el backend.
---
### **Backend**  
Este backend es el núcleo del asistente de inteligencia artificial basado en técnicas de Recuperación Aumentada por Generación (RAG). Está diseñado para procesar preguntas en lenguaje natural, recuperar información relevante de una base de datos vectorial (ChromaDB) y generar respuestas utilizando un modelo de lenguaje.  

El backend funciona como una API desarrollada con **FastAPI** y puede desplegarse de manera local o remota utilizando herramientas como **ngrok** para exposición pública. 

## **Características**  
- **Procesamiento de preguntas**: Interpreta consultas en lenguaje natural enviadas por el frontend.  
- **Recuperación de información**: Utiliza embeddings semánticos para buscar datos relevantes en ChromaDB.  
- **Generación de respuestas**: Integra un modelo generativo que proporciona respuestas precisas basadas en la consulta y la información recuperada.  
- **Preprocesamiento de texto**: Limpia y procesa las consultas para mejorar la precisión de la búsqueda.  

## **Tecnologías utilizadas**  
- **FastAPI**: Framework ligero y rápido para construir APIs.  
- **ChromaDB**: Base de datos vectorial para realizar consultas semánticas.  
- **HuggingFace Sentence Transformers**: Para generar embeddings de texto.  
- **NLTK**: Herramientas para preprocesar texto (eliminación de stopwords, limpieza, etc.).  
- **Torch**: Biblioteca utilizada para modelos de aprendizaje profundo.
- **LM Studio**: Aplicación de escritorio gratuita y de código abierto que permite ejecutar modelos de lenguaje grande (LLMs) localmente en tu PC.
---
# **Get Started**

Este proyecto consta de dos componentes principales: un **frontend** interactivo desarrollado con **Streamlit** y un **backend** implementado con **FastAPI**. A continuación, se detallan los pasos necesarios para configurar y ejecutar ambos.

## **Requisitos previos**  
1. **Python 3.9 o superior**  
2. Instalar las dependencias necesarias:  
   pip install -r requirements.txt
3. Ejecutar LM Studio, Activar la funcion de servidor y luego cargar el modelo LLM de su preferencia
4. Ejecutar "uvicorn backend:app --host 127.0.0.1 --port 8000"
5. Ejecutar "ngrok http 8000" (tener en cuenta tener el .exe de ngrok y colocar la llave)
6. Ejecutar "streamlit run front.py"
7. Colocar la URL de la api, en este caso la URL generada por ngrok
   ![image](https://github.com/user-attachments/assets/1806eb60-186c-4aab-864b-4e83c86bb6b2)

--- 
**Notas Adicionales**

Asegúrate de que las dependencias como nltk están configuradas correctamente. Por ejemplo, descarga los recursos necesarios:
- python -m nltk.downloader stopwords
