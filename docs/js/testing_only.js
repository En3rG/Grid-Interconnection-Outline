setInterval(function(){ document.location.reload() },5000);
document.getElementById("DSP").style.backgroundColor = "blue";



setInterval(function()
	{ 
		setTimeout(function() 
		{
			alert("Hello!");
		}, 5000); 
	},5000);
	
function drawing() {

	//do stuff, then

	setTimeout(function () {
		drawing_two();
	}, 1000);

}

//just need setTimeout for each LRU connections