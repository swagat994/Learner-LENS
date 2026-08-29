# LectureLens

LectureLens is an AI-powered learning assistant designed to help students transform lecture material into structured study resources. The system supports lecture summarization, quiz generation, flashcard generation, study-plan generation, and question answering based on uploaded lecture material.

The project uses a locally hosted Llama 3.2 model through Ollama and a Retrieval-Augmented Generation (RAG) pipeline for lecture-based question answering.

---

## Features

* JWT-based authentication
* User management
* Course management
* PDF lecture upload
* PDF text extraction
* AI-powered lecture summarization
* AI-generated multiple-choice quizzes
* AI-generated flashcards
* AI-generated study plans
* Question answering based on uploaded lectures
* Retrieval-Augmented Generation (RAG)
* Local text embeddings
* ChromaDB vector storage
* Persistent chat history
* MongoDB data storage
* User and course-scoped lecture retrieval
* Interactive Swagger/OpenAPI documentation

---

## Architecture

```text
                         LectureLens
                              |
                              v
                         FastAPI API
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
       Authentication      MongoDB          AI Layer
            JWT             Data          Ollama/Llama 3.2
             |                                 |
             |                    +------------+------------+
             |                    |            |            |
             |                    v            v            v
             |                Summary       Quiz       Flashcards
             |                                               |
             |                                               v
             |                                          Study Plan
             |
             v
        RAG Pipeline
             |
             v
        Text Chunking
             |
             v
    Sentence Transformers
             |
             v
         Embeddings
             |
             v
         ChromaDB
             |
             v
      Relevant Chunks
             |
             v
         Llama 3.2
             |
             v
           Answer
```

---

## Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Backend              | FastAPI               |
| Programming Language | Python                |
| Database             | MongoDB               |
| Authentication       | JWT                   |
| Password Hashing     | pwdlib                |
| Large Language Model | Llama 3.2             |
| LLM Runtime          | Ollama                |
| Embeddings           | Sentence Transformers |
| Embedding Model      | all-MiniLM-L6-v2      |
| Vector Database      | ChromaDB              |
| API Documentation    | Swagger / OpenAPI     |
| PDF Processing       | Python PDF utilities  |

---

## Project Structure

```text
backend/
|
├── src/
│   ├── ai/
│   │   ├── chat.py
│   │   ├── flashcards.py
│   │   ├── ollama_client.py
│   │   ├── quiz.py
│   │   ├── study_plan.py
│   │   └── summarizer.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── chat.py
│   │       ├── courses.py
│   │       ├── health.py
│   │       ├── lectures.py
│   │       ├── router.py
│   │       ├── study_plans.py
│   │       └── users.py
│   │
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── jwt.py
│   │   └── security.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── sections/
│   │
│   ├── database/
│   │   ├── client.py
│   │   ├── collections.py
│   │   └── dependencies.py
│   │
│   ├── exceptions/
│   │   ├── custom.py
│   │   └── handlers.py
│   │
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── repositories/
│   │   ├── chat.py
│   │   ├── course.py
│   │   ├── lecture.py
│   │   ├── study_plan.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── chat.py
│   │   ├── course.py
│   │   ├── lecture.py
│   │   ├── study_plan.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── chat.py
│   │   ├── course.py
│   │   ├── lecture.py
│   │   ├── study_plan.py
│   │   └── user.py
│   │
│   ├── utils/
│   │   ├── pdf.py
│   │   └── text.py
│   │
│   └── main.py
│
├── tests/
├── docs/
├── scripts/
├── uploads/
├── chroma_db/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── test.http
```

---

## Local Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Learner LENS/backend"
```

### 2. Create the Python Environment

Using Conda:

```bash
conda create -n lecturelens python=3.11
conda activate lecturelens
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Configure Ollama

Verify that Ollama is installed:

```bash
ollama --version
```

Download the required model:

```bash
ollama pull llama3.2:3b
```

Verify that the model is available:

```bash
ollama list
```

The output should contain:

```text
llama3.2:3b
```

### 5. Configure Environment Variables

Create a `.env` file using `.env.example` as a reference.

The following variables are required:

