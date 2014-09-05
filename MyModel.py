# -*- coding: utf-8 -*-
'''
Created on 2014/06/29

@author: seigo
'''

from google.appengine.ext import db

class HistoricalTable(db.Model):
    '''
        年表
    '''
    date = db.DateProperty(required=True)
    title = db.StringProperty(required=True)
    url = db.LinkProperty(required=True)
    pixel = db.IntegerProperty()
    
class PollRating(db.Model):
    '''
        支持率
    '''
    date = db.DateProperty(required=True)
    approval_rate = db.FloatProperty(required=True)
    unknown_rate = db.FloatProperty(required=True)
    disapproval_rate = db.FloatProperty(required=True)

class graphsvg(db.Model):
    '''
    SVGのテキスト格納
    '''
    svg = db.TextProperty(required=True)
    name = db.StringProperty()
    
class Preference(db.Model):
    '''
        全体の設定値
    '''
    graphFirstDate = db.DateProperty()
    margin = db.ListProperty(item_type=int)
    
class Government(db.Model):
    '''
        政権情報
    '''
    name = db.StringProperty(required=True)
    begin = db.DateProperty(required=True)
    end = db.DateProperty()
    now_flg = db.StringProperty()
    pixel = db.ListProperty(item_type=int)
    
    
class PhotoAttr(db.Model):
    '''
　　   PC版の年表に挿入する写真
    '''
    title = db.StringProperty()
    date = db.DateProperty(required=True)
    img_url = db.LinkProperty(required=True)
    pixel = db.IntegerProperty()
    width = db.IntegerProperty()
    
    
    
    
    