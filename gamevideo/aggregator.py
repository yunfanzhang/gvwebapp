#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: shawn@eryue.me
@date: Mon Aug 25 19:12:28 2014

Transfer the crawler data to online db

Lisense under GPLv3.
"""
# system

# package
import torndb

# project

cdb = torndb.Connection("127.0.0.1:3306", "GameVideos", "root")
odb = torndb.Connection("127.0.0.1:3306", "gamevideo", "root")

def aggregate_video():
    pass

if __name__ == "__main__":
    aggregate_video()
