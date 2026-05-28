const form = document.getElementById("create-account-form");
form.addEventListener("submit", async (event) => {
    event.preventDefault(); // prevent the default form submission behavior, which would cause a page reload
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const response = await fetch(
        `http://127.0.0.1:8000/register`,
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
    if (response.ok) {
        alert("Account created successfully! Please log in.");
        window.location.href = "login.html";
    } else {
        alert("Account creation failed: " + data.message);
    }
});