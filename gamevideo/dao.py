#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: shawn@eryue.me
@date: Mon Aug 25 17:30:41 2014

Manuplate Database for data

Lisense under GPLv3.
"""
# system

# package
import torndb

# project
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from model import VideoSummary, Video, GameSummary, Game


def build_query(mapping_dict, exp=list()):
    qs = ""
    for k in mapping_dict.keys():
        if k in exp:
            continue
        qs += k + ','

    return qs[:-1]


class AbstractDao(object):
    _db = None
    _atable = 'Uploader'

    def __init__(self):
        if AbstractDao._db == None:
            self._db = torndb.Connection(
                DB_HOST + ":" + str(DB_PORT),
                DB_NAME,
                DB_USER,
                DB_PASSWORD
            )

    def get_name_from_uid(self, uid):
        qs = "select uploader_name "
        qs += " from " + self._atable
        qs += " where uploader_id='" + str(uid) + "'"
        
        print qs
        data2 = self._db.get(qs)
        return data2['uploader_name']


class VideoSummaryDao(AbstractDao):
    _table = 'Video'

    def __init__(self):
        super(VideoSummaryDao, self).__init__()

    def get_all_count(self):
        count = self._db.get("select count(*) from " +
                               self._table)
        
        return count['count(*)']

    def get_all(self, start=None, limit=None, sort_by=None):
        qs = "select " + build_query(VideoSummary)
        qs += " from " + self._table
        if sort_by != None:
            qs += " order by " + sort_by + " desc "
        if start != None and limit != None:
            qs += " limit " + str(start) + "," + str(limit)
        

        print qs
        data = self._db.query(qs)
        
        # reverse mapping database to json
        res = list()
        for d in data:
            item = dict()
            for k,v in d.items():
                item[VideoSummary[k]] = v
            res.append(item)
            # update uploader_id to uplaoder_name
            item[VideoSummary['uploader_id']] = self.get_name_from_uid(d['uploader_id'])
        
        return res


class VideoDao(AbstractDao):
    _vtable = 'Video'

    def __init__(self):
        super(VideoDao, self).__init__()

    def get(self, video_id):
        qs = "select " + build_query(Video)
        qs += " from " + self._vtable
        qs += "  where video_id='" + video_id + "'"
        
        print qs
        data = self._db.get(qs)
        
        res = dict()
        for k,v in data.items():
            res[Video[k]] = v

        # update uploader_id to uplaoder_name
        res[Video['uploader_id']] = self.get_name_from_uid(data['uploader_id'])

        return res
        

class GameSummaryDao(AbstractDao):
    _table = 'Game'
    _vtable = 'Video'

    def __init__(self):
        super(GameSummaryDao, self).__init__()

    def get_all_count(self):
        count = self._db.get("select count(*) from " +
                               self._table)
        
        return count['count(*)']

    def get_all(self, start=None, limit=None, sort_by=None):
        qs = "select " + build_query(GameSummary, ['video_count'])
        qs += " from " + self._table
        if sort_by != None:
            qs += " order by " + sort_by + " desc "
        if start != None and limit != None:
            qs += " limit " + str(start) + "," + str(limit)
        

        print qs
        data = self._db.query(qs)
        
        # reverse mapping database to json
        res = list()
        for d in data:
            item = dict()
            for k,v in d.items():
                item[GameSummary[k]] = v
            
            # Get video count, this implementation is bad
            qs = "select count(*)"
            qs += " from " + self._vtable
            qs += " where game_id=" + str(d['game_id'])
            print qs
            data = self._db.get(qs)
            item[GameSummary['video_count']] = data['count(*)']

            res.append(item)
        
        return res


class GameDao(AbstractDao):
    _gtable = 'Game'
    _vtable = 'Video'

    def __init__(self):
        super(GameDao, self).__init__()

    def get(self, game_id):
        qs = "select " + build_query(Game, ['video_count'])
        qs += " from " + self._gtable
        qs += "  where game_id=" + game_id
        
        print qs
        data = self._db.get(qs)
        
        res = dict()
        for k,v in data.items():
            res[Game[k]] = v

        # Get video count, this implementation is bad
        qs = "select count(*)"
        qs += " from " + self._vtable
        qs += " where game_id=" + str(game_id)
        print qs
        data = self._db.get(qs)
        res[Game['video_count']] = data['count(*)']

        return res

    def get_video_count(self, game_id):
        # Get video count, this implementation is bad
        qs = "select count(*)"
        qs += " from " + self._vtable
        qs += " where game_id=" + str(game_id)
        print qs
        data = self._db.get(qs)

        return data['count(*)']

    def get_videos(self, game_id, start=None, limit=None, sort_by=None):
        qs = "select " + build_query(VideoSummary)
        qs += " from " + self._vtable
        qs += " where game_id=" + str(game_id) 
        if sort_by != None:
            qs += " order by " + sort_by + " desc "
        if start != None and limit != None:
            qs += " limit " + str(start) + "," + str(limit)
        

        print qs
        data = self._db.query(qs)
        
        # reverse mapping database to json
        res = list()
        for d in data:
            item = dict()
            for k,v in d.items():
                item[VideoSummary[k]] = v
            res.append(item)
            # update uploader_id to uplaoder_name
            item[VideoSummary['uploader_id']] = self.get_name_from_uid(d['uploader_id'])
        
        return res


class VideoSearchDao(AbstractDao):
    _vtable = 'Video'

    def __init__(self):
        super(VideoSearchDao, self).__init__()

    def get_video_count(self, word):
        # Get video count, this implementation is bad
        qs = "select count(*)"
        qs += " from " + self._vtable
        qs += " where title like %s"
        print qs
        data = self._db.get(qs,  ("%" + word + "%",))

        return data['count(*)']

    def get_videos(self, word, start=None, limit=None, sort_by=None):
        qs = "select " + build_query(VideoSummary)
        qs += " from " + self._vtable
        qs += " where title like %s"
        if sort_by != None:
            qs += " order by " + sort_by + " desc "
        if start != None and limit != None:
            qs += " limit " + str(start) + "," + str(limit)
        

        print qs
        data = self._db.query(qs, ("%" + word + "%",))
        
        # reverse mapping database to json
        res = list()
        for d in data:
            item = dict()
            for k,v in d.items():
                item[VideoSummary[k]] = v
            res.append(item)
            # update uploader_id to uplaoder_name
            item[VideoSummary['uploader_id']] = self.get_name_from_uid(d['uploader_id'])
        
        return res
