#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, url_for, escape, request, Response, render_template, make_response
from datetime import date
from datetime import timedelta
import sqlite3
import logging
import os

logging.basicConfig(filename=os.path.abspath('../hidden/logi.log'),level=logging.DEBUG)
app = Flask(__name__) 
app.debug = True

@app.route('/oikeudet', methods=['GET','POST'])
def oikeudet():

    kayttaja = request.form.get('kayttaja', "")
    salasana = request.form.get('salasana', "")
    
    if kayttaja == "Admin" and salasana == "salasana":
        Response = make_response("true")
        return Response
        
    Response = make_response("false")
    return Response

    
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


@app.route('/hae_viestit', methods=['GET','POST'])
def hae_viestit():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    maara = request.form.get('maara', "")
    try:
        maara = int (maara)
        
    except:
        maara = 10
        
    cur = con.cursor()
    
    try:
        cur.execute('select Nimi AS Nimi, Viesti AS Viesti, ViestiID AS ViestiID, Paiva AS Paiva from Viestit order by ViestiID desc')
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

    
@app.route('/hae_chat', methods=['GET','POST'])
def hae_chat():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
        
    cur = con.cursor()
    
    try:
        cur.execute('select Teksti AS Teksti, ChatID AS ChatID from Chat order by ChatID desc') #mieti miten saa käännettyä vielä toisen kerran
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

    
@app.route('/lisaa_tietokantaan', methods=['GET','POST'])
def lisaa_tietokantaan():
    
    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    nimi = request.form.get('nimi', "")
    viesti = request.form.get('viesti', "")

    indeksi = None
    
    today = date.today() #str
    
    poisto = True
    
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