window.onbeforeunload = function (event) {
	event.preventDefault();
	event.returnValue = '';
	alert(event.target.toString());
	console.log(event);
	console.log(event.currentTarget.location.href);
	return false;
}

// Getting all of the hrefs
var links = [];
var a = document.getElementsByTagName('a');
for (var i = 0; i < a.length; i++) {
	if (a[i].href) {
		links.push(a[i].href);
	}
}


// Communicating with Python backend
fetch(
	'https://lamp.computerstudi.es/~Kyler1220041/hackathon/interface.php', 
	{
		method: 'POST',
		body: new URLSearchParams({
			"links": JSON.stringify(links)
		}),
		headers: {
			'Content-Type': 'text/plain'
		}
	}
).then(response => {
	return response
}).then((data) => {
	console.log(data, "END")
}).catch((error) => {
	console.log(error)
});
