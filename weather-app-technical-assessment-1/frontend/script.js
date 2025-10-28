function getWeather() {
    const location = document.getElementById('location').value;
    fetch(`http://127.0.0.1:5000/weather?location=${location}`)
        .then(response => response.json())
        .then(data => {
            console.log('Received data:', data);  // Add this to log the full response
            if (data.error) {
                document.getElementById('result').innerHTML = `<p>${data.error}</p>`;
                return;
            }
            // Rest of the code...
            const iconUrl = `http://openweathermap.org/img/wn/${data.icon}@2x.png`;
            document.getElementById('result').innerHTML = `
                <h2>${data.location}</h2>
                <p>Temperature: ${data.temp}°C</p>
                <p>${data.description}</p>
                <img src="${iconUrl}" alt="Weather icon">
            `;
        });
}

function getForecast() {
    const location = document.getElementById('location').value;
    fetch(`http://127.0.0.1:5000/forecast?location=${location}`)
        .then(response => response.json())
        .then(data => {
            console.log('Received data:', data);  // Added for consistency
            if (data.error) {
                document.getElementById('result').innerHTML = `<p>${data.error}</p>`;
                return;
            }
            // Rest of the code...
            let html = '<h2>5-Day Forecast</h2>';
            data.forEach(day => {
                const iconUrl = `http://openweathermap.org/img/wn/${day.icon}@2x.png`;
                html += `<p>${day.date}: ${day.temp}°C - ${day.description} <img src="${iconUrl}" alt="icon"></p>`;
            });
            document.getElementById('result').innerHTML = html;
        });
}

function getCurrentLocationWeather() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const location = `${position.coords.latitude},${position.coords.longitude}`;
            document.getElementById('location').value = location;
            getWeather();
        });
    } else {
        alert("Geolocation not supported");
    }
}

document.getElementById('info').addEventListener('click', () => {
    alert("Product Manager Accelerator: Check our LinkedIn page for company description.");
});