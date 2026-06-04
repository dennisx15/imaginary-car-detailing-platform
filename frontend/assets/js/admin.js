async function loadAppointments() {
    const response = await fetch(`${API_BASE_URL}/appointments`);
    const appointments = await response.json();

    const container = document.getElementById("appointments-container"); // get the container element in html where we want to display the appointments

appointments.forEach(appointment => {
        const appointmentDate = new Date(appointment.date);

      //Format the date and time using clean, human-readable options
        const formattedDateTime = appointmentDate.toLocaleString('en-US', {
        weekday: 'short', // "Mon"
        year: 'numeric',  // "2026"
        month: 'short',   // "Jun"
        day: 'numeric',   // "1"
        hour: '2-digit',  // "09"
        minute: '2-digit' // "00"
    });
        const appointmentElement = document.createElement("div");// create a new div element for each appointment
        appointmentElement.innerHTML = `
            <h3>${appointment.name}</h3>
            <p>Phone: ${appointment.phone_number}</p>
            <p>Service: ${appointment.service.name}</p>
            <p>Description: ${appointment.service.description}</p>
            <p>Price: ${appointment.service.price}</p>
            <p>Notes: ${appointment.notes}</p>
            <p>Appointment: ${formattedDateTime}</p>
            <button onclick="deleteAppointment(${appointment.id})">
            Delete
            </button>
        `;// set the inner HTML of the appointment element to show the name and service of the appointment. We use template literals to insert the appointment data into the HTML string.
        container.appendChild(appointmentElement);// add the appointment element to the container in the HTML so it will be displayed on the page
    });
}
loadAppointments()

async function deleteAppointment(id){

    if (!confirm("Are you sure you want to cancel this car detailing appointment?")) {
        return;
    }

    try{
        const response = await fetch(`${API_BASE_URL}/appointments/${id}`, 
        {
        method: "DELETE"
    }
    );
    const data = await response.json(); // Wait to parse the text response message

    if (!response.ok) {
        alert(data.detail || "Failed to delete appointment.");
        return;
        }

        //Notify the user and reload the view to reflect the changes
        alert("Appointment successfully canceled!");
        location.reload(); // Simple way to refresh the page and show the updated list of appointments
    } catch (error) {
        console.error("Error during deletion:", error);
        alert("An error occurred while attempting to cancel the appointment.");
    }}
