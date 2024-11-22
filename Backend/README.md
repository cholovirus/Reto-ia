# Chat API - Backend

Este es el backend de una API de chat que utiliza técnicas de recuperación de información junto con modelos de lenguaje para generar respuestas personalizadas basadas en datos de noticias.

## Funciones y Clases

- **`Message`**: Define la estructura de un mensaje en el chat. Tiene dos campos:
  - `role`: El rol del remitente del mensaje (ej. "usuario", "sistema").
  - `content`: El contenido del mensaje.

- **`ChatRequest`**: Contiene los datos necesarios para una solicitud de chat:
  - `messages`: Una lista de objetos `Message` que representan la conversación.
  - `model`: El modelo de lenguaje a utilizar para la generación de respuestas.
  - `temperature`: Controla la aleatoriedad de las respuestas generadas.

- **`clean_text(prompt)`**: Función que limpia el texto de entrada:
  - Elimina caracteres especiales y palabras vacías en español.
  - Devuelve una estructura de consulta compatible con la base de datos.

- **`recuperacion(query)`**: Recupera información relevante desde una base de datos de noticias utilizando `chromadb`:
  - Utiliza un modelo de embeddings (Hugging Face) para transformar la consulta en un vector y buscar documentos relevantes.
  - Devuelve los documentos encontrados junto con sus metadatos.

- **`chat(request: ChatRequest)`**: Función principal que maneja la solicitud de chat:
  - Recibe una solicitud `ChatRequest`, procesa el mensaje del usuario, y recupera el contexto relevante.
  - Si se encuentra información relevante, la agrega al mensaje de la respuesta. De lo contrario, indica que no se encontraron noticias relacionadas.
  - Llama a un modelo de OpenAI (o modelo local) para generar una respuesta final y la retorna al usuario.
