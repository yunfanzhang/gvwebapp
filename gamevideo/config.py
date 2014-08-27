#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: shawn@eryue.me
@date: Tue Aug 26 00:13:39 2014

Configurations

Lisense under GPLv3.
"""
# system

# package

# project

mode = 'PRODUCTION'


API_PORT = 8080
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'GameVideos'
DB_USER = 'root'
DB_PASSWORD = ''

if mode == 'debug':
    API_PORT = 8080
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_NAME = 'GameVideos'
    DB_USER = 'root'
    DB_PASSWORD = ''
    
