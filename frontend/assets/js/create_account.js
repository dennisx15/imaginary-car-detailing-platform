const form = document.getElementById("create-account-form");
form.addEventListener("submit", async (event) => {
    event.preventDefault(); // prevent the default form submission behavior, which would cause a page reload
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const response = await authenticatedFetch(
        `${API_BASE_URL}/register`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }
    );
    const data = await response.json();
    console.log(data);
    if (response.ok) {
        alert("Account created successfully! Please log in.");
        window.location.href = "login.html";
    } else {
        alert("Account creation failed: " + data.message);
    }
});