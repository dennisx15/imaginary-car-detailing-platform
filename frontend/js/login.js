const form = document.getElementById("login-form");
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await authenticatedFetch(
        `${API_BASE_URL}/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                //TODO: remove user field and update backend to only require email and password for login
                password: password
            })
        }
    );
    const data = await response.json();
    console.log(data);

    if (!data.access_token) {
        alert("Login failed: " + data.message);
        return;
    }

    localStorage.setItem(
    "token",
    data.access_token);

    window.location.href = "index.html";// after successful login, we store the JWT token in localStorage and redirect the user to the index page. In a real application, you might want to show an error message if the login fails instead of just logging the response.

});

document.getElementById("create-account-button").addEventListener("click", async (event) => {
    event.preventDefault();
    window.location.href = "create_account.html";
});


