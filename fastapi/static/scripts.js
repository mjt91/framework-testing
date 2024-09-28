let chart;  // Declare chart variable globally

async function getForecast() {
    const periods = document.getElementById("periods").value;

    // Fetch forecast data from the backend
    const response = await fetch("/forecast/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ periods: parseInt(periods) })
    });

    const forecastData = await response.json();

    // Extract dates and forecasted values from the forecastData
    const forecastValues = forecastData.map(item => item.AutoARIMA);
    const forecastDates = forecastData.map(item => new Date(item.ds));  // Convert to Date objects

    // Update the chart with forecast data
    updateChart(forecastDates, forecastValues);
}

// Function to update the chart with new data
function updateChart(dates, values) {
    const ctx = document.getElementById('forecastChart').getContext('2d');

    if (chart) {
        chart.destroy();  // Destroy the existing chart to update with new data
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,  // x-axis will be the dates
            datasets: [{
                label: 'AirPassengers Forecast',
                data: values,
                borderColor: '#ff6384', // Line color
                backgroundColor: '#ff6384', // Line fill color
                fill: false,
                borderWidth: 2,
                pointRadius: 5,  // Add dots on the data points (size of the dots)
                pointBackgroundColor: '#ff6384',  // Color of the dots
                pointBorderColor: '#ff6384',  // Border color of the dots
                pointHoverRadius: 7,  // Slightly larger dot on hover
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',  // x-axis is time-based
                    time: {
                        unit: 'month',
                        tooltipFormat: 'MMM YYYY'  // Tooltip format for months
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Passengers'
                    }
                }
            }
        }
    });
}