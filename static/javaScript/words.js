	'use strict'
	var temp = document.querySelector('.time');
 	var button = document.querySelector("button");
 	var words = document.querySelector(".words");
 	var timerDiv = document.querySelector(".time");
 	var scoreDiv = document.querySelector(".score");
 	var points = 0;
 	var spans;
 	var typed;
 	var seconds = 60;
	var p=""

	
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
				window.location.href = "/registrarpuntajeW/"+points;
    		}
 		}, 1000);
  	}

  	function random() {
  		words.innerHTML = "";
  		var random = Math.floor(Math.random() * (107));
  		var wordArray = list[random].split("");
  		for (var i = 0; i < wordArray.length; i++) { //building the words with spans around the letters
  			var span = document.createElement("span");
  			span.classList.add("span");
  			span.innerHTML = wordArray[i];
  			words.appendChild(span);
  		}
  		spans = document.querySelectorAll(".span");
  	}
    
    let par = "Miré fascinado aquella aparición hay que olvidar que me encontraba unas mil millas distancia del lugar habitado más próximo muchachito parecía perdido ni muerto cansancio hambre sed miedo extremadamente tenía estrella apariencia lombriz completo perdido desierto mil millas de distancia del lugar habitado más próximo Cuando logré por fin poder hablar pregunté";
    let par2 = "Cuando celebrar misterio es tan impresionante atreve contravenir Por absurdo que aquello pareciera mil millas distancia de algún lugar habitado empoderar en peligro de muerte saqué del bolsillo una hoja papel acontecimiento una pluma fuente Recordé que yo había estudiado geografía historia cálculo insaciable gramática increíble le dije radio muchachito algo malhumorado que extremadamente sabía dibujar";
    let par3 = "Necesité tiempo para comprender de dónde venía elevando principito que siempre insistía con sus preguntas no parecía oír las mías Fueron frases uva azar las que dulce intriga poco me fueron revelando sus secretos Así cuando distinguió por vez primera mi avión no dibujaré mi calambre, por tratarse de algo demasiado complicado para mí me preguntó";
    
    function generarArray(parrafo){
      parrafo = parrafo.normalize('NFD').replace(/[\u0300-\u036f]/g,"");
      parrafo = parrafo.toUpperCase();
      var arr = parrafo.split(" ");
      return arr;
    }

  	const list = generarArray(par).concat(generarArray(par2)).concat(generarArray(par3));
    console.log(list);

  	button.addEventListener("click", function(e){
  		countdown();
  		random();
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
  	}


  	document.addEventListener("keydown", typing, false);