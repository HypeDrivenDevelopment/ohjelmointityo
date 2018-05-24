window.onload = function() {

	$("#kirjaudu").on("click", tarkasta_oikeudet);

}

// Globaalit muuttujat viestien hakemisen intervallille.
var ajastus;
var chatajastus;

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
	if (data == "Admin") {
		$("#laheta").on("click", lisaa_tietokantaan);
	
		$("#muuta").on("click", hae_viestitevent);
	
		$("#vaihda").on("click", lisaa_motd);
	
		$("#send").on("click", lisaa_chattietokantaan);
	
		$("#tyhjenna").on("click", tyhjenna_chat);
	
		$("#nayta").on("click", hae_kaikkiviestit);
	
		$("#hae").on("click", hae_hakusanalla);
	
		$("#aseta").on("click", aseta_ajastukset);
	
		hae_viestit();
	
		hae_chat();
	
		hae_kalenteri();
	
		hae_motd();
	
		alusta_ajastukset();
	
		$('#kirjautumiset').addClass('hidden');
	
		$('#sisalto').removeClass('hidden');
	}
	
	if (data == "User") {
		$("#laheta").on("click", lisaa_tietokantaan);
	
		$("#muuta").on("click", hae_viestitevent);
	
		$("#vaihda").on("click", ei_oikeuksia);
	
		$("#send").on("click", lisaa_chattietokantaan);
	
		$("#tyhjenna").on("click", ei_oikeuksia);
	
		$("#nayta").on("click", hae_kaikkiviestit);
	
		$("#hae").on("click", hae_hakusanalla);
	
		$("#aseta").on("click", aseta_ajastukset);
	
		hae_viestit();
	
		hae_chat();
	
		hae_kalenteri();
	
		hae_motd();
	
		alusta_ajastukset();
	
		$('#kirjautumiset').addClass('hidden');
	
		$('#sisalto').removeClass('hidden');
	}
	
	console.log( data );
	
}

/*
Intervallien asettaminen viestien hakuun sivun latauksen yhteydessä.
*/
function alusta_ajastukset() {
	var intervalli = $("#intervalli").val();
	ajastus = setInterval(ajastin, intervalli);
	chatajastus = setInterval(chatajastin, 5000);
}

/*
Intervallien uudelleenasettaminen viestien hakuun käyttäjän toimesta.
*/
function aseta_ajastukset(e) {
	e.preventDefault();
	clearInterval(ajastus);
	clearInterval(chatajastus);
	var intervalli = $("#intervalli").val();
	ajastus = setInterval(ajastin, intervalli);
	chatajastus = setInterval(chatajastin, 5000);
}

/*
Viesteihin liittyvien ajastettujen funktioiden kutsuminen.
*/
function ajastin() {
	hae_viestit();
	
	hae_kalenteri();
}

/*
Chatin hakevan funktion ajastettu kutsuminen.
*/
function chatajastin() {
	hae_chat();
}

/*
Funktio joka ilmoittaa käyttäjälle ettei hänellä ole riittäviä oikeuksia toiminnon käyttämiseen.
*/
function ei_oikeuksia() {
	console.log("ei oikeuksia");
}

/*
Funktio joka hakee päivän viestin tietokannasta.
*/
function hae_motd() {
	$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/hae_motd",
        type: "GET",
        dataType: "text",
        success: paivita_motd,
        error: ajax_virhe
	});
}

/*
Funktio joka lähettää uuden päivän viestin tietokantaan.
*/
function lisaa_motd(e) {
	e.preventDefault();
	$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/lisaa_motd",
        type: "POST",
        dataType: "text",
		
		data: { "motd":$("#motd").val(),
        },
        
        success: motdlisaaminen_onnistui,
        error: ajax_virhe
	});	
}

/*
Funktio joka hakee kalenterinäkymän kuluvan viikon deadlineista.
*/
function hae_kalenteri() {
	$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/hae_viikko",
        type: "GET",
        dataType: "text",
        success: lisaa_kalenteri,
        error: ajax_virhe
	});
}

/*
Funktio joka hakee viestitietokannassa olevia viestejä syötetyllä hakusanalla.
*/
function hae_hakusanalla(e) {
	e.preventDefault();
	$.ajax({
        async: true,
        url: "/~samipelt/cgi-bin/ohjelmointityo/flask.cgi/hae_viestit",
        type: "POST",
        dataType: "text",
		
		data: { "maara":$("#maara").val(),
		"hakusana":$("#hakusana").val(),
        },
        
        success: lisaa_viestit,
        error: ajax_virhe
	});	
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
		"kayttaja":$("#kayttaja").val(),
		
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

function hae_viestitevent(e) {
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
	var check = false;
	if ($('#poisto').is(":checked"))
	{
	check = true;
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
		"deadline":$("#deadline").val(),
		"lisatiedot":$("#lisatiedot").val(),
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
	$("#viesti").val(null);
	$("#deadline").val(null);
	$("#lisatiedot").val(null);
	hae_viestit();
	hae_kalenteri();
}

function chatlisaaminen_onnistui(data, textStatus, request) {
	console.log( data );
	$("#message").val(null);
	hae_chat();
}

function motdlisaaminen_onnistui(data, textStatus, request) {
	console.log( data );
	hae_motd();
}

function poistaminen_onnistui(data, textStatus, request) {
	console.log( data );
	hae_viestit();
	hae_kalenteri();
}

function lisaa_viestit(data, textStatus, request) {
	$('#taulu').replaceWith( data );
	console.log( data );
	$(".poista").on("click", poista_tietokannasta);
}

function lisaa_chat(data, textStatus, request) {
	$('#chatviestit').replaceWith( data );
	console.log( data );
}

function paivita_motd(data, textStatus, request) {
	$('#motdteksti').replaceWith( data );
	console.log( data );
}

function lisaa_kalenteri(data, textStatus, request) {
	$('#kalenteri').replaceWith( data );
	console.log( data );
}

function ajax_virhe(xhr, status, error) {
    console.log( "Error: " + error );
    console.log( "Status: " + status );
    console.log( xhr );
}