# -*- coding: utf-8 -*-
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from MyModel import HistoricalTable, PollRating, Government, PhotoAttr
from datetime import datetime

#from initData import initDATA, clearDATA

oneDayPx = 1.5      #グラフの縦方向の間隔を決める値　1日あたりのピクセル数

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            params = {'nickname':user.nickname(), 'logout_url':users.create_logout_url("/")}
            fpath = os.path.join(os.path.dirname(__file__), 'views', 'base.html')
            html = template.render(fpath, params)
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(html)
        else:
            self.redirect(users.create_login_url(self.request.uri))

class HistoricalTablePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            self.redirect(users.create_login_url(self.request.uri))
            return
        datas = HistoricalTable.all().order('-date')
        
        params = {'datas':datas,'nickname':user.nickname()}
        fpath = os.path.join(os.path.dirname(__file__), 'views', 'historicaltable.html')
        html = template.render(fpath, params)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(html)
        
    def post(self):
        mid = self.request.get('mid')
        data = HistoricalTable.get_by_id(long(mid))
        data.delete()
        self.redirect('/redirect?url=/HistoricalTable')

class HTPost(webapp.RequestHandler):
    def post(self):
        try:
            ndatetime = datetime.strptime(self.request.get('date').encode('utf-8'), '%Y-%m-%d')
            ndate = datetime.date(ndatetime)
            ntitle = self.request.get('title')
            nurl = self.request.get('url')
            obj = HistoricalTable(date=ndate,title=ntitle,url=nurl)
            obj.save()
            self.redirect('/redirect?url=/HistoricalTable')
        except:
            datas = HistoricalTable.all().order('-date')
            msg = "エラー　入力項目を確認してください"
            params = {'datas':datas,'message':msg}
            fpath = os.path.join(os.path.dirname(__file__), 'views', 'historicaltable.html')
            html = template.render(fpath, params)
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(html)
            

class GraphPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            self.redirect(users.create_login_url(self.request.uri))
            return
        datas = PollRating.all().order('-date')
        errorflg = self.request.get('posterror')
        if errorflg:
            params = {'datas':datas, 'message':'エラー　入力項目を確認してください','nickname':user.nickname()}
        else:
            params = {'datas':datas,'nickname':user.nickname()}
        fpath = os.path.join(os.path.dirname(__file__), 'views', 'pollrating.html')
        html = template.render(fpath, params)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(html)
        
    def post(self):
        mid = self.request.get('mid')
        data = PollRating.get_by_id(long(mid))
        data.delete()
        self.redirect('/redirect?url=/graph')


class graphPost(webapp.RequestHandler):
    def post(self):
        try:
            ndatetime = datetime.strptime(self.request.get('date').encode('utf-8'), '%Y-%m-%d')
            ndate = datetime.date(ndatetime)
            napproval_rate = float(self.request.get('approval_rate'))
            nunknown_rate = float(self.request.get('unknown_rate'))
            ndisapproval_rate = float(self.request.get('disapproval_rate'))
            obj = PollRating(date=ndate,approval_rate=napproval_rate,unknown_rate=nunknown_rate,disapproval_rate=ndisapproval_rate)
            obj.save()
            self.redirect('/redirect?url=/graph')
        except:
            self.redirect('/redirect?url=/graph&posterror=True')

class myRedirect(webapp.RequestHandler):
    def get(self):
        try:
            url = self.request.get('url')
            self.redirect(url)
        except:
            self.redirect('/')
            
