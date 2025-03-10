// Function to handle user login
async function login() {
    try {
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        // Input validation
        if (!username || !password) {
            alert("Please fill in all fields");
            return;
        }

        const response = await fetch("http://127.0.0.1:8000/auth/login/", {
            method: "POST",
            credentials: 'include',  // Important for cookies
            headers: { 
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.message === "Login successful") {
            if (data.token) {
                localStorage.setItem("token", data.token);
            }
            window.location.href = "/dashboard";  // Use relative path
        } else {
            throw new Error(data.error || "Login failed");
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`Login failed: ${error.message}`);
    }
}

// Function to handle user registration
async function register() {
    try {
        let username = document.getElementById("regUsername").value;
        let email = document.getElementById("regEmail").value;
        let password = document.getElementById("regPassword").value;

        // Input validation
        if (!username || !email || !password) {
            alert("Please fill in all fields");
            return;
        }

        // Basic email validation
        if (!email.includes('@') || !email.includes('.')) {
            alert("Please enter a valid email address");
            return;
        }

        const response = await fetch("http://127.0.0.1:8000/auth/register/", {
            method: "POST",
            credentials: 'include',  // Important for cookies
            headers: { 
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({ username, email, password })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.message === "User registered successfully") {
            alert("Registration Successful! Please login.");
            window.location.href = "/login";  // Redirect to login page
        } else {
            throw new Error(data.error || "Registration failed");
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`Registration failed: ${error.message}`);
    }
}

// Function to toggle between login and register forms
function toggleForms() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    if (loginForm.style.display === 'none') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    }
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}