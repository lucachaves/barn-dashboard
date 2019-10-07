const lastBarnImage = document.querySelector('.last-barn-image img')
const lastBarnDatetime = document.querySelector('.last-barn-datetime')

function requestLastBarnImage() {
  fetch('/barn/lastimage/info')
    .then(res => res.json())
    .then(json => loadLastBarnImage(json))
}

function loadLastBarnImage(image) {
  lastBarnImage.src = `/barn/lastimage?ftp=${image.path}`
  lastBarnDatetime.innerHTML = getLastBarnDatetime(image.datetime, image.camera)
  // setTimeout(requestLastBarnImage, 10000)
}

function getLastBarnDatetime(image, camera) {
  return `<i class="far fa-calendar"></i>
   <span class="image-date">${image.date}<span>
   <i class="far fa-clock pl-4"></i>
   <span class="image-date">${image.time}<span>
   <i class="fas fa-video pl-4"></i>
   <span class="image-date">${camera}<span>`
}

requestLastBarnImage()