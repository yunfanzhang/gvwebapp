#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: shawn@eryue.me
@date: Mon Aug 25 17:31:26 2014

Data model for api controller, a transfer layer from dao to controller

Lisense under GPLv3.
"""
# system

# package

# project

VideoSummary = {'video_id' : 'videoId',
                'title' : 'name',
                'imgSrc' : 'cover',
                'good' : 'likeCount',
                'duration' : 'duration',
                'play' : 'playedCount',
}


Video = {'video_id' : 'videoId',
         'title' : 'name',
         'imgSrc' : 'cover',
         'good' : 'likeCount',
         'duration' : 'duration',
         'play' : 'playedCount',
         'uploader_id': 'authorName',
         'href': 'playInfo',
}


GameSummary = {'game_id' : 'gameId',
               'game_name' : 'name',
               'description' : 'description',
               'cover' : 'cover',
               'video_count': 'videoCount',
}


Game = {'game_id' : 'gameId',
        'game_name' : 'name',
        'description' : 'description',
        'cover' : 'cover',
        'banner' : 'banner',
        'banner_enabled' : 'bannerEnabled',
        'video_count': 'videoCount',
}


class Comment(object):
    def __init__(self):
        self.comment_id = None
        self.video_id = None
        self.comment_user_name = None
        self.message = None


class App(object):
    def __init__(self):
        self.app_id = None
        self.name = None
        self.package = None
        self.icon = None
        self.downloadURL = None
