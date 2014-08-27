#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: shawn@eryue.me
@date: Mon Aug 25 18:09:23 2014

Application Server to handle requests

Lisense under GPLv3.
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# system
import json

# package
import tornado
import tornado.web
import tornado.options

# project
from dao import VideoSummaryDao, VideoDao, GameSummaryDao, GameDao, VideoSearchDao


class Application(tornado.web.Application):
    """
    Init a startup application
    """
    
    def __init__(self, ):
        """
        """
        
        handlers = [
            # API
            (r"^/api/v1$", BaseHandler),
            
            # Object API
            (r"^/api/v1/videos$", VideoCollectionHandler),
            (r"^/api/v1/videos/(\d+)$", VideoHandler),
            (r"^/api/v1/videos/(\d+)/comments$", VideoCommentCollectionHandler),
            (r"^/api/v1/videos/(\d+)/apps$", VideoAppCollectionHandler),
            (r"^/api/v1/videos/(\d+)/apps/(\d+)$", VideoAppHandler),
            (r"^/api/v1/games$", GameCollectionHandler),
            (r"^/api/v1/games/(\d+)$", GameHandler),
            (r"^/api/v1/games/(\d+)/videos$", GameVideoCollectionHandler),

            # Search API
            (r"^/api/v1/q/videos$", VideoSearchHandler),
        ]
        
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "template"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            debug = True,
        )

        #super(Application, self).__init__(self, handlers, **settings)
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get():
        pass

    def post():
        pass


class VideoCollectionHandler(BaseHandler):
    vs_dao = VideoSummaryDao()

    def get(self):
        page = int(self.get_argument('page', '1'))
        max_results = int(self.get_argument('maxResults', '20'))
        sort_by = self.get_argument('sort', 'new')
        
        if sort_by == 'like':
            sort_by = 'good'
        elif sort_by == 'watch':
            sort_by = 'play'
        else:
            sort_by = 'published'

        start = max_results * (page -1)
        limit = max_results

        video_all_counts = self.vs_dao.get_all_count()
        video_summaries = self.vs_dao.get_all(start, limit, sort_by)
        
        result = {
            'totalCount': video_all_counts,
            'items': video_summaries,
        }

        self.write(json.dumps(result))
        return

class VideoHandler(BaseHandler):
    vdao = VideoDao()

    def get(self, video_id):
        video = self.vdao.get(video_id)
        
        # TODO: use flvproxy to update playPage to downloadURL
        
        self.write(json.dumps(video))
        return

    def post(self, video_id):
        # TODO: implement like function
        req_data = json.loads(self.request.body)
        
        self.write(json.dumps(req_data))
        return

class VideoCommentCollectionHandler(BaseHandler):
    def get(self, video_id):
        page = int(self.get_argument('page', '1'))
        max_results = int(self.get_argument('maxResults', '20'))

        start = max_results * (page -1)
        limit = max_results
        # TODO: implement comment collection GET
        
        all_comment_count = 100
        all_comments = [
            {
                "commentId": 1,
                "commentUserName": u"春天花会开",
                "message": u"小二郎",
            }
        ]
        result = {
            "totalCount": all_comment_count,
            "items": all_comments,
        }
        self.write(json.dumps(result))
        return

    def post(self, video_id):
        # TODO: implement comment function
        req_data = json.loads(self.request.body)
        
        self.write(json.dumps({"status": True}))
        return
        

class VideoAppCollectionHandler(BaseHandler):
    def get(self, video_id):
        # TODO: data fill into Database
        all_app_count = 2
        all_apps =  [
            {
                "app_id": 1920,
                "name": "腾讯QQ",
                "package": "com.tencent.qq",
                "icon": "http://img.wdjimg.com/mms/icon/v1/2/fd/453c5c37cc3d366d32ecee33e1247fd2_48_48.png",
                "downloadURL": "http://apps.wandoujia.com/apps/com.tencent.mobileqq/download",
            },
            {
                "app_id": 1080,
                "name": "捕鱼达人3",
                "package": "org.cocos2d.fishingjoy3.wdj",
                "icon": "http://img.wdjimg.com/mms/icon/v1/e/aa/2e7d42fb38ff611a842d1878fc698aae_48_48.png",
                "downloadURL": "http://apps.wandoujia.com/apps/org.cocos2d.fishingjoy3.wdj/download",
            },                
        ]
        
        result = {
            'totalCount': all_app_count,
            'items': all_apps
        }

        self.write(json.dumps(result))
        return

class VideoAppHandler(BaseHandler):
    def post(self, video_id, app_id):
        # TODO: implement comment function
        req_data = json.loads(self.request.body)
        
        self.write(json.dumps({"status": True}))
        return
        

class GameCollectionHandler(BaseHandler):
    gs_dao = GameSummaryDao()

    def get(self):
        page = int(self.get_argument('page', '1'))
        max_results = int(self.get_argument('maxResults', '20'))

        start = max_results * (page -1)
        limit = max_results

        game_all_counts = self.gs_dao.get_all_count()
        game_summaries = self.gs_dao.get_all(start, limit)
        
        result = {
            'totalCount': game_all_counts,
            'items': game_summaries,
        }

        self.write(json.dumps(result))
        return


class GameHandler(BaseHandler):
    gdao = GameDao()

    def get(self, game_id):
        game = self.gdao.get(game_id)
        
        # TODO: use flvproxy to update playPage to downloadURL
        
        self.write(json.dumps(game))
        return



class GameVideoCollectionHandler(BaseHandler):
    gdao = GameDao()

    def get(self, game_id):
        page = int(self.get_argument('page', '1'))
        max_results = int(self.get_argument('maxResults', '20'))

        start = max_results * (page -1)
        limit = max_results

        video_all_counts = self.gdao.get_video_count(game_id)
        video_summaries = self.gdao.get_videos(game_id, start, limit)
        
        result = {
            'totalCount': video_all_counts,
            'items': video_summaries,
        }

        self.write(json.dumps(result))
        return
        


class VideoSearchHandler(BaseHandler):
    vsearch_dao = VideoSearchDao()
 
    def get(self):
        page = int(self.get_argument('page', '1'))
        max_results = int(self.get_argument('maxResults', '20'))
        word = self.get_argument('word', '')

        start = max_results * (page -1)
        limit = max_results

        video_all_counts = self.vsearch_dao.get_video_count(word)
        video_summaries = self.vsearch_dao.get_videos(word, start, limit)
        
        result = {
            'totalCount': video_all_counts,
            'items': video_summaries,
        }

        self.write(json.dumps(result))
        return
        

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = Application()

    application.listen(8080)

    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()
