# Práctica con Licitaciones: RAG-Powered Conversational Analyzer

Una API en **FastAPI** que combina LangChain, ChromaDB y OpenAI para ofrecer un **chat conversacional** con RAG (Retrieval-Augmented Generation) sobre documentos de licitaciones en PDF.

> 🏆 **MVP de hackathon**

---

## 🚀 Características

* **Indexado offline** de múltiples licitaciones (PDF) en un vector-store.
* **Chunking inteligente** con `RecursiveCharacterTextSplitter`.
* **Vector-store** persistente utilizando ChromaDB.
* **Conversational RAG** mediante `ConversationalRetrievalChain` de LangChain.
* **Memoria de diálogo** para mantener el contexto entre turnos de chat.
* **Metadata & trazabilidad**: cada fragmento indexado incluye nombre de archivo, página y chunk\_id. *(Pendiente de implementación completa)*
* **API REST** con un único endpoint `POST /chat`.

---

## 📦 Prerrequisitos

* Python 3.10 o superior
* Clave de API de OpenAI
* (Opcional) Docker y Docker Hub

---

## 🔧 Instalación y configuración

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu-org/hackia-licita.git
   cd hackia-licita/backend
   ```

2. **Crear y activar el entorno virtual**

   ```bash
   python3 -m venv .venv

   # macOS / Linux
   source .venv/bin/activate

   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   Copia `.env.example` a `.env` y edita:

   ```ini
   OPENAI_API_KEY=sk-...
   CHROMA_PERSIST=.chromadb
   ```

---

## 📁 Estructura del proyecto

```plaintext
backend/
├── docs/                  # Licitaciones (PDF/TXT)
│   ├── ejemplo1.pdf
│   └── ejemplo2.pdf
├── .chromadb/             # Vector-store de ChromaDB (generado)
├── .env                   # Variables sensibles (no versionar)
├── model_clf.pkl          # (Opcional) Clasificador supervisado
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Documentación principal
└── src/                   # Código fuente
    ├── __init__.py
    ├── config.py         # Carga de variables de entorno
    ├── ingestion.py      # Indexación de documentos en ChromaDB
    ├── chain.py          # Definición del RAG-Chat chain
    ├── main.py           # FastAPI: expone `POST /chat`
    └── train_classifier.py  # (Opcional) Entrenamiento del clasificador
```

---

## ⚙️ Flujo de trabajo

### 1. Indexación

Antes de levantar la API, indexa todos los documentos:

```bash
python -m src.ingestion
```

**Salida esperada:**

```text
🔍 Buscando archivos en: backend/docs
▶️ Cargando ejemplo1.pdf
▶️ Cargando ejemplo2.pdf
✂️ Fragmentos creados: 24
✅ Indexados 24 fragmentos de 2 archivos.
```

### 2. (NO IMPLEMENTADO) Entrenamiento del clasificador

Para generar un modelo supervisado de scoring de riesgo:

```bash
python -m src.train_classifier
```

Se creará el archivo `model_clf.pkl` en la raíz.

### 3. Levantar la API

```bash
uvicorn src.main:app --reload
```

* Swagger UI: `http://127.0.0.1:8000/docs`

### 4. Probar el chat

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"¿Qué penalizaciones hay por retrasos?"}'
```

**Respuesta de ejemplo:**

```json
{
  "answer": "El contrato establece una penalización de 0.5% del valor diario por día de retraso en la entrega de luminarias.",
  "sources": ["ejemplo1.pdf"]
}
```

---

## 🛠️ Detalles de implementación

* **`ingestion.py`**:

  * Usa `RecursiveCharacterTextSplitter` para generar chunks de \~500 caracteres.
  * Inyecta metadata (`source`, `page`, `chunk_id`).
  * Indexa los fragments en ChromaDB.

* **`chain.py`**:

  * Configura `OpenAIEmbeddings` + Chroma retriever (`search_kwargs={"k":4}`).
  * Define `ChatOpenAI(model_name="gpt-4o-mini")`.
  * Construye `ConversationalRetrievalChain.from_llm(...)` con memoria (solo guarda `output_key="answer"`).

* **`main.py`**:

  * Esquemas Pydantic: `ChatReq` y `ChatRes(answer: str, sources: List[str])`.
  * Un único endpoint `POST /chat`.

---

## 📑 Contribuciones

1. Haz **fork** de este repositorio.
2. Crea una rama para tu mejora:

   ```bash
   ```

git checkout -b feature/mi-mejora

```
3. Añade tests y documentación si es necesario.  
4. Abre un **Pull Request** describiendo tu aporte.

```


