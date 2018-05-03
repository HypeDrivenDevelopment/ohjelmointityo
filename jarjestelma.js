window.onload = function() {

	$("#kirjaudu").on("click", tarkasta_oikeudet);

}

/*
Funktio joka lähettää käyttäjän syöttämät nimen ja salasanan ajaxilla tarkistettavaksi.
*/
function tarkasta_oikeudet(e) {
e.preventDefault();
$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/oikeudet",
        type: "POST",
        dataType: "text",
		data: { "kayttaja":$("#kayttaja").val(),
		"salasana":$("#salasana").val(),
        },
        success: kirjautumisen_tarkistus,
        error: ajax_virhe
});	
}


/*
Funktio joka kirjautumisen onnistuessa lataa tietokannat, 
lisää painikkeisiin toiminnallisuuden, sekä piilottaa kirjautumisen ja näyttää sivun muun sisällön.
*/
function kirjautumisen_tarkistus (data, textStatus, request) {
	if (data == "true") {
	$("#laheta").on("click", lisaa_tietokantaan);
	
	$("#muuta").on("click", muuta_asetukset);
	
	$("#send").on("click", lisaa_chattietokantaan);
	
	$("#tyhjenna").on("click", tyhjenna_chat);
	
	$("#nayta").on("click", hae_kaikkiviestit);
	
	hae_viestit();
	
	hae_chat();
	
	$('#kirjautumiset').addClass('hidden');
	
	$('#sisalto').removeClass('hidden');
	}
	
	console.log( data );
	
	// if data == perus, asdf
	// if data == admin, asdf+
}
/*
Funktio joka lähettää ajaxilla kutsun chattietokannan tyhjentämisestä.
*/
function tyhjenna_chat(e) {
e.preventDefault();
$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/tyhjenna_chat",
        type: "GET",
        dataType: "text",
        success: tyhjennys_onnistui,
        error: ajax_virhe
});
}
/*
Funktio joka välittää käyttäjän syötteen ajaxilla chattietokantaan.
*/
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

/*
Funktio joka hakee ajaxilla chattietokannan sisällön.
*/
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
/*
Funktio joka hakee klikatun viestielementin ID:n ja välittää sen ajaxilla eteenpäin poistoa varten.
*/
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

/*
Funktio joka hakee ajaxilla halutun määrän viestitietokannan viestejä.
*/
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

/*
Funktio joka hakee ajaxilla kaikki viestitietokannan viestit.
*/
function hae_kaikkiviestit(e) {
e.preventDefault();
var kaikki = 999;
$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/hae_viestit",
        type: "POST",
        dataType: "text",
		data: { "maara":kaikki,
		},
        success: lisaa_viestit,
        error: ajax_virhe
});
}

/*
Funktio joka ottaa lomakkeelta käyttäjän nimen, viestin ja tiedon automaattisesta poistosta 
ja välittää ne ajaxilla viestitietokantaan lisättäväksi.
*/
function lisaa_tietokantaan(e) {
e.preventDefault();
var check = false
if ($('#poisto').is(":checked"))
{
  check = true
}
console.log( check );
$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/lisaa_tietokantaan",
        type: "POST",
        dataType: "text",
		
		data: { "nimi":$("#kayttaja").val(),
        "viesti":$("#viesti").val(),
		"poisto":check,
        },
        
        success: lisaaminen_onnistui,
        error: ajax_virhe
});	
}

function tyhjennys_onnistui(data, textStatus, request) {
	console.log( data );
	hae_chat();
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