import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getCurrentUser } from "../api/auth";
import {
    createCourse,
    deleteCourse,
    getCourses,
} from "../api/courses";


function Dashboard() {
    const navigate = useNavigate();

    const [user, setUser] = useState(null);
    const [courses, setCourses] = useState([]);

    const [showCreateForm, setShowCreateForm] =
        useState(false);

    const [title, setTitle] = useState("");
    const [description, setDescription] =
        useState("");

    const [loading, setLoading] = useState(true);
    const [creating, setCreating] = useState(false);
    const [error, setError] = useState("");


    useEffect(() => {
        loadDashboard();
    }, []);


    const loadDashboard = async () => {
        try {
            setLoading(true);
            setError("");

            const [userData, courseData] =
                await Promise.all([
                    getCurrentUser(),
                    getCourses(),
                ]);

            setUser(userData);
            setCourses(courseData);
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to load dashboard."
            );
        } finally {
            setLoading(false);
        }
    };


    const handleCreateCourse = async (event) => {
        event.preventDefault();

        if (!title.trim()) {
            return;
        }

        try {
            setCreating(true);
            setError("");

            const newCourse = await createCourse({
                title: title.trim(),
                description:
                    description.trim() || null,
            });

            setCourses((currentCourses) => [
                ...currentCourses,
                newCourse,
            ]);

            setTitle("");
            setDescription("");
            setShowCreateForm(false);
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to create course."
            );
        } finally {
            setCreating(false);
        }
    };


    const handleDeleteCourse = async (
        courseId
    ) => {
        const confirmed = window.confirm(
            "Are you sure you want to delete this course?"
        );

        if (!confirmed) {
            return;
        }

        try {
            setError("");

            await deleteCourse(courseId);

            setCourses((currentCourses) =>
                currentCourses.filter(
                    (course) =>
                        course.id !== courseId
                )
            );
        } catch (error) {
            setError(
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to delete course."
            );
        }
    };


    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };


    if (loading) {
        return (
            <div className="dashboard-page">
                <p>Loading dashboard...</p>
            </div>
        );
    }


    return (
        <div className="dashboard-page">

            <header className="dashboard-header">

                <div>
                    <h1>LectureLens</h1>

                    {user && (
                        <p>
                            Welcome, {user.name}
                        </p>
                    )}
                </div>

                <button
                    className="logout-button"
                    onClick={handleLogout}
                >
                    Logout
                </button>

            </header>


            <main className="dashboard-content">

                <div className="section-header">

                    <div>
                        <h2>Your Courses</h2>

                        <p>
                            Manage your courses and
                            lecture material.
                        </p>
                    </div>

                    <button
                        className="primary-button"
                        onClick={() =>
                            setShowCreateForm(
                                !showCreateForm
                            )
                        }
                    >
                        {showCreateForm
                            ? "Cancel"
                            : "Create Course"}
                    </button>

                </div>


                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}


                {showCreateForm && (
                    <form
                        className="course-form"
                        onSubmit={
                            handleCreateCourse
                        }
                    >

                        <h3>Create a Course</h3>

                        <div className="form-group">

                            <label htmlFor="title">
                                Course Title
                            </label>

                            <input
                                id="title"
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

                            <label htmlFor="description">
                                Description
                            </label>

                            <textarea
                                id="description"
                                value={description}
                                onChange={(event) =>
                                    setDescription(
                                        event.target
                                            .value
                                    )
                                }
                                maxLength={500}
                                rows={4}
                            />

                        </div>


                        <button
                            className="primary-button"
                            type="submit"
                            disabled={creating}
                        >
                            {creating
                                ? "Creating..."
                                : "Create Course"}
                        </button>

                    </form>
                )}


                {courses.length === 0 ? (
                    <div className="empty-state">

                        <h3>
                            No courses yet
                        </h3>

                        <p>
                            Create your first course
                            to get started.
                        </p>

                    </div>
                ) : (
                    <div className="course-grid">

                        {courses.map((course) => (
                            <div
                                className="course-card"
                                key={course.id}
                            >

                                <div
                                    className="course-card-content"
                                    onClick={() =>
                                        navigate(
                                            `/courses/${course.id}`
                                        )
                                    }
                                >

                                    <h3>
                                        {course.title}
                                    </h3>

                                    <p>
                                        {course.description ||
                                            "No description provided."}
                                    </p>

                                </div>


                                <div className="course-card-footer">

                                    <button
                                        className="view-button"
                                        onClick={() =>
                                            navigate(
                                                `/courses/${course.id}`
                                            )
                                        }
                                    >
                                        Open Course
                                    </button>

                                    <button
                                        className="delete-button"
                                        onClick={() =>
                                            handleDeleteCourse(
                                                course.id
                                            )
                                        }
                                    >
                                        Delete
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


export default Dashboard;