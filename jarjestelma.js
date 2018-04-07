window.onload = function {
	
	$("#laheta").on("click", lisaa_tietokantaan);
	
	$("#muuta").on("click", hae_viestit);
	
	oikeudet;()
	
	hae_viestit(); // vois ottaa parametrinä asetuksista viestien määrän
}

function hae_viestit() {
	var kentat = document.getElementsByName("maara");
	var kentta = kentat[0];
	var luku = kentta.value;
	
	var kentat2 = document.getElementsByName("maara2");
	var kentta2 = kentat2[0];
	var luku2 = kentta2.value;
}

function oikeudet() {
	// submit nappulat näkyviin jos oikeudet
	// admin ominaisuudet näkyviin jos lisää oikeuksia
	
	
}