/* eslint-env serviceworker */

console.log('Loading ServiceWorker.')

var baseDatetime = ''

self.addEventListener('install', function (event) {
  console.log('Installing ServiceWorker.')
})

self.addEventListener('activate', function (event) {
  console.log('Activating ServiceWorker.')
})

self.addEventListener('fetch', function (event) {
  console.log('Fetch event triggered.')
  console.log(event.request)
  var request = event.request

  // TODO: consult the referrer header on each request instead of using a global var
  if (event.request.mode !== 'navigate' &&
      event.request.url.indexOf('/webui/') === -1) { // Do not rewrite webui embedded resources
       // TODO: use a 3XX redirect to better guide the browser
       //  if hostname == refferrer, check to ensure serviceworker does not run infinitely on each embedded resource
    request = reroute(event.request, baseDatetime) // Only embedded resources
    console.log('REROUTING request for ' + event.request.url + ' to ' + request.url)
    console.log(event.request)
  } else if (event.request.mode === 'navigate') {
    // We need to preserve memento-datetime for use in requesting
    //  embedded resources. Possibly use SW caches instead? TODO
    var datetime = event.request.url.match(/\/([0-9]{14})\//)[1]
    baseDatetime = datetime
  }

  event.respondWith(
    fetch(request).then(serverFetch, serverFailure).catch(serverFailure)
  )

  function serverFetch (response) {
    console.log('Fetching from server.')
    console.log(response)
    return response
  }

  function serverFailure () {
    console.log('Fetching from server failed.')
    return new Response('<h1>Service Unavailable</h1>', {
      status: 503,
      statusText: 'Service Unavailable',
      headers: new Headers({
        'Content-Type': 'text/html'
      })
    })
  }

  function reroute (request, datetime) {
    return new Request(`http://127.0.0.1:5000/memento/${datetime}/${request.url}`) // TODO: Rm hard-code for server
  }
})
