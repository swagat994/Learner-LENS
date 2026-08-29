import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Course from "./pages/Course";
import Lecture from "./pages/Lecture";
import Quiz from "./pages/Quiz";
import Flashcards from "./pages/Flashcards";
import Chat from "./pages/Chat";

import ProtectedRoute from "./components/ProtectedRoute";
import PublicRoute from "./components/PublicRoute";


function App() {
    return (
        <BrowserRouter>
            <Routes>

                {/* Root */}

                <Route
                    path="/"
                    element={
                        <Navigate
                            to="/login"
                            replace
                        />
                    }
                />


                {/* Public Routes */}

                <Route element={<PublicRoute />}>

                    <Route
                        path="/login"
                        element={<Login />}
                    />

                    <Route
                        path="/signup"
                        element={<Signup />}
                    />

                </Route>


                {/* Protected Routes */}

                <Route element={<ProtectedRoute />}>

                    <Route
                        path="/dashboard"
                        element={<Dashboard />}
                    />

                    <Route
                        path="/courses/:courseId"
                        element={<Course />}
                    />

                    <Route
                        path="/courses/:courseId/lectures/:lectureId"
                        element={<Lecture />}
                    />

                    <Route
                        path="/courses/:courseId/lectures/:lectureId/quiz"
                        element={<Quiz />}
                    />

                    <Route
                        path="/courses/:courseId/lectures/:lectureId/flashcards"
                        element={<Flashcards />}
                    />

                    <Route
                        path="/courses/:courseId/chat"
                        element={<Chat />}
                    />

                </Route>

            </Routes>
        </BrowserRouter>
    );
}


export default App;