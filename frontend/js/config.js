const API_BASE_URL = "http://192.168.1.74:8000"


/**
 * function for handling expired tokens
 */
async function authenticatedFetch(url, options = {}) {

    const response = await fetch(url, options);

    if (response.status === 401) {

        localStorage.removeItem("token");

        alert(
            "Session expired. Please log in again."
        );

        window.location.href =
            "login.html";

        throw new Error("Unauthorized");
    }

    return response;
}