class htmlGenerate(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            self.redirect(users.create_login_url(self.request.uri))
            return
        
        gettemplate = self.request.get('template')
        if gettemplate:
            mytemplate = gettemplate
        else:
            mytemplate = 'result.html'
        
        '''
        Graph Parameter set
        '''
        
        if mytemplate.rfind('sp')==-1 and mytemplate.rfind('SP')==-1:
            '''テンプレートにSPまたはｓｐと入っていなかったらPC版の幅とマージンにセット'''
            width = 220             #グラフエリア（SVG）の幅
            legend_h = 90           #グラフの凡例の高さ
            margin=  [45,60,10,10]  #グラフエリアのマージン（SVGベース）
        else:
            '''テンプレートにSPまたはｓｐと入っていたらスマホ版のマージンに'''
            width =220
            legend_h =60
            margin = [20,15,15,10]
        
        svga, svgd, height = self.svgGenerate(width, margin,legend_h)
        svga_reverse = reversed(svga)
        svgd_reverse = reversed(svgd)
        scale = {}
        scale['width']= width
        scale['height']= int(height+margin[0] + margin[2]+legend_h)
        
        scale['startline']= margin[3]
        scale['startline_h'] = margin[0]+ legend_h
        scale['endline_h'] = height+margin[0]+legend_h
        scale['endline_w'] = width -margin[1]
        graph_w = width - margin[1] - margin[3]
        scale['20'] = graph_w*0.2 +margin[3]
        scale['40'] = graph_w*0.4 +margin[3]
        scale['60'] = graph_w*0.6 +margin[3]
        scale['80'] = graph_w*0.8 +margin[3]
        scale['startline_ht'] = width-margin[1]+10
        scale['startline_hex']= scale['startline_h'] -30
        scale['endline_hex'] = scale['endline_h'] +30
        
        
        '''
        Photo Parameter set
        '''
        self.reBuildPhoto(legend_h+margin[0])
        photos = PhotoAttr.all().order('-date')
        
        '''
        Other Parameter
        '''
        latest_obj = PollRating.all().order('-date').fetch(limit=1, offset=0)[0]
        latest_date = datetime(latest_obj.date.year, latest_obj.date.month, latest_obj.date.day)
        first_date = datetime(2007,4,1)
        month_pos = self.htMeasure(first_date, latest_date,margin[0]+legend_h)
        self.reBuildGov(legend_h+margin[0])
        go_list = Government.all().order('-begin')
        
        '''
        rendering
        '''
        self.htPosition(latest_date,margin[0]+legend_h)
        ht = HistoricalTable.all().order('-date')
        
        params = {'ht':ht,'svga':svga,'svgd':svgd,'svga_reverse':svga_reverse,'svgd_reverse':svgd_reverse,
                  'scale':scale,'month_pos':month_pos, 'go_list':go_list,'photos':photos, 'nickname':user.nickname()}
        fpath = os.path.join(os.path.dirname(__file__), 'views', mytemplate)
        html = template.render(fpath, params)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(html)
        
    
    def svgGenerate(self, WIDTH, MARGIN, PRE_H):
        width = WIDTH-(MARGIN[1]+MARGIN[3])
        margin_w = MARGIN[3]
        margin_h = MARGIN[0]+PRE_H
        datas = PollRating.all().order('-date')
        newest= datas[0].date.toordinal()
        l = datas.count()
        oldest= datas[l-1].date.toordinal()
        terms = newest-oldest
        height = terms*oneDayPx
        svga = []
        svgd = []
        for data in datas:
            y = (newest - data.date.toordinal())*oneDayPx +margin_h
            xa = data.approval_rate/100*width +margin_w
            xun = xa + data.unknown_rate/100*width
            svga.append([int(xa),int(y)])
            svgd.append([int(xun),int(y)])
        return svga, svgd, height
    
    def htMeasure(self, FIRST_DATE, LAST_DATE, MARGIN):
        first_date = FIRST_DATE
        last_date = LAST_DATE
        margin = MARGIN
        date = first_date
        months_pos = []
        timedelta = datetime(2012,2,1) - datetime(2012,1,1)
        while date < LAST_DATE + timedelta:
            strMonth_Day = date.strftime(' %Y-%m')
            terms = datetime.date(last_date).toordinal()- datetime.date(date).toordinal()
            position = terms *oneDayPx +margin
            months_pos.append([strMonth_Day,position])
            date = date + timedelta
            date = datetime(date.year, date.month, 1)
            
        return months_pos
    
    def htPosition(self, LAST_DATE, MARGIN):
        last_date = datetime.date(LAST_DATE)
        hts = HistoricalTable.all().order('-date')
        margin = MARGIN
        for ht in hts:
            pos = (last_date.toordinal() - ht.date.toordinal())*oneDayPx + margin-13
            ht.pixel = int(pos)
            ht.save()
        return
    
    def reBuildGov(self, MARGIN):
        govs = Government.all()
        latest_obj = PollRating.all().order('-date').fetch(limit=1, offset=0)[0]
        latest_date = latest_obj.date
        for gov in govs:
            endpos = (latest_date.toordinal() - gov.end.toordinal())*oneDayPx + MARGIN
            beginpos = (latest_date.toordinal() - gov.begin.toordinal())*oneDayPx +MARGIN
            textpos_center = (beginpos + endpos)/2
            textpos_onethird = (beginpos + endpos)/3
            textpos_twothird = (beginpos + endpos)*2/3
            gov.pixel = [int(beginpos),int(endpos),int(textpos_center),int(textpos_onethird),int(textpos_twothird)]
            gov.save()
    
    def reBuildPhoto(self, MARGIN):
        latest_obj = PollRating.all().order('-date').fetch(limit=1, offset=0)[0]
        latest_date = latest_obj.date
        photos = PhotoAttr.all()
        for photo in photos:
            pos = (latest_date.toordinal() - photo.date.toordinal())*oneDayPx + MARGIN
            photo.pixel = int(pos)
            photo.save()
        

class government(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            self.redirect(users.create_login_url(self.request.uri))
            return
        datas = Government.all().order('-begin')
        
        params = {'datas':datas,'nickname':user.nickname()}
        fpath = os.path.join(os.path.dirname(__file__), 'views', 'government.html')
        html = template.render(fpath, params)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(html)
        
    
    def post(self):
        mid = self.request.get('mid')
        if mid:
            data = Government.get_by_id(long(mid))
            data.delete()
        else:
            '''pref = Preference.all().fetch(limit=1, offset=0)'''
            go_name = self.request.get('go_name')
            begindatetime = datetime.strptime(self.request.get('begin').encode('utf-8'), '%Y-%m-%d')
            begin = datetime.date(begindatetime)
            if self.request.get('end'):
                enddatetime = datetime.strptime(self.request.get('end').encode('utf-8'), '%Y-%m-%d')
                end = datetime.date(enddatetime)
            else:
                end = datetime.date(datetime.today())
            now_flg = self.request.get('now_flg')
            
            obj = Government(name=go_name, begin=begin, end=end, now_flg= now_flg)
            obj.save()
            
        self.redirect('/redirect?url=/government')


class photoSet(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            self.redirect(users.create_login_url(self.request.uri))
            return
        mid = self.request.get('delitem')
        if mid:
            deldata = PhotoAttr.get_by_id(long(mid))
            deldata.delete()
            self.redirect('/redirect?url=/photo')
        
        photos = PhotoAttr.all().order('-date')
        params = {'photos':photos,'nickname':user.nickname()}
        fpath = os.path.join(os.path.dirname(__file__), 'views', 'photoset.html')
        html = template.render(fpath, params)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.headers['Cache-Control'] = 'no-cache'
        self.response.out.write(html)
        
    def post(self):
        mid = self.request.get('mid')
        if mid:
            moddata = PhotoAttr.get_by_id(long(mid))
            ndatetime = datetime.strptime(self.request.get('date').encode('utf-8'), '%Y-%m-%d')
            ndate = datetime.date(ndatetime)
            moddata.date=ndate
            moddata.save()
            
        else:
            url = self.request.get('photo_url')
            title = self.request.get('photo_title')
            width = int(self.request.get('width'))
            ndatetime = datetime.strptime(self.request.get('date').encode('utf-8'), '%Y-%m-%d')
            ndate = datetime.date(ndatetime)
            
            data = PhotoAttr(title=title,date=ndate, img_url=url, width=width)
            data.save()
        self.redirect('/redirect?url=/photo')
        

        

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/HistoricalTable',HistoricalTablePage),
                                      ('/HTPost', HTPost),
                                      ('/graph', GraphPage),
                                      ('/graphPost',graphPost),
                                      ('/redirect',myRedirect),
                                      ('/generate',htmlGenerate),
                                      ('/government',government),
                                      ('/photo',photoSet)
#                                      ,('/initdata',initDATA)
                                      ],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
