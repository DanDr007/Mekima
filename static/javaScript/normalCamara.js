var temp = document.querySelector('.time');
var button = document.querySelector("button");
var words = document.querySelector(".words");
var timerDiv = document.querySelector(".time");
var scoreDiv = document.querySelector(".score");
var points = 0;
var spans;
var typed;
var seconds = 60;
var errores = 0;
var videoWidth = 320;
var videoHeight = 240;
var videoTag = document.getElementById('theVideo');
var canvasTag = document.getElementById('theCanvas');
var csrf = document.getElementsByName("csrfmiddlewaretoken")

videoTag.setAttribute('width', videoWidth);
videoTag.setAttribute('height', videoHeight);
canvasTag.setAttribute('width', videoWidth);
canvasTag.setAttribute('height', videoHeight);


	function countdown() {
		points = 0;
		var timer = setInterval(function(){
			button.disabled = true;
		   seconds--;
		   temp.innerHTML = seconds;
		   if (seconds === 0) {
		 alert("se acabó el tiempooooooo, tu puntuación es:  " + points);
			   scoreDiv.innerHTML = "0";
			   words.innerHTML = "";
			   button.disabled = false;
			   clearInterval(timer);
			   seconds = 60;
			   timerDiv.innerHTML = "60";
			   button.disabled = false;	
			   window.location.href = "/registrarpuntajeNCam/"+points+10-errores;
		   }
		}, 1000);
	 }

	function random() {
		words.innerHTML = "";
		var random = Math.floor(Math.random() * (36));
		var wordArray = list[random].split("");
		for (var i = 0; i < wordArray.length; i++) { //building the words with spans around the letters
			var span = document.createElement("span");
			span.classList.add("span");
			span.innerHTML = wordArray[i];
			words.appendChild(span);
		}
		spans = document.querySelectorAll(".span");
	}

	//  genera 300 caracteres aleatorios
	function array() {
	var result = [];
	var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
	var charactersLength = characters.length;
		for ( var i = 0; i < 300; i++ ) {
	   		result += characters.charAt(Math.floor(Math.random() * charactersLength));
		}
	return result.split("");
	}
	
	const list = array();
	console.log(list);

	button.addEventListener("click", function(e){
		countdown();
		random();
		loadCamera();
		button.disabled = true;	
	});

	function typing(e) {
		typed = String.fromCharCode(e.which);
		for (var i = 0; i < spans.length ; i++) {
			if (spans[i].innerHTML === typed) { // if typed letter is the one from the word
				if (spans[i].classList.contains("bg")) { // if it already has class with the background color then check the next one
					continue;
				} else if (spans[i].classList.contains("bg") === false && spans[i-1] === undefined || spans[i-1].classList.contains("bg") !== false ) { // if it dont have class, if it is not first letter or if the letter before it dont have class (this is done to avoid marking the letters who are not in order for being checked, for example if you have two "A"s so to avoid marking both of them if the first one is at the index 0 and second at index 5 for example)
					spans[i].classList.add("bg");
					break;
				}
			}
		}
		var checker = 0;
		for (var j = 0; j < spans.length; j++) { //checking if all the letters are typed
			if (spans[j].className === "span bg") {
				checker++;
			}
			if (checker === spans.length) { // if so, animate the words with animate.css class
				words.classList.add("animated");
				words.classList.add("fadeOut");
				points++; // increment the points
				scoreDiv.innerHTML = points; //add points to the points div
				document.removeEventListener("keydown", typing, false);
				setTimeout(function(){
					words.className = "words"; // restart the classes
					random(); // give another word
					document.addEventListener("keydown", typing, false);
				}, 400);
			}

		}
		var canvasContext = canvasTag.getContext('2d');
		canvasContext.drawImage(videoTag, 0, 0, videoWidth, videoHeight);
		  var data = canvasTag.toDataURL("image/png")
		  console.log("presionada: "+e.key)
		  $.ajax({
			headers:{
				"X-CSRFToken": getCookie("csrftoken")
			  },
			type: 'POST',
			url: '/jugarNormal/',
			data: {
			  imagen: data,
			  letra: e.key
			},
			dataType: 'json',
			success: function (response) {
			  errores += parseInt(response.errores)
			  console.log(errores)
			  document.getElementById("errores").innerHTML = errores
			  document.getElementById("estado").innerHTML = response.estado
			}
		  })
}

document.addEventListener("keydown", typing, false);

//hands

//variables

function loadCamera() {
	navigator.mediaDevices.getUserMedia({
		audio: false,
		video: {
		  width: videoWidth,
		  height: videoHeight
		}}).then(stream => {
		  videoTag.srcObject = stream;
		}).catch(e => {
		  document.getElementById('errorTxt').innerHTML = 'ERROR: ' + e.toString();
		});

};