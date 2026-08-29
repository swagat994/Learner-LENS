import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { generateQuiz } from "../api/lectures";


function Quiz() {
    const { courseId, lectureId } = useParams();
    const navigate = useNavigate();

    const [quiz, setQuiz] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const [currentQuestion, setCurrentQuestion] =
        useState(0);

    const [selectedAnswer, setSelectedAnswer] =
        useState("");

    const [answers, setAnswers] = useState({});

    const [finished, setFinished] =
        useState(false);


    const handleGenerateQuiz = async () => {
        try {
            setLoading(true);
            setError("");

            const data = await generateQuiz(
                courseId,
                lectureId
            );

            setQuiz(data);
            setCurrentQuestion(0);
            setSelectedAnswer("");
            setAnswers({});
            setFinished(false);
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to generate quiz."
            );
        } finally {
            setLoading(false);
        }
    };


    const handleNext = () => {
        if (!selectedAnswer) {
            return;
        }

        const updatedAnswers = {
            ...answers,
            [currentQuestion]: selectedAnswer,
        };

        setAnswers(updatedAnswers);

        if (
            currentQuestion ===
            quiz.questions.length - 1
        ) {
            setFinished(true);
            return;
        }

        setCurrentQuestion(
            currentQuestion + 1
        );

        setSelectedAnswer(
            updatedAnswers[
                currentQuestion + 1
            ] || ""
        );
    };


    const calculateScore = () => {
        if (!quiz) {
            return 0;
        }

        return quiz.questions.reduce(
            (score, question, index) => {
                if (
                    answers[index] ===
                    question.answer
                ) {
                    return score + 1;
                }

                return score;
            },
            0
        );
    };


    return (
        <div className="dashboard-page">

            <header className="dashboard-header">

                <div>
                    <Link
                        to={`/courses/${courseId}/lectures/${lectureId}`}
                    >
                        ← Back to Lecture
                    </Link>

                    <h1>Quiz</h1>

                    <p>
                        Test your understanding of
                        this lecture.
                    </p>
                </div>

                <button
                    className="logout-button"
                    onClick={() => {
                        localStorage.removeItem(
                            "token"
                        );

                        navigate("/login");
                    }}
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


                {!quiz && (
                    <div className="empty-state">

                        <h2>
                            Ready to test yourself?
                        </h2>

                        <p>
                            Generate a quiz based on
                            your lecture summary.
                        </p>

                        <button
                            className="primary-button"
                            onClick={
                                handleGenerateQuiz
                            }
                            disabled={loading}
                        >
                            {loading
                                ? "Generating Quiz..."
                                : "Generate Quiz"}
                        </button>

                    </div>
                )}


                {quiz && !finished && (
                    <div className="quiz-card">

                        <div className="quiz-progress">
                            Question{" "}
                            {currentQuestion + 1}{" "}
                            of{" "}
                            {quiz.questions.length}
                        </div>


                        <h2>
                            {
                                quiz.questions[
                                    currentQuestion
                                ].question
                            }
                        </h2>


                        <div className="quiz-options">

                            {quiz.questions[
                                currentQuestion
                            ].options.map(
                                (option) => (
                                    <button
                                        key={option}
                                        className={
                                            selectedAnswer ===
                                            option
                                                ? "quiz-option selected"
                                                : "quiz-option"
                                        }
                                        onClick={() =>
                                            setSelectedAnswer(
                                                option
                                            )
                                        }
                                    >
                                        {option}
                                    </button>
                                )
                            )}

                        </div>


                        <button
                            className="primary-button"
                            onClick={handleNext}
                            disabled={!selectedAnswer}
                        >
                            {currentQuestion ===
                            quiz.questions.length - 1
                                ? "Finish Quiz"
                                : "Next Question"}
                        </button>

                    </div>
                )}


                {quiz && finished && (
                    <div className="quiz-result">

                        <h2>
                            Quiz Complete
                        </h2>

                        <div className="score">
                            {calculateScore()} /{" "}
                            {quiz.questions.length}
                        </div>

                        <p>
                            You answered{" "}
                            {calculateScore()}{" "}
                            out of{" "}
                            {quiz.questions.length}{" "}
                            questions correctly.
                        </p>


                        <div className="quiz-review">

                            {quiz.questions.map(
                                (
                                    question,
                                    index
                                ) => {
                                    const correct =
                                        answers[
                                            index
                                        ] ===
                                        question.answer;

                                    return (
                                        <div
                                            className="review-card"
                                            key={index}
                                        >

                                            <h3>
                                                Question{" "}
                                                {index +
                                                    1}
                                            </h3>

                                            <p>
                                                {
                                                    question.question
                                                }
                                            </p>

                                            <p>
                                                <strong>
                                                    Your answer:
                                                </strong>{" "}
                                                {answers[
                                                    index
                                                ]}
                                            </p>

                                            <p>
                                                <strong>
                                                    Correct answer:
                                                </strong>{" "}
                                                {
                                                    question.answer
                                                }
                                            </p>

                                            <p>
                                                {
                                                    question.explanation
                                                }
                                            </p>

                                            <strong>
                                                {correct
                                                    ? "Correct"
                                                    : "Incorrect"}
                                            </strong>

                                        </div>
                                    );
                                }
                            )}

                        </div>


                        <button
                            className="primary-button"
                            onClick={() => {
                                setQuiz(null);
                                setAnswers({});
                                setFinished(false);
                            }}
                        >
                            Generate New Quiz
                        </button>

                    </div>
                )}

            </main>

        </div>
    );
}


export default Quiz;