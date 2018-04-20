window.onload = function() {
	
	$("#laheta").on("click", lisaa_tietokantaan);
	
	$("#muuta").on("click", hae_viestit);
	
	//$(".poista").on("click", poista_tietokannasta)
 
	
	//oikeudet();
	
	hae_viestit(); // vois ottaa parametrinä asetuksista viestien määrän
}

function poista_tietokannasta(e) {
	apuid = $(this).attr("id");
	console.log(apuid);

$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/poista_tietokannasta",
        type: "POST",
        dataType: "text",
		
		data: { "id":apuid,
        },
        
        success: poistaminen_onnistui,
        error: ajax_virhe
});	
	
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

function lisaa_tietokantaan(e) {
e.preventDefault();
$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/lisaa_tietokantaan",
        type: "POST",
        dataType: "text",
		
		data: { "nimi":$("#nimi").val(),
        "viesti":$("#viesti").val(),
        },
        
        success: lisaaminen_onnistui,
        error: ajax_virhe
});	
}

function oikeudet() {
	// submit nappulat näkyviin jos oikeudet
	// admin ominaisuudet näkyviin jos lisää oikeuksia
	
	
}

function lisaaminen_onnistui(data, textStatus, request) {
	console.log( data );
	hae_viestit();
}

function poistaminen_onnistui(data, textStatus, request) {
	console.log( data );
	hae_viestit();
}

function lisaa_viestit(data, textStatus, request) {
	$('#taulu').replaceWith( data );
	console.log( data );
	$(".poista").on("click", poista_tietokannasta)
}

function ajax_virhe(xhr, status, error) {
        console.log( "Error: " + error );
        console.log( "Status: " + status );
        console.log( xhr );
}