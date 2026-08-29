import { useState } from "react";
import {
    Link,
    useNavigate,
    useParams,
} from "react-router-dom";

import { generateFlashcards } from "../api/lectures";


function Flashcards() {
    const { courseId, lectureId } = useParams();
    const navigate = useNavigate();

    const [flashcards, setFlashcards] =
        useState(null);

    const [currentCard, setCurrentCard] =
        useState(0);

    const [showAnswer, setShowAnswer] =
        useState(false);

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState("");


    const handleGenerateFlashcards =
        async () => {
            try {
                setLoading(true);
                setError("");

                const data =
                    await generateFlashcards(
                        courseId,
                        lectureId
                    );

                setFlashcards(data.flashcards);
                setCurrentCard(0);
                setShowAnswer(false);
            } catch (error) {
                setError(
                    error.response?.data?.error?.message ||
                    error.response?.data?.detail ||
                    "Unable to generate flashcards."
                );
            } finally {
                setLoading(false);
            }
        };


    const handleNext = () => {
        if (
            currentCard <
            flashcards.length - 1
        ) {
            setCurrentCard(
                currentCard + 1
            );

            setShowAnswer(false);
        }
    };


    const handlePrevious = () => {
        if (currentCard > 0) {
            setCurrentCard(
                currentCard - 1
            );

            setShowAnswer(false);
        }
    };


    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };


    return (
        <div className="dashboard-page">

            <header className="dashboard-header">

                <div>

                    <Link
                        to={`/courses/${courseId}/lectures/${lectureId}`}
                    >
                        Back to Lecture
                    </Link>

                    <h1>Flashcards</h1>

                    <p>
                        Review important concepts
                        from your lecture.
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


                {!flashcards && (
                    <div className="empty-state">

                        <h2>
                            Ready to study?
                        </h2>

                        <p>
                            Generate flashcards
                            from your lecture
                            summary.
                        </p>

                        <button
                            className="primary-button"
                            onClick={
                                handleGenerateFlashcards
                            }
                            disabled={loading}
                        >
                            {loading
                                ? "Generating..."
                                : "Generate Flashcards"}
                        </button>

                    </div>
                )}


                {flashcards && (
                    <div className="flashcards-container">

                        <div className="flashcard-progress">
                            Card{" "}
                            {currentCard + 1}{" "}
                            of{" "}
                            {flashcards.length}
                        </div>


                        <div
                            className="flashcard"
                            onClick={() =>
                                setShowAnswer(
                                    !showAnswer
                                )
                            }
                        >

                            {!showAnswer ? (
                                <>
                                    <span className="flashcard-label">
                                        Question
                                    </span>

                                    <h2>
                                        {
                                            flashcards[
                                                currentCard
                                            ].question
                                        }
                                    </h2>

                                    <p>
                                        Click to reveal
                                        answer
                                    </p>
                                </>
                            ) : (
                                <>
                                    <span className="flashcard-label">
                                        Answer
                                    </span>

                                    <h2>
                                        {
                                            flashcards[
                                                currentCard
                                            ].answer
                                        }
                                    </h2>

                                    <p>
                                        Click to hide
                                        answer
                                    </p>
                                </>
                            )}

                        </div>


                        <div className="flashcard-controls">

                            <button
                                className="secondary-button"
                                onClick={
                                    handlePrevious
                                }
                                disabled={
                                    currentCard === 0
                                }
                            >
                                Previous
                            </button>


                            <button
                                className="primary-button"
                                onClick={() =>
                                    setShowAnswer(
                                        !showAnswer
                                    )
                                }
                            >
                                {showAnswer
                                    ? "Hide Answer"
                                    : "Show Answer"}
                            </button>


                            <button
                                className="secondary-button"
                                onClick={
                                    handleNext
                                }
                                disabled={
                                    currentCard ===
                                    flashcards.length - 1
                                }
                            >
                                Next
                            </button>

                        </div>


                        <button
                            className="generate-again-button"
                            onClick={
                                handleGenerateFlashcards
                            }
                            disabled={loading}
                        >
                            {loading
                                ? "Generating..."
                                : "Generate New Set"}
                        </button>

                    </div>
                )}

            </main>

        </div>
    );
}


export default Flashcards;