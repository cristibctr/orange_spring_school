const tempData = {
    labels: [
        'Temperature',
    ],
    datasets: [
        {
            label: 'Temperature',
            data: [],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
            ],
            hoverOffset: 4
        }
    ]
};
const humData = {
    labels: [
        'Humidity',
    ],
    datasets: [
        {
            label: 'Humidity',
            data: [],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
            ],
            hoverOffset: 4
        }
    ]
};
const CO2Data = {
    labels: [
        'CO2',
    ],
    datasets: [
        {
            label: 'CO2',
            data: [],
            backgroundColor: [
            'rgb(168, 209, 205)',
            'rgb(0, 0, 102)'
            ],
            hoverOffset: 4
        }
    ]
};
const presData = {
    labels: [
        'Pressure',
    ],
    datasets: [
        {
            label: 'Pressure',
            data: [],
            backgroundColor: [
            'rgb(153, 153, 255)',
            'rgb(0, 204, 255)'
            ],
            hoverOffset: 4
        }
    ]
};

const tempConfig = {
    type: 'doughnut',
    data: tempData,
};
const humConfig = {
    type: 'doughnut',
    data: humData,
};
const CO2Config = {
    type: 'doughnut',
    data: CO2Data,
};
const presConfig = {
    type: 'doughnut',
    data: presData,
};

const tempChart = new Chart(
    $('#tempChart'),
    tempConfig
);
const humChart = new Chart(
    $('#humChart'),
    humConfig
);
const presChart = new Chart(
    $('#presChart'),
    presConfig
);
const CO2Chart = new Chart(
    $('#CO2Chart'),
    CO2Config
);

async function fetchData() {
    devices = await fetch('/api/v0/devices');
    devices = await devices.json()
    for (device of devices) {
        if(device.id.includes("android"))
        {
            stream = await fetch('/api/v0/stream/' + device.id)
            stream = await stream.json()
            return fetch('/api/v0/telemetry/' + stream[0].streamId)
        }
    }
}
fetchData()
    .then(reqData => reqData.json())
    .then(function (reqData) {
        tempData.datasets[0].data = [reqData.temperature, 100 - reqData.temperature]
        humData.datasets[0].data = [reqData.humidity, 100 - reqData.humidity]
        CO2Data.datasets[0].data = [reqData.CO2, 2000 - reqData.CO2]
        presData.datasets[0].data = [reqData.pressure, 4000 - reqData.pressure]
        tempChart.update();
        humChart.update();
        CO2Chart.update();
        presChart.update();
    })
setInterval(function() {
    fetchData()
    .then(reqData => reqData.json())
    .then(function (reqData) {
        tempData.datasets[0].data = [reqData.temperature, 100 - reqData.temperature]
        humData.datasets[0].data = [reqData.humidity, 100 - reqData.humidity]
        CO2Data.datasets[0].data = [reqData.CO2, 2000 - reqData.CO2]
        presData.datasets[0].data = [reqData.pressure, 4000 - reqData.pressure]
        tempChart.update();
        humChart.update();
        CO2Chart.update();
        presChart.update();
    })
}, 4000);