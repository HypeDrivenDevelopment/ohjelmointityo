window.onload = function() {
	
	$("#laheta").on("click", lisaa_tietokantaan);
	
	$("#muuta").on("click", muuta_asetukset);
	
	$("#send").on("click", lisaa_chattietokantaan);
	
	//$(".poista").on("click", poista_tietokannasta)
 
	
	//oikeudet();
	
	hae_viestit();
	
	hae_chat();
}

function lisaa_chattietokantaan(e) {
e.preventDefault();
$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/lisaa_chattietokantaan",
        type: "POST",
        dataType: "text",
		
		data: { "message":$("#message").val(),
        },
        
        success: chatlisaaminen_onnistui,
        error: ajax_virhe
});	
}

function hae_chat() {
$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/hae_chat",
        type: "GET",
        dataType: "text",
        success: lisaa_chat,
        error: ajax_virhe
});
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

function muuta_asetukset(e) {
e.preventDefault();
hae_viestit();
}

function hae_viestit() {
$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/hae_viestit",
        type: "POST",
        dataType: "text",
		data: { "maara":$("#maara").val(),
		},
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

function chatlisaaminen_onnistui(data, textStatus, request) {
	console.log( data );
	hae_chat();
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

function lisaa_chat(data, textStatus, request) {
	$('#chatviestit').replaceWith( data );
	console.log( data );
}

function ajax_virhe(xhr, status, error) {
        console.log( "Error: " + error );
        console.log( "Status: " + status );
        console.log( xhr );
}