#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, url_for, escape, request, Response, render_template, make_response
from datetime import date
from datetime import timedelta
from datetime import datetime
import time
import datetime
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
        logging.debug( sys.exc_info()[0] )
    
    oikeus = ""
    
    for o in cur:
        oikeus = o["Oikeus"]
    
    con.close()
        
    if oikeus == "":
        Response = make_response("false")
        return Response
        
    Response = make_response(oikeus)
    return Response
    
    
@app.route('/hae_motd', methods=['GET','POST'])
def hae_motd():
    
    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    
    try:
        cur.execute('select Viesti AS Viesti from motd')
    except:
        logging.debug( sys.exc_info()[0] )
    
    viesti = ""
    
    for o in cur:
        viesti = o["Viesti"]
    
    viesti = '<h2 id="motdteksti">' + viesti + '</h2>'
    
    con.close()
        
    Response = make_response(viesti)
    return Response
    
    
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
        Response = make_response("ei toimi")
        return Response
            
    con.commit()
    con.close()

    resp = make_response("toimii")
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp  

    
@app.route('/hae_viikko', methods=['GET','POST'])
def hae_viikko():

    luku = datetime.datetime.today().weekday() # palauttaa kokonaisluvun, maanantai = 0
    
    today = date.today()

    maanantai = today + timedelta(days=-(luku)) # saadaan maanantai
    
    seuraavamaanantai = maanantai + timedelta(days=7)
    
    maanantai = str(maanantai)
    seuraavamaanantai = str(seuraavamaanantai)


    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
        
    cur = con.cursor()
    
    try:
        cur.execute('select Viesti AS Viesti, Deadline AS Deadline from Viestit where Deadline is not null order by Deadline')
    except:
        logging.debug( sys.exc_info()[0] )
         
    viikko = ""
    day = ""
    dayb = ""
    
    otsikot = "<tr><th>Maanantai</th><th>Tiistai</th><th>Keskiviikko</th><th>Torstai</th><th>Perjantai</th><th>Lauantai</th><th>Sunnuntai</th></tr>"
    
    i = 0
    
    for o in cur:
        if o["Deadline"] >= maanantai and o["Deadline"] < seuraavamaanantai:
            while i < 7:
                paivastr = o["Deadline"]

                paiva = datetime.datetime.strptime(paivastr, "%Y-%m-%d")

                vkopaiva = paiva.weekday()
                
                if vkopaiva == i:
                    day = day + o["Viesti"] + " | " + o["Deadline"] + "<br>"
                    break
                else:
                    dayb = "<td>" + day + "</td>"
                    viikko = viikko + dayb
                    i += 1
                    day = ""
    
    if day != "":
        dayb = "<td>" + day + "</td>"
        viikko = viikko + dayb
        i += 1
    
    if i < 6:
        erotus = 7 - i
        while erotus > 0:
            viikko = viikko + "<td>""</td>"
            erotus -= 1
    
    viikko = "<tr>" + viikko + "</tr>"
    viikko = otsikot + viikko
    viikko = "<table id='kalenteri' name='kalenteri'>" + viikko + "</table>"
    
    con.close()

    resp = make_response(viikko, 200)
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp
    

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
        Response = make_response("ei toimi")
        return Response
        
    con.commit()
    con.close()

    resp = make_response("toimii")
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp


# Viestitietokannasta kaikki viestit hakeva funktio, joka syötteen perusteella palauttaa n-kappaletta uusinta viestiä listamuodossa.
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
            logging.debug( sys.exc_info()[0] )
            
    else:
        try:
            cur.execute("select Nimi AS Nimi, Viesti AS Viesti, ViestiID AS ViestiID, Paiva AS Paiva, Deadline AS Deadline, Lisatiedot AS Lisatiedot from Viestit where Viesti like ? order by ViestiID desc", ('%'+hakusana+'%',))
        except:
            logging.debug( sys.exc_info()[0] )
    
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

    resp = make_response(viestit, 200)
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp

# Chattietokannasta viestit hakeva funktio, joka palauttaa maksimissaan 10 uusinta viestiä taulukkomuodossa.    
@app.route('/hae_chat', methods=['GET','POST'])
def hae_chat():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
        
    cur = con.cursor()
    
    try:
        cur.execute('select Teksti AS Teksti, ChatID AS ChatID from Chat order by ChatID') 
    except:
        logging.debug( sys.exc_info()[0] )
        
    #maara = 10
    #i = 1
    viestit = ""
    for o in cur:
        viestit = viestit + "<td>" + o["Teksti"] + "</td>"
        #if i == maara:
        #    break
        #i += 1
        
    viestit = '<tr>' + viestit + '</tr>'

    viestit = '<table id="chatviestit">' + viestit + '</table>' 
    
    con.close()

    resp = make_response(viestit, 200)
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp

    
# Chattietokantaan viestin lisäävä funktio, joka palauttaa tiedon onnistumisesta.
@app.route('/lisaa_chattietokantaan', methods=['GET','POST'])
def lisaa_chattietokantaan():
    
    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    teksti = request.form.get('message', "")

    indeksi = None
    
    try:
        con.execute(
            "INSERT INTO Chat VALUES (?, ?)",
            (indeksi, teksti))
            
    except:
        con.rollback()
        Response = make_response("ei toimi")
        return Response
            
    con.commit()
    con.close()

    resp = make_response("toimii")
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp    


# Viestitietokantaan lisäävä funtio, käyttää saatua nimeä, viestiä ja tietoa viestin poistosta, sekä hakee päivämäärän. Palauttaa tiedon onnistumisesta.
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
        Response = make_response("ei toimi")
        return Response
            
    con.commit()
    con.close()

    resp = make_response("toimii")
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp


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
        Response = make_response("ei toimi")
        return Response
        
    con.commit()
    con.close()

    resp = make_response("toimii")
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp
    

# Funktio joka tyhjentää chattietokannan kokonaan ja palauttaa tiedon onnistumisesta.    
@app.route('/tyhjenna_chat', methods=['GET','POST'])
def tyhjenna_chat():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    try:
        con.execute('DELETE FROM Chat')
    except:
        con.rollback()
        Response = make_response("ei toimi")
        return Response
        
    con.commit()
    con.close()

    resp = make_response("toimii")
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)