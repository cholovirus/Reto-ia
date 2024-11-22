import chromadb
import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain_chroma import Chroma
from chromadb.config import Settings

import torch

if torch.cuda.is_available():
    print("GPU está disponible.")
else:
    print("GPU no está disponible, se está usando CPU.")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
file_path = "bd_conocimiento.xlsx"
df = pd.read_excel(file_path)
df = df.drop(df.columns[0], axis=1)
df.iloc[:, 10:] = df.iloc[:, 10:].fillna(0)
df_new = df.iloc[:, 10:].fillna(0)
df["Fecha"] = df["Fecha"].astype(str)
# Verificar los datos

column_names = df.columns.tolist()
column_names.remove("Acontecimiento")
metadatas = df[column_names].to_dict(orient="records")



embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": device})
print("start")
embeddings = embedding_model.embed_documents(df["Acontecimiento"].tolist())
print("end")

persist_directory = "./db"  # Especifica la ruta donde se almacenarán los datos
client = chromadb.PersistentClient(path=persist_directory)

collection_name = "news_ayacucho"

# Verificar si la colección existe
try:
    collection = client.get_collection(collection_name)
    print(f"Conectado a la colección existente: {collection_name}")
except Exception:
    # Crear la colección si no existe
    collection = client.create_collection(collection_name)
    print(f"Se creó la colección: {collection_name}")


collection.add(
    documents=df["Acontecimiento"].tolist(),  # Las descripciones de las noticias
    metadatas=metadatas,  # Los metadatos asociados (información adicional sobre cada noticia)
    embeddings=embeddings,  # Los embeddings generados para cada descripción
    ids=[str(i) for i in range(len(embeddings))]  # IDs únicos para cada fila
)

