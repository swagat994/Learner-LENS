import { useEffect, useState } from "react";
import {
    Link,
    useNavigate,
    useParams,
} from "react-router-dom";

import {
    getChatHistory,
    sendMessage,
} from "../api/chat";


function Chat() {
    const { courseId } = useParams();
    const navigate = useNavigate();

    const [messages, setMessages] =
        useState([]);

    const [message, setMessage] =
        useState("");

    const [loading, setLoading] =
        useState(true);

    const [sending, setSending] =
        useState(false);

    const [error, setError] =
        useState("");


    useEffect(() => {
        loadChatHistory();
    }, [courseId]);


    const loadChatHistory = async () => {
        try {
            setLoading(true);
            setError("");

            const data =
                await getChatHistory(courseId);

            setMessages(data);
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to load chat history."
            );
        } finally {
            setLoading(false);
        }
    };


    const handleSubmit = async (event) => {
        event.preventDefault();

        const trimmedMessage =
            message.trim();

        if (!trimmedMessage || sending) {
            return;
        }

        try {
            setSending(true);
            setError("");

            const response =
                await sendMessage(
                    courseId,
                    trimmedMessage
                );

            const newMessage = {
                id: `temp-${Date.now()}`,
                question: response.question,
                answer: response.answer,
            };

            setMessages((currentMessages) => [
                ...currentMessages,
                newMessage,
            ]);

            setMessage("");
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to send message."
            );
        } finally {
            setSending(false);
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
                        to={`/courses/${courseId}`}
                    >
                        Back to Course
                    </Link>

                    <h1>AI Study Assistant</h1>

                    <p>
                        Ask questions about your
                        course material.
                    </p>

                </div>


                <button
                    className="logout-button"
                    onClick={handleLogout}
                >
                    Logout
                </button>

            </header>


            <main className="chat-page">

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}


                <div className="chat-container">

                    <div className="chat-messages">

                        {loading ? (
                            <div className="chat-empty">
                                Loading conversation...
                            </div>
                        ) : messages.length === 0 ? (
                            <div className="chat-empty">

                                <h2>
                                    Ask your first
                                    question
                                </h2>

                                <p>
                                    Ask anything about
                                    the lectures in
                                    this course.
                                </p>

                            </div>
                        ) : (
                            messages.map(
                                (item, index) => (
                                    <div
                                        className="chat-message-group"
                                        key={
                                            item.id ||
                                            index
                                        }
                                    >

                                        <div className="user-message">
                                            <div className="message-label">
                                                You
                                            </div>

                                            <p>
                                                {
                                                    item.question
                                                }
                                            </p>
                                        </div>


                                        <div className="ai-message">
                                            <div className="message-label">
                                                LectureLens AI
                                            </div>

                                            <p>
                                                {
                                                    item.answer
                                                }
                                            </p>
                                        </div>

                                    </div>
                                )
                            )
                        )}

                    </div>


                    <form
                        className="chat-input-container"
                        onSubmit={handleSubmit}
                    >

                        <textarea
                            value={message}
                            onChange={(event) =>
                                setMessage(
                                    event.target
                                        .value
                                )
                            }
                            placeholder="Ask a question about your course..."
                            rows={3}
                            disabled={sending}
                        />


                        <button
                            className="primary-button"
                            type="submit"
                            disabled={
                                sending ||
                                !message.trim()
                            }
                        >
                            {sending
                                ? "Thinking..."
                                : "Send"}
                        </button>

                    </form>

                </div>

            </main>

        </div>
    );
}


export default Chat;