```env
MONGODB_URI=
DATABASE_NAME=lecturelens

JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

MODEL_NAME=llama3.2:3b
TEMPERATURE=0.2
MAX_TOKENS=2048
```

Sensitive values must not be committed to version control.

### 6. Start the Backend

From the `backend` directory:

```bash
uvicorn src.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Authentication

LectureLens uses JWT-based authentication.

The authentication flow is:

```text
Signup
  |
  v
Login
  |
  v
JWT Access Token
  |
  v
Authorization Header
  |
  v
Protected Endpoint
```

Protected requests use:

```http
Authorization: Bearer <JWT_TOKEN>
```

Swagger can also be used to authorize protected endpoints using the generated JWT token.

---

## AI Features

### Lecture Summarization

When a lecture PDF is uploaded, its text is extracted and processed by the locally hosted Llama 3.2 model.

```text
PDF
 |
 v
Text Extraction
 |
 v
Llama 3.2
 |
 v
Summary
```

### Quiz Generation

Lecture material is provided to the LLM to generate multiple-choice questions containing answer options, correct answers, and explanations.

### Flashcard Generation

Lecture material is processed to generate question-and-answer flashcards focused on important concepts, definitions, and technical terminology.

### Study Plan Generation

Lecture material and the requested study duration are provided to the LLM to generate a structured study plan containing topics and study tasks for each day.

---

## Retrieval-Augmented Generation

LectureLens uses Retrieval-Augmented Generation for lecture-based question answering.

When a lecture is uploaded:

```text
PDF
 |
 v
Text Extraction
 |
 v
Text Chunking
 |
 v
Embedding Generation
 |
 v
ChromaDB
```

When a student asks a question:

```text
Student Question
 |
 v
Question Embedding
 |
 v
Similarity Search
 |
 v
Relevant Lecture Chunks
 |
 v
Question + Retrieved Context
 |
 v
Llama 3.2
 |
 v
Answer
```

The retrieval process provides the language model with relevant portions of the student's lecture material before generating the response.

---

## Why RAG?

Sending an entire lecture to the language model for every question is inefficient and becomes increasingly impractical as document size grows.

The RAG architecture allows LectureLens to:

* Retrieve only relevant sections of lecture material
* Reduce unnecessary LLM context
* Ground generated answers in the student's content
* Avoid processing the entire lecture for every question
* Support larger collections of lecture material

---

## Data Isolation

Lecture chunks stored in ChromaDB contain metadata including:

```text
user_id
course_id
lecture_id
chunk_index
```

Retrieval is restricted using the authenticated user's ID and the requested course ID.

The intended access model is:

```text
User A
 |
 +-- Course A
      |
      +-- Course A lecture chunks


User B
 |
 +-- Course B
      |
      +-- Course B lecture chunks
```

This prevents the retrieval layer from intentionally mixing lecture content between users.

---

## Chat History

Chat interactions are persisted in MongoDB.

Each chat record contains information such as:

```text
user_id
course_id
question
answer
created_at
```

This allows users to retrieve previous conversations associated with a course.

---

## API Testing

The project includes a `test.http` file for testing the API.

The primary workflow is:

```text
Signup
 |
 v
Login
 |
 v
Get Current User
 |
 v
Create Course
 |
 v
Upload Lecture
 |
 v
Generate Summary
 |
 v
Generate Quiz
 |
 v
Generate Flashcards
 |
 v
Generate Study Plan
 |
 v
Ask Lecture Question
 |
 v
Retrieve Chat History
```

Swagger/OpenAPI documentation can also be used for interactive API testing.

---

## Future Improvements

Potential improvements include:

* Frontend integration
* Streaming LLM responses
* Conversation-aware RAG
* Hybrid keyword and vector search
* Retrieval reranking
* Background processing for large PDF files
* Improved document chunking strategies
* Automatic indexing of existing lectures
* Evaluation metrics for generated content
* Redis-based caching
* Production-grade vector database
* Docker containerization
* Cloud deployment

---

## Project Status

LectureLens is currently implemented as a local prototype.

The AI inference layer uses Ollama and Llama 3.2, eliminating the need for paid external LLM APIs during development.

The backend currently provides authentication, course and lecture management, AI-powered study tools, RAG-based lecture question answering, and persistent chat history.
