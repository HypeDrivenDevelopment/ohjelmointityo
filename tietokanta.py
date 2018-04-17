#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, url_for, escape, request, Response, render_template, make_response
import sqlite3
import logging
import os

logging.basicConfig(filename=os.path.abspath('../hidden/logi.log'),level=logging.DEBUG)
app = Flask(__name__) 
app.debug = True

@app.route('/hae_viestit', methods=['GET'])
def hae_viestit():

    con = sqlite3.connect( os.path.abspath('../hidden/viestinta'))
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    
    try:
        cur.execute('select Nimi AS Nimi, Viesti AS Viesti from Viestit')
    except:
        logging.debug( sys.exc_info()[0] )
    
    viestit = ""
    for o in cur:
        viestit = viestit + "<li>" + o["Nimi"] + " | " + o["Viesti"] + "</li>"
        
    viestit = '<ul id="taulu">' + viestit + '</ul>' 
    
    con.close()

    resp = make_response(viestit, 200)
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
    
    try:
        con.execute(
            "INSERT INTO Viestit VALUES (?, ?, ?)",
            (indeksi, nimi, viesti))
            
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