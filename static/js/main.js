const lastBarnImage = document.querySelector('.last-barn-image img')
const lastBarnDatetime = document.querySelector('.last-barn-datetime')
let chart 

function requestLastBarnImage() {
  fetch('/barn/lastimage/info')
    .then(res => res.json())
    .then(json => loadInfo(json))
}

function loadInfo(image) {
  loadLastBarnImage(image)
  loadSceneRecognation(image)
}

function loadLastBarnImage(image) {
  lastBarnImage.src = `/barn/lastimage?ftp=${image.path}`
  lastBarnDatetime.innerHTML = getLastBarnDatetime(image.datetime, image.camera)
  setTimeout(requestLastBarnImage, 5000)
}

function getLastBarnDatetime(image, camera) {
  return `<i class="far fa-calendar"></i>
   <span class="image-date">${image.date}<span>
   <i class="far fa-clock pl-4"></i>
   <span class="image-date">${image.time}<span>
   <i class="fas fa-video pl-4"></i>
   <span class="image-date">${camera}<span>`
}

function chartSceneRecognation(data) {
  const ctx = document.getElementById('chartSceneRecognation')
  //console.log(data)
  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [
        {
          data: data.predictions.map(p => Number(p).toFixed(2)),
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
                  beginAtZero: true
              }
          }]
      }
    }
  })
}

function loadSceneRecognation(image) {
  fetch(`/barn/scenerecognition?ftp=${image.path}`)
    .then(res => res.json())
    .then(json => chartSceneRecognation(json))
}

function chartStatistics() {
  const ctx = document.getElementById('chartStatistics')
  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [
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
      ],
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

function chartSensors() {
  const ctx = document.getElementById('chartSensors')
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [50,60,70,75,80,85,90,95,98,99],
      datasets: [{ 
          data: [86,114,106,106,107,111,133,221,783,2478],
          label: "Temperature",
          borderColor: "#3e95cd",
          fill: false
        }, { 
          data: [282,350,411,502,635,809,947,1402,3700,5267],
          label: "Humidity",
          borderColor: "#8e5ea2",
          fill: false
        }, { 
          data: [168,170,178,190,203,276,408,547,675,734],
          label: "Motion",
          borderColor: "#3cba9f",
          fill: false
        }
      ]
    },
    options: {
    }
  });
}

function chartClasses() {
  const ctx = document.getElementById('chartClasses')
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [50,60,70,75,80,85,90,95,98,99],
      datasets: [{ 
          data: [5,3,4,3,2,1,1,1,2,2],
          label: "Class 0",
          borderColor: "#3e95cd",
          fill: false
        },{ 
          data: [4,3,4,5,6,5,4,3,5,3],
          label: "Class 1",
          borderColor: "#3e95cd",
          fill: false
        }, { 
          data: [0,0,0,0,0,0,1,0,0,0],
          label: "Class 2",
          borderColor: "#8e5ea2",
          fill: false
        }, { 
          data: [0,0,1,0,2,2,2,0,0,0],
          label: "Class 3",
          borderColor: "#3cba9f",
          fill: false
        }, { 
          data: [0,0,1,0,2,2,2,0,0,0],
          label: "Class 4",
          borderColor: "#3cba9f",
          fill: false
        }, { 
          data: [0,0,1,0,2,3,2,0,0,0],
          label: "Class 5",
          borderColor: "#3cba9f",
          fill: false
        }, { 
          data: [0,0,1,0,0,2,2,0,0,0],
          label: "Class 6",
          borderColor: "#3cba9f",
          fill: false
        }, { 
          data: [1,0,1,0,2,2,2,0,0,0],
          label: "Class 7",
          borderColor: "#3cba9f",
          fill: false
        }, { 
          data: [0,0,1,0,2,2,2,0,0,1],
          label: "Class 8",
          borderColor: "#3cba9f",
          fill: false
        }, { 
          data: [0,0,1,0,2,2,0,0,3,2],
          label: "Class 9",
          borderColor: "#3cba9f",
          fill: false
        }
      ]
    },
    options: {
    }
  });
}


requestLastBarnImage()
chartStatistics()
chartSensors()
chartClasses()