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
    
    if encoded == "6416068d531d179b8de9bcab314dbb4788f4280d":
        Response = make_response("true")
        return Response
    
    Response = make_response("false")
    return Response

    
@app.route('/hae_viikko', methods=['GET','POST'])
def hae_viikko():

    luku = datetime.datetime.today().weekday() # palauttaa kokonaisluvun, maanantai = 0, mahd 1 datetime liikaa
    
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
        if o["Deadline"] > maanantai and o["Deadline"] < seuraavamaanantai:
            while i < 7:
                paivastr = o["Deadline"]

                paiva = datetime.datetime.strptime(paivastr, "%Y-%m-%d")

                vkopaiva = paiva.weekday()
                strvkopaiva = str(vkopaiva)
                
                if vkopaiva == i:
                    day = day + strvkopaiva + " || " + o["Viesti"] + " | " + o["Deadline"] + "\n"
                    break
                else:
                    dayb = "<td>" + day + "</td>"
                    viikko = viikko + dayb
                    i += 1
                    day = ""
    
    if day != "":
        dayb = "<td>" + day + "</td>"
        viikko = viikko + dayb    
    
    #if i < 7, for erotus do td /td
    
    viikko = "<tr>" + viikko + "</tr>"
    viikko = otsikot + viikko
    viikko = "<table>" + viikko + "</table>"
    
    con.close()

    resp = make_response(viikko, 200)
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp
    

# Viestitietokannasta viikon vanhat viestit poistava funktio, joka palauttaa tiedon onnistumisesta.
@app.route('/poista_vanhat', methods=['GET','POST'])
def poista_vanhat():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    today = date.today()
    week = today + timedelta(days=-7)

    try:
        con.execute('delete from Viestit WHERE Paiva<?', (week,))
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
            cur.execute('select Nimi AS Nimi, Viesti AS Viesti, ViestiID AS ViestiID, Paiva AS Paiva from Viestit order by ViestiID desc')
        except:
            logging.debug( sys.exc_info()[0] )
            
    else:
        try:
            cur.execute("select Nimi AS Nimi, Viesti AS Viesti, ViestiID AS ViestiID, Paiva AS Paiva from Viestit where Viesti like ? order by ViestiID desc", ('%'+hakusana+'%',))
        except:
            logging.debug( sys.exc_info()[0] )
    
    i = 1
    viestit = ""
    for o in cur:
        numero = o["ViestiID"]
        merkkijono = str (numero)
        viestit = viestit + "<li class='poista' id='" + merkkijono + "'>" + o["Nimi"] + " | " + o["Viesti"] + " | " + o["Paiva"] + "</li>"
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
        cur.execute('select Teksti AS Teksti, ChatID AS ChatID from Chat order by ChatID desc') 
    except:
        logging.debug( sys.exc_info()[0] )
        
    maara = 10
    i = 1
    viestit = ""
    for o in cur:
        viestit = viestit + "<td>" + o["Teksti"] + "</td>"
        if i == maara:
            break
        i += 1
        
    viestit = '<tr id="chatviestit">' + viestit + '</tr>' 
    
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

    indeksi = None
    
    today = date.today()
    
    
    try:
        con.execute(
            "INSERT INTO Viestit VALUES (?, ?, ?, ?, ?)",
            (indeksi, nimi, viesti, today, poisto))
            
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