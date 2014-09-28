#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: shawn@eryue.me
@date: Mon Aug 25 19:12:28 2014

Transfer the crawler data to online db

Lisense under GPLv3.
"""
# system
import time
import cPickle

# package
import requests
import torndb
from BeautifulSoup import BeautifulSoup

# project
from config import *

cdb = torndb.Connection(DB_HOST + ":" + str(DB_PORT),
                        DB_NAME,
                        DB_USER,
                        DB_PASSWORD)

pickh = cPickle.load(open('ignoreVideo.pickle', 'rb'))

def aggregate_video(vid):
    qs = "select * from Video where video_id=" + str(vid)
    data = cdb.get(qs)
    
    print data
    play_url = data['href']
    r = requests.get("http://flv.wandoujia.com/hack/flv?format=normal&url=" +
                     play_url)
    dom = BeautifulSoup(r.text)
    print dom
    if dom.duration and dom.v:
        us = "insert into OnlineVideo ("

        us += ",".join(data.keys())
        us += ") values ("
        us += ",".join(['%s' for d in data.values()])
        us += ")"
        print us

        cdb.insert(us, *data.values())
    else:
        pickh.add(vid)
        cPickle.dump(pickh, open('ignoreVideo.pickle', 'wb'))
        print "Video %s is not parsable " + str(vid)

if __name__ == "__main__":
    # aggregate videos
    qs = "select video_id from Video"
    data = cdb.query(qs)
    rest = 0
    for d in data:
        vid = d['video_id']
        
        # check whether is processed
        # TODO: this is a easy version, we should check whether
        #       online is still playable
        qs = "select video_id from OnlineVideo where video_id=" + str(vid)
        online_data = cdb.get(qs)
        if vid in pickh or online_data is not None:
            print "Video %s is already online" % (vid)
            continue

        b_time = time.time()
        aggregate_video(d['video_id'])
        e_time = time.time()
        interval = e_time - b_time
        if interval < 1000:
            print interval
            time.sleep(1)

        # sleep a little time to less the possible to be recognized
        rest += 1
        if rest >= 60:
            rest = 0
            time.sleep(10)
