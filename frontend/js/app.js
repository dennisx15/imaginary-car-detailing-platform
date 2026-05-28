const form = document.getElementById("appointment-form");

form.addEventListener("submit", async (event) => {//This function will run when the submit button is pressed

    event.preventDefault(); // prevents the default form submission behavior, which would cause a page reload

    //extract the values from the form fields and store them in variables
    const name = document.getElementById("name").value;
    const service = document.getElementById("service").value;
    const phone_number = document.getElementById("phone_number").value;
    const notes = document.getElementById("notes").value;
    const token = localStorage.getItem("token");

    
const response = await fetch( // fetch waits for backend response before moving on to next line of code
        "http://127.0.0.1:8000/appointments",//this is the backend endpoint we want to send data to
        {
            method: "POST", // the kind of http request we want to send

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }, // some metadata about the request, in this case we are saying we are sending JSON data

            body: JSON.stringify({
                name: name,
                phone_number: phone_number,
                service: service,
                notes: notes,
            }) // this is the actual data we want to send. We create a JavaScript object with the name and service, then convert it to a JSON string with JSON.stringify
        }
    );

    const data = await response.json(); // we wait for the response from the backend and then parse it as JSON. The backend will send back a JSON object with a message and the id of the new appointment.

    console.log(data); // we log the response data to the console. In a real application, you might want to update the UI to show a success message or clear the form fields instead of just logging the response.

});

async function loadAppointments() {
    const response = await fetch("http://127.0.0.1:8000/my-appointments",
        {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`,
                method: "GET"
            }
        }
    );
    const appointments = await response.json();

    const container = document.getElementById("appointments-container"); // get the container element in html where we want to display the appointments

    appointments.forEach(appointment => {
        const appointmentElement = document.createElement("div");// create a new div element for each appointment
        appointmentElement.innerHTML = `
            <h3>${appointment.name}</h3>
            <p>Phone: ${appointment.phone_number}</p>
            <p>Service: ${appointment.service}</p>
            <p>Notes: ${appointment.notes}</p>
            <button onclick="deleteAppointment(${appointment.id})">
            Delete
            </button>
        `;// set the inner HTML of the appointment element to show the name and service of the appointment. We use template literals to insert the appointment data into the HTML string.
        container.appendChild(appointmentElement);// add the appointment element to the container in the HTML so it will be displayed on the page
    });
}
loadAppointments()

async function deleteAppointment(id){

    const token = localStorage.getItem("token");
    await fetch(

        `http://127.0.0.1:8000/my-appointments/${id}`,

        {
            method: "DELETE",

            headers: {
                "Authorization":
                    `Bearer ${token}`
            }
        }
    );

    location.reload();
}