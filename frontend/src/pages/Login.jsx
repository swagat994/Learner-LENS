import { useState } from "react";
import {
    Link,
    useNavigate,
} from "react-router-dom";

import { login } from "../api/auth";


function Login() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);


    const handleChange = (event) => {
        setFormData({
            ...formData,
            [event.target.name]:
                event.target.value,
        });
    };


    const handleSubmit = async (event) => {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            const data = await login(formData);

            localStorage.setItem(
                "token",
                data.access_token
            );

            navigate("/dashboard");
        } catch (error) {
            const message =
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Invalid email or password.";

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
                            Welcome back
                        </h1>

                        <p>
                            Sign in to continue
                            learning smarter.
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

                            <label htmlFor="email">
                                Email address
                            </label>

                            <input
                                id="email"
                                name="email"
                                type="email"
                                value={
                                    formData.email
                                }
                                onChange={
                                    handleChange
                                }
                                placeholder="you@example.com"
                                autoComplete="email"
                                required
                            />

                        </div>


                        <div className="auth-form-group">

                            <div className="password-label-row">

                                <label htmlFor="password">
                                    Password
                                </label>

                            </div>

                            <input
                                id="password"
                                name="password"
                                type="password"
                                value={
                                    formData.password
                                }
                                onChange={
                                    handleChange
                                }
                                placeholder="Enter your password"
                                autoComplete="current-password"
                                required
                            />

                        </div>


                        <button
                            className="auth-submit-button"
                            type="submit"
                            disabled={loading}
                        >
                            {loading
                                ? "Signing in..."
                                : "Sign in"}
                        </button>

                    </form>


                    <div className="auth-divider">
                        <span>
                            New to LectureLens?
                        </span>
                    </div>


                    <Link
                        className="auth-create-button"
                        to="/signup"
                    >
                        Create an account
                    </Link>

                </div>


                <p className="auth-footer">
                    Learn. Review. Master.
                </p>

            </div>

        </div>
    );
}


export default Login;