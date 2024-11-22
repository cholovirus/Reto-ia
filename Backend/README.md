# Chat API - Backend

Este es el backend de una API de chat que utiliza técnicas de recuperación de información junto con modelos de lenguaje para generar respuestas personalizadas basadas en datos de noticias.

## Funciones y Clases backend.py

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

---

## Funciones y Clases pre_procesamiento.py

- **Verificación de GPU**: El código verifica si hay una GPU disponible para acelerar los cálculos utilizando `torch`. Si no está disponible, se usa la CPU.
  - Usa `torch.cuda.is_available()` para comprobar la disponibilidad de la GPU.

- **Carga y procesamiento de datos**: Se carga un archivo de Excel con `pandas`, se limpia y ajusta:
  - Se elimina la primera columna del archivo.
  - Se rellenan valores faltantes en las columnas numéricas con 0.
  - Se convierte la columna "Fecha" a tipo de dato `str` para su correcto manejo.

- **Generación de embeddings**: Utiliza el modelo de embeddings `sentence-transformers/all-MiniLM-L6-v2` para transformar las descripciones de las noticias ("Acontecimiento") en vectores.
  - Los embeddings se generan usando el dispositivo (GPU o CPU) disponible.

- **Creación y almacenamiento en base de datos**:
  - Se crea una colección en `chromadb` (si no existe) para almacenar las descripciones de noticias junto con sus metadatos y embeddings generados.
  - Se agrega cada documento con sus embeddings y metadatos a la colección.
