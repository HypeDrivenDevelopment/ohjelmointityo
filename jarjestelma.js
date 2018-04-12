window.onload = function() {
	
	//$("#laheta").on("click", lisaa_tietokantaan);
	
	$("#muuta").on("click", hae_viestit);
	
	oikeudet();
	
	hae_viestit(); // vois ottaa parametrinä asetuksista viestien määrän
}

function hae_viestit() {
	//var kentat = document.getElementsByName("maara");
	//var kentta = kentat[0];
	//var luku = kentta.value;
	
	//var kentat2 = document.getElementsByName("maara2");
	//var kentta2 = kentat2[0];
	//var luku2 = kentta2.value;
	
	//if maara =/= 0, maara n
	
$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/hae_viestit",
        type: "GET",
        dataType: "text",
        success: lisaa_viestit,
        error: ajax_virhe
});
}

function oikeudet() {
	// submit nappulat näkyviin jos oikeudet
	// admin ominaisuudet näkyviin jos lisää oikeuksia
	
	
}

function lisaa_viestit(data, textStatus, request) {
	$('#viestit').replaceWith( data );
	console.log( data );
}

function ajax_virhe(xhr, status, error) {
        console.log( "Error: " + error );
        console.log( "Status: " + status );
        console.log( xhr );
}