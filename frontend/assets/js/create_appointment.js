const form = document.getElementById("appointment-form");
let selectedSlot = null;
let selectedTime = null;

form.addEventListener("submit", async (event) => {//This function will run when the submit button is pressed

    event.preventDefault(); // prevents the default form submission behavior, which would cause a page reload

    //extract the values from the form fields and store them in variables
    //const name = document.getElementById("name").value;
    //const service = document.getElementById("service").value;
    //const phone_number = document.getElementById("phone_number").value;
    //const notes = document.getElementById("notes").value;
    //const appointment_time = document.getElementById("appointment_time").value;
    //const token = localStorage.getItem("token");
    //const fullDateTime = `${appointment_time}T${selectedTime}`; // combine the date and time into a single string in ISO format

    const serviceId = parseInt(document.getElementById("service_id").value); // Convert the string "1", "2", or "3" into an integer
    const name = document.getElementById("name").value;
    const phone_number = document.getElementById("phone_number").value;
    const notes = document.getElementById("notes").value;
    const appointment_time = document.getElementById("appointment_time").value;
    const token = localStorage.getItem("token");
    const fullDateTime = `${appointment_time}T${selectedTime}`;


    
const response = await authenticatedFetch( // fetch waits for backend response before moving on to next line of code
        `${API_BASE_URL}/appointments`,//this is the backend endpoint we want to send data to
        {
            method: "POST", // the kind of http request we want to send

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }, // some metadata about the request, in this case we are saying we are sending JSON data

            body: JSON.stringify({
                name: name,
                phone_number: phone_number,
                service_id: serviceId,
                notes: notes,
                date: fullDateTime
            }) // this is the actual data we want to send. We create a JavaScript object with the name and service, then convert it to a JSON string with JSON.stringify
        }
    );

    const data = await response.json(); // we wait for the response from the backend and then parse it as JSON. The backend will send back a JSON object with a message and the id of the new appointment.

    if (!response.ok) {
        alert(data.detail);
        location.reload();
        return;
    }

    alert("Appointment booked successfully!");
    location.reload(); // after successfully creating the appointment, we reload the page to show the updated list of appointments. In a real application, you might want to update the UI dynamically instead of reloading the page.


    console.log(data); // we log the response data to the console. In a real application, you might want to update the UI to show a success message or clear the form fields instead of just logging the response.

});



/**
 * This function will load the available time slots for a given date when the user selects a date from the date input field. It sends a GET request to the backend with the selected date, and the backend responds with a JSON object that indicates which time slots are available. The function then creates buttons for each time slot and disables the buttons for the unavailable slots. When a user clicks on an available time slot button, it highlights the selected button and stores the selected time in a variable.
 */

async function loadAvailableSlots() {

    const appointment_time = document.getElementById("appointment_time").value;
    if (!appointment_time) {return;}

    console.log(appointment_time);
    const response = await authenticatedFetch(`${API_BASE_URL}/appointments/slots/${appointment_time}`);

    console.log(response.status);
    const slots = await response.json();

    const container =
    document.getElementById("slots-container");

    container.innerHTML = "";
    for (const slot in slots) {
        const button =
        document.createElement("button");
        button.innerText = slot;
        if (!slots[slot]) {
            button.disabled = true;
            button.style.backgroundColor ="gray";
            } // if the slot is not available, disable the button and change its color to gray
            
        button.addEventListener("click", () => {
            selectedTime = slot;
            if (selectedSlot) {
                selectedSlot.style.backgroundColor = "";
            }
            button.style.backgroundColor = "lightblue";
            selectedSlot = button;
            });
        container.appendChild(button);
        }};

        
document.getElementById(
    "appointment_time").
    addEventListener(
        "change",
        loadAvailableSlots);

const today =
    new Date().toISOString().split("T")[0];

document.getElementById(
    "appointment_time"
).value = today;

loadAvailableSlots();


