# LectureLens Frontend

The LectureLens frontend is a React-based web application that provides the user interface for the LectureLens learning platform. It communicates with the FastAPI backend through REST APIs and provides authentication, course management, lecture management, AI-powered study tools, and course-specific RAG chat.

## Features

### Authentication

* User registration
* User login
* JWT-based authentication
* Protected application routes
* Automatic handling of unauthorized API responses
* Automatic redirection for authenticated and unauthenticated users

### Course Management

* Create courses
* View courses
* Update courses
* Delete courses
* View course-specific lectures

### Lecture Management

* Upload PDF lecture material
* View uploaded lectures
* Generate AI-powered lecture summaries

### AI Study Tools

* Generate quizzes from lecture content
* Generate flashcards from lecture content
* Ask questions using course-specific RAG chat

### Chat

* Course-specific AI conversations
* Persistent chat history
* Loading and error states
* Authentication-aware API requests

### User Interface

* Responsive layout
* Consistent component styling
* Rounded controls and cards
* Form validation
* Loading states
* Error handling
* Responsive behavior for smaller screens

---

## Technology Stack

| Technology   | Purpose                           |
| ------------ | --------------------------------- |
| React        | User interface                    |
| Vite         | Development server and build tool |
| React Router | Client-side routing               |
| Axios        | HTTP client and API communication |
| ESLint       | Static analysis and code quality  |
| CSS          | Application styling               |

---

## Project Structure

```text
frontend/
│
├── public/
│
├── src/
│   │
│   ├── api/
│   │   ├── axios.js
│   │   ├── auth.js
│   │   ├── courses.js
│   │   ├── lectures.js
│   │   └── chat.js
│   │
│   ├── components/
│   │   ├── ProtectedRoute.jsx
│   │   └── PublicRoute.jsx
│   │
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Course.jsx
│   │   ├── Lecture.jsx
│   │   ├── Quiz.jsx
│   │   ├── Flashcards.jsx
│   │   └── Chat.jsx
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── .env
├── package.json
└── README.md
```

---

## Prerequisites

The following software must be installed before running the frontend:

* Node.js
* npm

Verify the installations:

```bash
node --version
npm --version
```

---

## Installation

Navigate to the frontend directory and install the project dependencies:

```bash
npm install
```

---

## Environment Configuration

Create a `.env` file in the `frontend` directory.

```env
VITE_API_URL=http://localhost:8000/api/v1
```

`VITE_API_URL` specifies the base URL used by Axios for communicating with the LectureLens backend.

For local development, the expected configuration is:

```text
Frontend
http://localhost:5173

Backend
http://localhost:8000/api/v1
```

Environment files containing sensitive information should not be committed to version control.

---

## Running the Development Server

Start the frontend development server with:

```bash
npm run dev
```

Vite will display the local development URL in the terminal.

The application is typically available at:

```text
http://localhost:5173
```

The LectureLens backend must also be running for authentication, course management, lecture processing, and AI functionality to work.

---

## Linting

Run ESLint with:

```bash
npm run lint
```

This checks the frontend source code for common JavaScript and React issues.

---

## Production Build

Create a production build with:

```bash
npm run build
```

The generated production files are placed in the `dist` directory.

To preview the production build locally:

```bash
npm run preview
```

---

## Authentication

LectureLens uses JWT-based authentication.

The authentication flow is:

```text
User
 |
 | Login credentials
 v
React Frontend
 |
 | POST /auth/login
 v
FastAPI Backend
 |
 | Access token
 v
React Frontend
 |
 | Store token
 v
localStorage
 |
 | Authorization: Bearer <token>
 v
Protected API endpoints
```

The Axios request interceptor retrieves the JWT from `localStorage` and attaches it to authenticated requests.

If the backend responds with HTTP 401 Unauthorized, the Axios response interceptor removes the stored token and redirects the user to the login page.

---

## Route Protection

The frontend separates public and protected routes.

### Public Routes

```text
/login
/signup
```

