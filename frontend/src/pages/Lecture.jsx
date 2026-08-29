import { useEffect, useState } from "react";
import {
    Link,
    useNavigate,
    useParams,
} from "react-router-dom";

import {
    getLecture,
    summarizeLecture,
} from "../api/lectures";


function Lecture() {
    const { courseId, lectureId } = useParams();
    const navigate = useNavigate();

    const [lecture, setLecture] = useState(null);
    const [loading, setLoading] = useState(true);
    const [summarizing, setSummarizing] =
        useState(false);
    const [error, setError] = useState("");


    useEffect(() => {
        loadLecture();
    }, [lectureId]);


    const loadLecture = async () => {
        try {
            setLoading(true);
            setError("");

            const data = await getLecture(
                courseId,
                lectureId
            );

            setLecture(data);
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to load lecture."
            );
        } finally {
            setLoading(false);
        }
    };


    const handleSummarize = async () => {
        try {
            setSummarizing(true);
            setError("");

            const updatedLecture =
                await summarizeLecture(
                    courseId,
                    lectureId
                );

            setLecture(updatedLecture);
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to generate summary."
            );
        } finally {
            setSummarizing(false);
        }
    };


    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };


    if (loading) {
        return (
            <div className="dashboard-page">
                <p>Loading lecture...</p>
            </div>
        );
    }


    if (!lecture) {
        return (
            <div className="dashboard-page">

                <p>Lecture not found.</p>

                <button
                    className="primary-button"
                    onClick={() =>
                        navigate(
                            `/courses/${courseId}`
                        )
                    }
                >
                    Back to Course
                </button>

            </div>
        );
    }


    return (
        <div className="dashboard-page">

            <header className="dashboard-header">

                <div>

                    <Link
                        to={`/courses/${courseId}`}
                    >
                        Back to Course
                    </Link>

                    <h1>{lecture.title}</h1>

                    <p>
                        {lecture.file_name}
                    </p>

                </div>


                <button
                    className="logout-button"
                    onClick={handleLogout}
                >
                    Logout
                </button>

            </header>


            <main className="dashboard-content">

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}


                <section className="lecture-section">

                    <div className="section-header">

                        <div>

                            <h2>Summary</h2>

                            <p>
                                AI-generated summary
                                of your lecture.
                            </p>

                        </div>


                        {!lecture.summary && (
                            <button
                                className="primary-button"
                                onClick={
                                    handleSummarize
                                }
                                disabled={
                                    summarizing
                                }
                            >
                                {summarizing
                                    ? "Generating..."
                                    : "Generate Summary"}
                            </button>
                        )}

                    </div>


                    {lecture.summary ? (
                        <div className="summary-card">

                            <p>
                                {lecture.summary}
                            </p>

                        </div>
                    ) : (
                        <div className="empty-state">

                            <h3>
                                No summary yet
                            </h3>

                            <p>
                                Generate an
                                AI-powered summary
                                of this lecture.
                            </p>

                        </div>
                    )}

                </section>


                <section className="lecture-section">

                    <div className="section-header">

                        <div>

                            <h2>
                                AI Study Tools
                            </h2>

                            <p>
                                Use AI to study and
                                test your understanding.
                            </p>

                        </div>

                    </div>


                    <div className="course-grid">

                        <div className="course-card">

                            <div className="course-card-content">

                                <h3>
                                    Quiz
                                </h3>

                                <p>
                                    Test your
                                    understanding of
                                    the lecture.
                                </p>

                            </div>


                            <div className="course-card-footer">

                                <button
                                    className="view-button"
                                    disabled={
                                        !lecture.summary
                                    }
                                    onClick={() =>
                                        navigate(
                                            `/courses/${courseId}/lectures/${lectureId}/quiz`
                                        )
                                    }
                                >
                                    Generate Quiz
                                </button>

                            </div>

                        </div>


                        <div className="course-card">

                            <div className="course-card-content">

                                <h3>
                                    Flashcards
                                </h3>

                                <p>
                                    Review important
                                    concepts with
                                    flashcards.
                                </p>

                            </div>


                            <div className="course-card-footer">

                                <button
                                    className="view-button"
                                    disabled={
                                        !lecture.summary
                                    }
                                    onClick={() =>
                                        navigate(
                                            `/courses/${courseId}/lectures/${lectureId}/flashcards`
                                        )
                                    }
                                >
                                    Generate Flashcards
                                </button>

                            </div>

                        </div>


                        <div className="course-card">

                            <div className="course-card-content">

                                <h3>
                                    AI Chat
                                </h3>

                                <p>
                                    Ask questions about
                                    your course material
                                    using RAG-powered AI.
                                </p>

                            </div>


                            <div className="course-card-footer">

                                <button
                                    className="view-button"
                                    onClick={() =>
                                        navigate(
                                            `/courses/${courseId}/chat`
                                        )
                                    }
                                >
                                    Open Chat
                                </button>

                            </div>

                        </div>

                    </div>

                </section>

            </main>

        </div>
    );
}


export default Lecture;