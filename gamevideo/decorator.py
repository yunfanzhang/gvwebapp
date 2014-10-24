#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: shawn@eryue.me
@date: Fri Oct 24 23:14:20 2014

Lisense under GPLv3.
"""

# system
import json

# package

# project


def authencicated(fn):
    def decorator(self, *args, **kwargs):
        if 'user' not in self.session:
            self.write(json.dumps({'status': False}))
            return
        fn(self, *args, **kwargs)
        
    return decorator
