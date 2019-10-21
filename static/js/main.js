const lastBarnImage = document.querySelector('.last-barn-image img')
const lastBarnDatetime = document.querySelector('.last-barn-datetime')
const lastSegmentationImage = document.querySelector('.last-segmentation-image img')
const lastSegmentationFeatures = document.querySelector('.last-segmentation-features')
const scene_recognition_labels = [
  "Normal situation",
  "Aggression frontal",
  "Aggression lateral",
  "Aggression vertical",
  "Aggression overtaking",
  "Curiosity",
  "Queuing fewer",
  "Queuing crowded",
  "Drinking water",
  "Low visibility"
]

startApp()

function startApp() {
  requestBarnInfo()
  chartStatistics()
  loadSensorDatas()
}

function requestBarnInfo() {
  fetch('/barn/images/last/info')
    .then(res => res.json())
    .then(json => loadInfo(json))
}

function loadInfo(image) {
  loadLastBarnImage(image)
  loadSceneRecognation(image)
}

// Last Barn Image
function loadLastBarnImage(image) {
  lastBarnImage.src = `/barn/images/${image.id}`
  lastBarnDatetime.innerHTML = getLastBarnDatetime(image.datetime, image.camera)
  lastSegmentationImage.src = `/barn/instancesegmentation/${image.id}/image`
  lastSegmentationImage.addEventListener('load', () => loadLastInstanceSegmentation(image.id))
  setTimeout(requestBarnInfo, 60000) // 1 minute
}

function getLastBarnDatetime(datetime, camera) {
  date = datetime.split('T')[0].replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1')
  time = datetime.split('T')[1]
  return `<i class="far fa-calendar"></i>
   <span class="image-date">${date}</span>
   <i class="far fa-clock pl-4"></i>
   <span class="image-date">${time}</span>
   <i class="fas fa-video pl-4"></i>
   <span class="image-date">${camera}</span>`
}

// Scene Recognation
function loadSceneRecognation(image) {
  fetch(`/barn/scenerecognition/${image.id}`)
    .then(res => res.json())
    .then(json => chartSceneRecognation(json))
}

function chartSceneRecognation(data) {
  loadLatestSceneRecognation()
  const ctx = document.getElementById('chartSceneRecognation')
  const values = [
    data.normal_situation,
    data.aggression_frontal,
    data.aggression_lateral,
    data.aggression_vertical,
    data.aggression_overtaking,
    data.curiosity,
    data.queuing_fewer,
    data.queuing_crowded,
    data.drinking_water,
    data.low_visibility
  ]
  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: scene_recognition_labels,
      datasets: [
        {
          data: values.map(p => Number(p).toFixed(2)),
          backgroundColor: ['#A0522D', '#C0C0C0', '#8E5EA2', '#40E0D0', '#0000CD', '#DC143C', '#3E95CD', '#00FFFF', '#98FB98', '#B0E0E6'],
          borderWidth: 1
        }
      ]
    },
    options: {
      legend: {
        display: false
      },
      scales: {
          yAxes: [{
              ticks: {
                  beginAtZero: true
              }
          }]
      }
    }
  })
}

function loadLatestSceneRecognation() {
  fetch('/barn/scenerecognition')
    .then(res => res.json())
    .then(json => chartClasses(json))
}

