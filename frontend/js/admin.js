async function loadAppointments() {
    const response = await fetch("http://127.0.0.1:8000/appointments");
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
    await fetch(`http://127.0.0.1:8000/appointments/${id}`, 
        {
        method: "DELETE"
    }
    );
    location.reload();
}