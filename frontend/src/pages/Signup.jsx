import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { signup } from "../api/auth";


function Signup() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        name: "",
        email: "",
        password: "",
    });

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);


    const handleChange = (event) => {
        setFormData({
            ...formData,
            [event.target.name]: event.target.value,
        });
    };


    const handleSubmit = async (event) => {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            await signup(formData);

            navigate("/login");
        } catch (error) {
            const message =
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Unable to create account.";

            setError(message);
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className="auth-page">

            <div className="auth-decoration auth-decoration-one" />
            <div className="auth-decoration auth-decoration-two" />

            <div className="auth-wrapper">

                <div className="auth-brand">

                    <div className="brand-icon">
                        LL
                    </div>

                    <span>
                        LectureLens
                    </span>

                </div>


                <div className="auth-card">

                    <div className="auth-heading">

                        <h1>
                            Create your account
                        </h1>

                        <p>
                            Start learning smarter
                            with LectureLens.
                        </p>

                    </div>


                    {error && (
                        <div className="auth-error">
                            {error}
                        </div>
                    )}


                    <form
                        className="auth-form"
                        onSubmit={handleSubmit}
                    >

                        <div className="auth-form-group">

                            <label htmlFor="name">
                                Full name
                            </label>

                            <input
                                id="name"
                                name="name"
                                type="text"
                                value={formData.name}
                                onChange={handleChange}
                                placeholder="Enter your full name"
                                autoComplete="name"
                                minLength={2}
                                maxLength={100}
                                required
                            />

                        </div>


                        <div className="auth-form-group">

                            <label htmlFor="email">
                                Email address
                            </label>

                            <input
                                id="email"
                                name="email"
                                type="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="you@example.com"
                                autoComplete="email"
                                required
                            />

                        </div>


                        <div className="auth-form-group">

                            <label htmlFor="password">
                                Password
                            </label>

                            <input
                                id="password"
                                name="password"
                                type="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="Create a secure password"
                                autoComplete="new-password"
                                minLength={8}
                                maxLength={128}
                                required
                            />

                            <span className="password-hint">
                                Use at least 8 characters.
                            </span>

                        </div>


                        <button
                            className="auth-submit-button"
                            type="submit"
                            disabled={loading}
                        >
                            {loading
                                ? "Creating account..."
                                : "Create account"}
                        </button>

                    </form>


                    <div className="auth-divider">
                        <span>
                            Already have an account?
                        </span>
                    </div>


                    <Link
                        className="auth-create-button"
                        to="/login"
                    >
                        Sign in instead
                    </Link>

                </div>


                <p className="auth-footer">
                    Learn. Review. Master.
                </p>

            </div>

        </div>
    );
}


export default Signup;