function chartClasses(data) {
  // TODO top10 https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
  const ctx = document.getElementById('chartClasses')
  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(r => r.image.datetime.replace(/(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)/, '$2/$3 $4:$5')),
      datasets: [{ 
          data: data.map(r => r.normal_situation),
          label: "Class 0",
          backgroundColor: "#A0522D",
          borderColor: "#A0522D",
          fill: false
        },{ 
          data: data.map(r => r.aggression_frontal),
          label: "Class 1",
          backgroundColor: "#C0C0C0",
          borderColor: "#C0C0C0",
          fill: false
        }, { 
          data: data.map(r => r.aggression_lateral),
          label: "Class 2",
          backgroundColor: "#8E5EA2",
          borderColor: "#8E5EA2",
          fill: false
        }, { 
          data: data.map(r => r.aggression_vertical),
          label: "Class 3",
          backgroundColor: "#40E0D0",
          borderColor: "#40E0D0",
          fill: false
        }, { 
          data: data.map(r => r.aggression_overtaking),
          label: "Class 4",
          backgroundColor: "#0000CD",
          borderColor: "#0000CD",
          fill: false
        }, { 
          data: data.map(r => r.curiosity),
          label: "Class 5",
          backgroundColor: "#DC143C",
          borderColor: "#DC143C",
          fill: false
        }, { 
          data: data.map(r => r.queuing_fewer),
          label: "Class 6",
          backgroundColor: "#3E95CD",
          borderColor: "#3E95CD",
          fill: false
        }, { 
          data: data.map(r => r.queuing_crowded),
          label: "Class 7",
          backgroundColor: "#00FFFF",
          borderColor: "#00FFFF",
          fill: false
        }, { 
          data: data.map(r => r.drinking_water),
          label: "Class 8",
          backgroundColor: "#98FB98",
          borderColor: "#98FB98",
          fill: false
        }, { 
          data: data.map(r => r.low_visibility),
          label: "Class 9",
          backgroundColor: "#B0E0E6",
          borderColor: "#B0E0E6",
          fill: false
        }
      ]
    },
    options: {
    }
  });
}

function chartStatistics() {
  const ctx = document.getElementById('chartStatistics')
  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: scene_recognition_labels,
      datasets: [
        {
          data: [8.5, 0.2, 1.7, 0, 0, 9.5, 30.1, 24.9, 3.5, 21.7],
          backgroundColor: ["#3e95cd", "#3e95cd", "#3e95cd", "#3e95cd", "#3e95cd", "#3e95cd", "#3e95cd", "#3e95cd", "#3e95cd", "#3e95cd"],
          borderWidth: 1
        }
      ]
    },
    options: {
      legend: {
        display: false
      },
      scales: {
          yAxes: [{
              ticks: {
                  beginAtZero: true,
                  callback: function(value) {
                    return (value / 800 + '%');
                }
              }
          }]
      }
    }
  })
}

// Instance segmentation
function loadLastInstanceSegmentation(id) {
  fetch(`/barn/instancesegmentation/${id}/features`)
    .then(res => res.json())
    .then(json => updateLastInstanceSegmentationFeatures(json))
}

function updateLastInstanceSegmentationFeatures(data) {
  lastSegmentationFeatures.innerHTML = `<i class="fas fa-wine-bottle"></i>
   <span class="image-milk">${data.isMilk ? 'A cow is milking' : 'No cow is milking'}</span>
   <i class="fas fa-horse pl-4"></i>
   <span class="image-cows">${data.n_cows}</span>
   <i class="fas fa-male pl-4"></i>
   <span class="image-humans">${data.n_humans}</span>`
}

// Sensors
function loadSensorDatas() {
  fetch('/barn/sensors/A81758FFFE03580D')
    .then(res => res.json())
    .then(json => chartSensors(json))
}

function chartSensors(data) {
  const ctx = document.getElementById('chartSensors')
  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.timestamp,
      datasets: [{ 
          data: data.temperature,
          label: "Temperature",
          backgroundColor: "#3e95cd",
          borderColor: "#3e95cd",
          fill: false
        }, { 
          data: data.humidity,
          label: "Humidity",
          backgroundColor: "#8e5ea2",
          borderColor: "#8e5ea2",
          fill: false
        }, { 
          data: data.motion,
          label: "Motion",
          backgroundColor: "#3cba9f",
          borderColor: "#3cba9f",
          fill: false
        }
      ]
    },
    options: {
    }
  });
  setTimeout(loadSensorDatas, 900000) // 15 minutes
}
