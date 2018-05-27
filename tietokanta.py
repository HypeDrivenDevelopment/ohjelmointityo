#!/usr/bin/python
# -*- coding: utf-8 -*-

# Samu Peltonen 28.5.2018
# Tietokantakyselyitä ja muokkauksia suorittava ohjelma.

from flask import Flask, session, redirect, url_for, escape, request, Response, render_template, make_response
from datetime import date
from datetime import timedelta
from datetime import datetime
import datetime
import time
import hashlib
import sqlite3
import logging
import os

logging.basicConfig(filename=os.path.abspath('../hidden/logi.log'),level=logging.DEBUG)
app = Flask(__name__) 
app.debug = True

# Salasanan ja käyttäjätunnuksen tarkastava funktio, joka palauttaa tiedon tarkastuksen onnistumisesta. Salauksessa käytetään SHA-1:tä.
@app.route('/oikeudet', methods=['GET','POST'])
def oikeudet():

    kayttaja = request.form.get('kayttaja', "")
    salasana = request.form.get('salasana', "")
    
    merkkijono = kayttaja + salasana
    
    encoded = hashlib.sha1(merkkijono.encode('utf-8')).hexdigest()
    
    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    
    try:
        cur.execute('select Oikeus AS Oikeus from Oikeudet where Merkkijono=?', (encoded,))
    except:
        Response = make_response("oikeudet ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
    
    oikeus = ""
    
    for o in cur:
        oikeus = o["Oikeus"]
    
    con.close()
        
    if oikeus == "":
        Response = make_response("false")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
        
    Response = make_response(oikeus)
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response
    
    
# Päivän viestin tietokannasta hakeva funktio, joka palauttaa viestin merkkijonona otsikkotageilla.    
@app.route('/hae_motd', methods=['GET','POST'])
def hae_motd():
    
    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    
    try:
        cur.execute('select Viesti AS Viesti from motd')
    except:
        Response = make_response("hae_motd ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
    
    viesti = ""
    
    for o in cur:
        viesti = o["Viesti"]
    
    viesti = '<h2 id="motdteksti">' + viesti + '</h2>'
    
    con.close()
        
    Response = make_response(viesti)
    return Response
    

# Päivän viestin tietokantaan muuttava funktio.    
@app.route('/lisaa_motd', methods=['GET','POST'])
def lisaa_motd():
    
    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    motd = request.form.get('motd', "")

    try:
        con.execute(
            "update Motd set Viesti=?", (motd,))
            
    except:
        con.rollback()
        Response = make_response("lisaa_motd ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
            
    con.commit()
    con.close()

    Response = make_response("toimii")
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response  

 
# Merkkijonon taulukkotageilla kuluvan viikon deadlineista hakeva funktio. 
@app.route('/hae_viikko', methods=['GET','POST'])
def hae_viikko():

    luku = datetime.datetime.today().weekday() # palauttaa kokonaisluvun, maanantai = 0
    
    today = date.today()

    maanantai = today + timedelta(days=-(luku)) # saadaan kuluvan viikon maanantai
    
    seuraavamaanantai = maanantai + timedelta(days=7)
    
    maanantai = str(maanantai)
    seuraavamaanantai = str(seuraavamaanantai)


    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
        
    cur = con.cursor()
    
    try:
        cur.execute('select Viesti AS Viesti, Deadline AS Deadline from Viestit where Deadline is not null order by Deadline')
    except:
        Response = make_response("hae_viikko ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
         
    viikko = ""
    day = ""
    dayb = ""
    
    # Taulukon luominen: Ensin luodaan otsikkosolut viikonpäiville.
    otsikot = "<tr><th>Maanantai</th><th>Tiistai</th><th>Keskiviikko</th><th>Torstai</th><th>Perjantai</th><th>Lauantai</th><th>Sunnuntai</th></tr>"
    
    i = 0
    
    # Sitten testataan järjestyksessä olevia deadlineja, osuvatko ne kuluvalle viikolle.
    for o in cur:
        if o["Deadline"] >= maanantai and o["Deadline"] < seuraavamaanantai:
        
            # Jos osuu, niin testataan osuuko päivä indeksin osoittamalle viikonpäivälle ja mahdollisesti lisätään se merkkijonoon
            while i < 7:
                paivastr = o["Deadline"]

                paiva = datetime.datetime.strptime(paivastr, "%Y-%m-%d")

                vkopaiva = paiva.weekday()
                
                if vkopaiva == i:
                    day = day + o["Viesti"] + " | " + o["Deadline"] + "<br>"
                    break
                
                # Jollei osunut niin päätetään käsiteltävä päivä lisäämällä solutagit saatujen deadlinejen ympärille ja siirrytään seuraavaan päivään.
                else:
                    dayb = "<td>" + day + "</td>"
                    viikko = viikko + dayb
                    i += 1
                    day = ""
    
    # Lisätään vielä mahdollisesti äsken day muuttujaan jäänyt deadline taulukkoon.
    if day != "":
        dayb = "<td>" + day + "</td>"
        viikko = viikko + dayb
        i += 1
    
    # Jos viikossa ei ollut deadlineja loppuviikosta tai koko viikkona niin täydennetään sinne kuitenkin tyhjiä soluja.
    if i < 6:
        erotus = 7 - i
        while erotus > 0:
            viikko = viikko + "<td>""</td>"
            erotus -= 1
    
    viikko = "<tr>" + viikko + "</tr>"
    viikko = otsikot + viikko
    viikko = "<table id='kalenteri' name='kalenteri'>" + viikko + "</table>"
    
    con.close()

    Response = make_response(viikko, 200)
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response
    

# Viestitietokannasta viikon deadlinesta vanhentuneet viestit poistava funktio, joka palauttaa tiedon onnistumisesta.
@app.route('/poista_vanhat', methods=['GET','POST'])
def poista_vanhat():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    today = date.today()
    week = today + timedelta(days=-7)

    try:
        con.execute('delete from Viestit WHERE Deadline<? and Poisto="True" and not Deadline=""', (week,)) 
    except:
        con.rollback()
        Response = make_response("poista_vanhat ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
        
    con.commit()
    con.close()

    Response = make_response("toimii")
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response


# Viestitietokannasta kaikki viestit hakeva funktio, joka syötteen perusteella palauttaa n-kappaletta uusinta viestiä merkkijonona listatageilla.
@app.route('/hae_viestit', methods=['GET','POST'])
def hae_viestit():

    poistot = poista_vanhat()

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    maara = request.form.get('maara', "")
    
    try:
        maara = int (maara)
        
    except:
        maara = 10
    
    hakusana = request.form.get('hakusana', "")
    
    haku = True
    
    if hakusana == "":
        haku = False
        
    cur = con.cursor()
    
    if haku == False:
        try:
            cur.execute('select Nimi AS Nimi, Viesti AS Viesti, ViestiID AS ViestiID, Paiva AS Paiva, Deadline AS Deadline, Lisatiedot AS Lisatiedot from Viestit order by ViestiID desc')
        except:
            Response = make_response("hae_viestit ei toimi")
            Response.charset = "UTF-8"
            Response.mimetype = "text/plain"
            return Response
            
    else:
        try:
            cur.execute("select Nimi AS Nimi, Viesti AS Viesti, ViestiID AS ViestiID, Paiva AS Paiva, Deadline AS Deadline, Lisatiedot AS Lisatiedot from Viestit where Viesti like ? order by ViestiID desc", ('%'+hakusana+'%',))
        except:
            Response = make_response("hae_viestit ei toimi")
            Response.charset = "UTF-8"
            Response.mimetype = "text/plain"
            return Response
    
    i = 1
    viestit = ""
    for o in cur:
        numero = o["ViestiID"]
        merkkijono = str (numero)
        viestit = viestit + "<li class='poista' id='" + merkkijono + "'>" + "L&auml;hett&auml;j&auml;: " + o["Nimi"] + " &emsp; " + "Viesti: " + o["Viesti"] + " &emsp; " + "Lis&auml;&auml;misp&auml;iv&auml;: " + o["Paiva"] + " &emsp; " + "Deadline: " + o["Deadline"] + " &emsp; " + "Lis&auml;tiedot: " + o["Lisatiedot"] + "</li>"
        if i == maara:
            break
        i += 1
        
    viestit = '<ul id="taulu">' + viestit + '</ul>' 
    
    con.close()

    Response = make_response(viestit, 200)
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response

# Chattietokannasta viestit hakeva funktio, joka palauttaa kaikki viestit merkkijonona taulukkotageilla.    
@app.route('/hae_chat', methods=['GET','POST'])
def hae_chat():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
        
    cur = con.cursor()
    
    try:
        cur.execute('select Teksti AS Teksti, ChatID AS ChatID, Kayttaja AS Kayttaja from Chat order by ChatID') 
    except:
        Response = make_response("hae_chat ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
        
    viestit = ""
    for o in cur:
        viestit = viestit + "<td>" + o["Kayttaja"] + " : " + o["Teksti"] + "</td>"
        
    viestit = '<tr>' + viestit + '</tr>'

    viestit = '<table id="chatviestit">' + viestit + '</table>' 
    
    con.close()

    Response = make_response(viestit, 200)
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response

    
# Chattietokantaan viestin lisäävä funktio, joka palauttaa tiedon onnistumisesta.
@app.route('/lisaa_chattietokantaan', methods=['GET','POST'])
def lisaa_chattietokantaan():
    
    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    teksti = request.form.get('message', "")
    kayttaja = request.form.get('kayttaja', "")

    indeksi = None
    
    try:
        con.execute(
            "INSERT INTO Chat VALUES (?, ?, ?)",
            (indeksi, teksti, kayttaja))
            
    except:
        con.rollback()
        Response = make_response("lisaa_chattietokantaan ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
            
    con.commit()
    con.close()

    Response = make_response("toimii")
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response    


# Viestitietokantaan lisäävä funtio, käyttää saatua nimeä, viestiä, tietoa viestin poistosta, deadlinea ja lisätietoja, sekä hakee päivämäärän. Palauttaa tiedon onnistumisesta.
@app.route('/lisaa_tietokantaan', methods=['GET','POST'])
def lisaa_tietokantaan():
    
    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    nimi = request.form.get('nimi', "")
    viesti = request.form.get('viesti', "")
    poisto = request.form.get('poisto', "False")
    deadline = request.form.get('deadline', "")
    lisatiedot = request.form.get('lisatiedot', "")

    indeksi = None
    
    today = date.today()
    
    
    try:
        con.execute(
            "INSERT INTO Viestit VALUES (?, ?, ?, ?, ?, ?, ?)",
            (indeksi, nimi, viesti, today, poisto, deadline, lisatiedot))
            
    except:
        con.rollback()
        Response = make_response("lisaa_tietokantaan ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
            
    con.commit()
    con.close()

    Response = make_response("toimii")
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response


# Funktio joka saa poistaa saatua id:tä vastaavan viestin viestitietokannasta. Palauttaa tiedon onnistumisesta.    
@app.route('/poista_tietokannasta', methods=['GET','POST'])
def poista_tietokannasta():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    id = request.form.get('id', "")
    
    try:
        con.execute('DELETE FROM Viestit WHERE ViestiID=?', (id,))
    except:
        con.rollback()
        Response = make_response("poista_tietokannasta ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
        
    con.commit()
    con.close()

    Response = make_response("toimii")
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response
    

# Funktio joka tyhjentää chattietokannan kokonaan ja palauttaa tiedon onnistumisesta.    
@app.route('/tyhjenna_chat', methods=['GET','POST'])
def tyhjenna_chat():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    try:
        con.execute('DELETE FROM Chat')
    except:
        con.rollback()
        Response = make_response("tyhjenna_chat ei toimi")
        Response.charset = "UTF-8"
        Response.mimetype = "text/plain"
        return Response
        
    con.commit()
    con.close()

    Response = make_response("toimii")
    Response.charset = "UTF-8"
    Response.mimetype = "text/plain"
    return Response

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)