#!/usr/bin/python
# -*- coding: utf-8 -*-

# Samu Peltonen 28.5.2018
# Flask CGI-sovelluksena
from wsgiref.handlers import CGIHandler
from tietokanta import app as application

if __name__ == '__main__':
   CGIHandler().run(application)