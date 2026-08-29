import { useEffect, useState } from "react";
import {
    Link,
    useNavigate,
    useParams,
} from "react-router-dom";

import { getCourse } from "../api/courses";
import {
    getLectures,
    uploadLecture,
} from "../api/lectures";


function Course() {
    const { courseId } = useParams();
    const navigate = useNavigate();

    const [course, setCourse] = useState(null);
    const [lectures, setLectures] = useState([]);

    const [title, setTitle] = useState("");
    const [file, setFile] = useState(null);

    const [showUploadForm, setShowUploadForm] =
        useState(false);

    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState("");


    useEffect(() => {
        loadCourse();
    }, [courseId]);


    const loadCourse = async () => {
        try {
            setLoading(true);
            setError("");

            const [courseData, lectureData] =
                await Promise.all([
                    getCourse(courseId),
                    getLectures(courseId),
                ]);

            setCourse(courseData);
            setLectures(lectureData);
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to load course."
            );
        } finally {
            setLoading(false);
        }
    };


    const handleUpload = async (event) => {
        event.preventDefault();

        if (!title.trim() || !file) {
            setError(
                "Please provide a lecture title and PDF file."
            );
            return;
        }

        if (file.type !== "application/pdf") {
            setError("Only PDF files are allowed.");
            return;
        }

        try {
            setUploading(true);
            setError("");

            const lecture = await uploadLecture(
                courseId,
                title.trim(),
                file
            );

            setLectures((currentLectures) => [
                ...currentLectures,
                lecture,
            ]);

            setTitle("");
            setFile(null);
            setShowUploadForm(false);

            event.target.reset();
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to upload lecture."
            );
        } finally {
            setUploading(false);
        }
    };


    if (loading) {
        return (
            <div className="dashboard-page">
                <p>Loading course...</p>
            </div>
        );
    }


    if (!course) {
        return (
            <div className="dashboard-page">
                <p>Course not found.</p>

                <button
                    onClick={() =>
                        navigate("/dashboard")
                    }
                >
                    Back to Dashboard
                </button>
            </div>
        );
    }


    return (
        <div className="dashboard-page">

            <header className="dashboard-header">

                <div>
                    <Link to="/dashboard">
                        LectureLens
                    </Link>

                    <h1>{course.title}</h1>

                    <p>
                        {course.description ||
                            "No description provided."}
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

                <div className="section-header">

                    <div>
                        <h2>Lectures</h2>

                        <p>
                            Upload and manage your
                            lecture material.
                        </p>
                    </div>

                    <button
                        className="primary-button"
                        onClick={() =>
                            setShowUploadForm(
                                !showUploadForm
                            )
                        }
                    >
                        {showUploadForm
                            ? "Cancel"
                            : "Upload Lecture"}
                    </button>

                </div>


                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}


                {showUploadForm && (
                    <form
                        className="course-form"
                        onSubmit={handleUpload}
                    >

                        <h3>
                            Upload Lecture
                        </h3>


                        <div className="form-group">

                            <label htmlFor="lecture-title">
                                Lecture Title
                            </label>

                            <input
                                id="lecture-title"
                                type="text"
                                value={title}
                                onChange={(event) =>
                                    setTitle(
                                        event.target
                                            .value
                                    )
                                }
                                maxLength={100}
                                required
                            />

                        </div>


                        <div className="form-group">

                            <label htmlFor="lecture-file">
                                PDF File
                            </label>

                            <input
                                id="lecture-file"
                                type="file"
                                accept=".pdf,application/pdf"
                                onChange={(event) =>
                                    setFile(
                                        event.target
                                            .files?.[0] ||
                                        null
                                    )
                                }
                                required
                            />

                        </div>


                        <button
                            className="primary-button"
                            type="submit"
                            disabled={uploading}
                        >
                            {uploading
                                ? "Uploading..."
                                : "Upload Lecture"}
                        </button>

                    </form>
                )}


                {lectures.length === 0 ? (
                    <div className="empty-state">

                        <h3>
                            No lectures yet
                        </h3>

                        <p>
                            Upload your first PDF
                            lecture to get started.
                        </p>

                    </div>
                ) : (
                    <div className="course-grid">

                        {lectures.map((lecture) => (
                            <div
                                className="course-card"
                                key={lecture.id}
                            >

                                <div className="course-card-content">

                                    <h3>
                                        {lecture.title}
                                    </h3>

                                    <p>
                                        {lecture.file_name}
                                    </p>

                                </div>


                                <div className="course-card-footer">

                                    <button
                                        className="view-button"
                                        onClick={() =>
                                            navigate(
                                                `/courses/${courseId}/lectures/${lecture.id}`
                                            )
                                        }
                                    >
                                        Open Lecture
                                    </button>

                                </div>

                            </div>
                        ))}

                    </div>
                )}

            </main>

        </div>
    );
}


export default Course;