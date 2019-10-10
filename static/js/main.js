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
  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [
        {
          data: data.predictions.map(p => Number(p).toFixed(2)),
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

requestLastBarnImage()