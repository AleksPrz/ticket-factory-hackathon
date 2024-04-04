// Check if the APIs are supported 
// navigator and window are global objects

function checkSupport() {
	if (!('serviceWorker' in navigator)) {
		throw new Error("No support for service worker")
	}

	if (!('Notification' in window)) {
		throw new Error("No support for notification API")
	}

	if (!('PushManager' in window)) {
		throw new Error("No support for Push API")
	}
}

// SW = Service Worker
async function registerSW(url) {
	// We use the methods and properties of the navigator object
	const registration = await navigator.serviceWorker.register('service_worker.js')
	
	// Esperar hasta que el service worker esté activo
	while (!registration.active) {
		await new Promise(resolve => setTimeout(resolve, 10)); // Esperar 100ms antes de volver a verificar
	}
	
	registration.active.postMessage({ url_data: url });

	return registration
}

// Show the popup to ask for notification permission
async function requestPermission() {
	// The notification object is at global scope
	const permission = await Notification.requestPermission()

    if (permission !== 'granted') {
        throw new Error("Notification permission not granted")
    } 
}

async function main(url) {
	try {
		checkSupport()
		await requestPermission()
		await registerSW(url)
	} catch (error) {
		console.log(error.message)
	}
}