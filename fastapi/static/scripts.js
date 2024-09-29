let chart;  // Declare chart variable globally
let historicalDates = [];
let historicalValues = [];

// Fetch historical data and store it in the global variables
async function fetchHistoricalData() {
    const response = await fetch('/historical_data/');
    const data = await response.json();  // No need for JSON.parse(), response.json() automatically parses it

    // Extract the dates and values from the historical data
    historicalDates = data.map(item => new Date(item.ds));  // Convert dates to Date objects
    historicalValues = data.map(item => item.y);  // Extract passenger values
}

// Fetch historical data on page load
window.addEventListener('load', async () => {
    await fetchHistoricalData();  // Ensure historical data is fetched before using it
});


// Function to fetch the forecast data from the backend
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
    const forecastDates = forecastData.map(item => new Date(item.ds));  // Convert to Date objects
    const forecastValues = forecastData.map(item => item.AutoARIMA);

    // Update the chart with both historical and forecast data
    updateChart(historicalDates, historicalValues, forecastDates, forecastValues);
}

// Function to update the chart with both historical and forecast data
function updateChart(historicalDates, historicalValues, forecastDates, forecastValues) {
    const ctx = document.getElementById('forecastChart').getContext('2d');

    if (chart) {
        chart.destroy();  // Destroy the existing chart to update with new data
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: historicalDates.concat(forecastDates),  // Combine historical and forecast dates for the x-axis
            datasets: [
                {
                    label: 'Historical Data',
                    data: historicalValues,
                    borderColor: '#4bc0c0',  // Line color for historical data
                    backgroundColor: '#4bc0c033',  // Line fill color for historical data (hex with transparency)
                    fill: false,
                    borderWidth: 2,
                    pointRadius: 3,  // Dots on historical data points
                    pointBackgroundColor: '#4bc0c0'
                },
                {
                    label: 'Forecast Data',
                    data: new Array(historicalValues.length).concat(forecastValues),  // Leave empty space for historical values
                    borderColor: '#ff6384',  // Line color for forecast data
                    backgroundColor: '#ff638433',  // Line fill color for forecast data (hex with transparency)
                    fill: false,
                    borderWidth: 2,
                    pointRadius: 3,  // Dots on forecast data points
                    pointBackgroundColor: '#ff6384'
                }
            ]
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