### Protected Routes

```text
/dashboard

/courses/:courseId

/courses/:courseId/lectures/:lectureId

/courses/:courseId/lectures/:lectureId/quiz

/courses/:courseId/lectures/:lectureId/flashcards

/courses/:courseId/chat
```

`ProtectedRoute` verifies the presence of an authentication token before rendering protected pages.

`PublicRoute` prevents authenticated users from unnecessarily accessing the login and registration pages.

---

## API Communication

API communication is centralized through Axios.

The Axios instance:

1. Uses `VITE_API_URL` as the base URL.
2. Automatically attaches the JWT when available.
3. Uses JSON for standard API requests.
4. Supports `FormData` for PDF uploads.
5. Handles unauthorized responses globally.

The frontend communicates with endpoints provided by the FastAPI backend, including:

```text
POST   /auth/signup
POST   /auth/login

POST   /courses
GET    /courses
GET    /courses/{course_id}
PUT    /courses/{course_id}
DELETE /courses/{course_id}

POST   /courses/{course_id}/lectures
GET    /courses/{course_id}/lectures
GET    /courses/{course_id}/lectures/{lecture_id}

POST   /courses/{course_id}/lectures/{lecture_id}/summarize

POST   /courses/{course_id}/lectures/{lecture_id}/quiz

POST   /courses/{course_id}/lectures/{lecture_id}/flashcards

POST   /courses/{course_id}/chat
GET    /courses/{course_id}/chat
```

---

## PDF Upload

Lecture PDFs are uploaded using a `multipart/form-data` request.

The frontend sends:

```text
POST /courses/{course_id}/lectures
```

with the following form fields:

```text
title
file
```

The file is transmitted using the browser's `FormData` API.

The Axios configuration allows the browser to automatically generate the required multipart boundary.

---

## AI Features

### Lecture Summarization

Users can request an AI-generated summary for an uploaded lecture.

```text
POST /courses/{course_id}/lectures/{lecture_id}/summarize
```

The generated summary is displayed on the lecture page.

### Quiz Generation

Users can generate an AI-powered quiz from a summarized lecture.

### Flashcard Generation

Users can generate AI-powered flashcards from a summarized lecture.

### RAG Chat

The frontend provides a course-specific chat interface.

```text
POST /courses/{course_id}/chat
```

The request contains:

```json
{
    "message": "User question"
}
```

The backend returns:

```json
{
    "question": "User question",
    "answer": "Generated answer"
}
```

Chat history is retrieved using:

```text
GET /courses/{course_id}/chat
```

---

## Frontend Architecture

The frontend follows a separation between pages, API communication, and reusable routing components.

```text
React Pages
    |
    v
API Modules
    |
    v
Axios Instance
    |
    v
FastAPI Backend
```

### Pages

Pages contain the user-facing application views and manage page-level state.

### API Modules

API modules contain functions responsible for communicating with specific backend resources.

### Axios Instance

The centralized Axios instance manages:

* Base API URL
* JWT authentication
* Request configuration
* Response handling
* Unauthorized request handling

### Route Components

`ProtectedRoute` controls access to authenticated pages.

`PublicRoute` controls access to authentication pages.

---

## Development Workflow

Start the backend before starting the frontend.

### Backend

From the backend directory:

```bash
uvicorn src.main:app --reload
```

### Frontend

From the frontend directory:

```bash
npm run dev
```

The frontend can then be accessed through the URL provided by Vite.

---

## Code Quality

Before committing changes, run:

```bash
npm run lint
```

and:

```bash
npm run build
```

Both commands should complete successfully before creating a production deployment.

---

## Project Status

The LectureLens frontend currently provides the complete client-side interface for:

* User authentication
* JWT-based authorization
* Protected routing
* Course management
* Lecture management
* PDF uploads
* AI lecture summarization
* AI quiz generation
* AI flashcard generation
* RAG-powered course chat
* Persistent chat history
* API error handling
* Responsive user interface

