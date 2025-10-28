function getWeather() {
    const location = document.getElementById('location').value;
    fetch(`http://127.0.0.1:5000/weather?location=${location}`)
        .then(response => response.json())
        .then(data => {
            console.log('Received data:', data);
            if (data.error) {
                document.getElementById('result').innerHTML = `<p>${data.error}</p>`;
                return;
            }
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
            console.log('Received data:', data);
            if (data.error) {
                document.getElementById('result').innerHTML = `<p>${data.error}</p>`;
                return;
            }
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

// CRUD Functions
function createRecord() {
    const location = document.getElementById('location').value;
    const start_date = document.getElementById('start_date').value;
    const end_date = document.getElementById('end_date').value;
    if (!location || !start_date || !end_date) {
        alert("Location, start date, and end date required");
        return;
    }
    fetch('http://127.0.0.1:5000/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({location, start_date, end_date})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            document.getElementById('result').innerHTML = `<p>Record created with ID: ${data.id}</p>`;
        }
    })
    .catch(error => console.error('Error:', error));
}

function readRecords() {
    fetch('http://127.0.0.1:5000/read')
        .then(response => response.json())
        .then(data => {
            let html = '<h2>Stored Records</h2><table><tr><th>ID</th><th>Location</th><th>Start</th><th>End</th><th>Temps</th></tr>';
            data.forEach(record => {
                html += `<tr><td>${record.id}</td><td>${record.location}</td><td>${record.start}</td><td>${record.end}</td><td>${record.temps}</td></tr>`;
            });
            html += '</table>';
            document.getElementById('result').innerHTML = html;
        });
}

function updateRecord() {
    const id = document.getElementById('record_id').value;
    const location = document.getElementById('location').value;
    if (!id || !location) {
        alert("Record ID and new location required");
        return;
    }
    fetch(`http://127.0.0.1:5000/update/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({location})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            document.getElementById('result').innerHTML = `<p>Record updated successfully</p>`;
        }
    });
}

function deleteRecord() {
    const id = document.getElementById('record_id').value;
    if (!id) {
        alert("Record ID required");
        return;
    }
    fetch(`http://127.0.0.1:5000/delete/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            document.getElementById('result').innerHTML = `<p>Record deleted successfully</p>`;
        }
    });
}

// Export CSV
function exportCSV() {
    fetch('http://127.0.0.1:5000/export/csv')
        .then(response => response.text())
        .then(csv => {
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'weather_records.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        })
        .catch(error => {
            console.error('Export error:', error);
            document.getElementById('result').innerHTML = `<p>Error exporting CSV</p>`;
        });
}

document.getElementById('info').addEventListener('click', () => {
    alert("Product Manager Accelerator: Check our LinkedIn page for company description.");
});
