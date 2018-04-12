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

    resp = make_response("viesti")
    resp.charset = "UTF-8"
    resp.mimetype = "text/plain"
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)