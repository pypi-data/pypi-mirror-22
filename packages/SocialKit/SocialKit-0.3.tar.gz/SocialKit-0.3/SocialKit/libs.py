import json, re
from qlib.net import to
from pyquery import PyQuery as pq
from urllib.parse import urlencode
from .phantomjs import WebDriver
from hashlib import md5
from .log import show
from json import dumps

GOT_IMG_RE = re.compile(r'(http[s]?://[\w\.\?\!\;\=\-\/]+?\.(?:png|jpg))')


def clound_get(spide_url, url, charset='',method='requests',proxy=None, **kargs):
    """
    
    @proxy socks5://127.0.0.1:1080

    """
    args = dict()
    args['url'] = url
    args['method'] = method
    if proxy:
        kargs['proxy'] = proxy

    args['options'] = dumps(kargs)
    args['charset'] = charset

    r = to(spide_url, method='post', data=args)
    if r.status_code == 200:
        return r.json()
    else:
        return {'code':400}


class People:
    """
        people info save here.
        @init
            p = People(name, desc, user_id, loc, date,....)
        
        @set some info to a people:
            People.set('people name', {..dict.})
        
        @find people
            People.find('people fuzz name')
            p.find_other('people fuzz name')
    """
    peoples = dict()
    peoples_name = set()

    def __init__(self, name, desc=None, user_id=None, linkedin=None, linkedin_img=None ,twi=None, twi_img=None,loc=None, date=None, face=None,face_img=None, **kargs):
        self.name = name
        self.loc = loc
        self.date = date
        self.user_ids = None
        self.img = None
        self.face = face
        self.face_img = face_img
        self.twi = twi
        self.twi_img = twi_img

        self.linkedin = linkedin
        self.linkedin_img = linkedin_img
        self.desc = desc
        for k in kargs:
            setattr(self, k, kargs[k])

        People.peoples[name] = self
        People.peoples_name.add(name)

    @staticmethod
    def find(name):
        for i in People.peoples_name:
            if name in i:
                yield People.peoples[i]

    def find_other(self, name):
        for i in People.peoples_name:
            if name in i:
                yield People.peoples[i]

    @staticmethod
    def set(name, info):
        if not isinstance(info, dict):
            raise Exception("must be a dict")
        
        People.peoples[name][k] = info

    def __getitem__(self, name):
        return People.peoples[name]



    def __setitem__(self, name, info):
        if not isinstance(info, dict):
            raise Exception("must be a dict")
        for k in info:
            setattr(self, k, info[k])


    def __hash__(self):
        return id(self)


class Twitter:
    S_URL = 'https://twitter.com/{user}'
    URL =  'https://twitter.com/i/profiles/show/{user}/timeline/tweets?include_available_features=1&include_entities=1&lang=en&max_position={po}&reset_error_state=false'
    def __init__(self, user, proxy=None):
        self.user = user
        self.session, init_res = to(Twitter.S_URL.format(user=user), cookie=True, proxy=proxy)
        self.init = init_res.content
        self.min_id, self.max_id = self.get_id_range(self.init)
        self.has_more = True
        self.values = {i.attr("data-tweet-id"):TwMsg(i) for i in  pq(self.init)("div.stream-container")("li.stream-item > div.tweet")}

    def get_id_range(self, cc):
        min_position = pq(cc)("div.stream-container").attr("data-min-position")
        max_position = pq(cc)("div.stream-container").attr("data-max-position")
        return int(min_position), int(max_position)

    
    def get(self):
        j = self.session.get(Tw.URL.format(user=self.user, po=self.min_id)).json()
        self.min_id = j['min_position']
        self.has_more = j['has_more_items']
        self.values += {i.attr("data-tweet-id"): TwMsg(i) for i in  pq(j['items_html'])("li.stream-item > div.tweet")}


    @classmethod
    def get_user_twitter(cl, user):
        c = cl(user)
        while c.has_more:
            c.get()
        return c.values

    def search(self, key):
        keys = []
        for i in self.values:
            if i.search(key):
                keys.append(i)

    def __getitem__(self,id):
        return self.values.get(id)

class TwMsg:

    def __init__(self, pq_data):

        if isinstance(pq_data, pq):
            self.r = pq_data
        else:
            self.r = pq(pq_data)

        self.id = self.r.attr("data-tweet-id")
        self.txt = self.r.html()


        self.time_s = int(self.r("div.stream-item-header>small.time>a>span").attr("data-time"))
        self.time = time.ctime(self.time_s)
        self.mark = self.r("div.context>div.js-retweet-text")
        self.text = self.r("div.js-tweet-text-container")
        self.media = self.r("div.AdaptiveMediaOuterContainer")
        self.reply = self.r("div.ReplyingToContextBelowAuthor")
        self.imgs = GOT_IMG_RE.findall(self.r)

    
    def search(self, key):
        if key in self.txt:
            return True
        return False  


class Facebook:
    url = 'https://www.facebook.com/{user}'
    def __init__(self, user, proxy=None):
        self.user = user
        self.browser = WebDriver(proxy=proxy)

        init_url = Facebook.url.format(user=user)
        self.browser.get(init_url)
        self.raw = pq(self.browser.page)
        self.name = self.raw("span#fb-timeline-cover-name").text()
        self.education = [pq(i).text() for i in self.raw("div#pagelet_eduwork")]
        self.homwtow = [pq(i).text() for i in self.raw("div#pagelet_hometown")]
        self.imgs = self.extract_img(self.raw)
        self.fav = self.raw("div.phs").text()

    def extract_img(self, i):
        return GOT_IMG_RE.findall(i.html())
    
    @staticmethod
    def search(user, proxy=None):
        browser = WebDriver(proxy=proxy)
        result = []
        
        u = Facebook.url.format(user='public/{user}?page=1'.format(user=user))
        show(u)
        browser.get(u, timeout=None)
        html = pq(browser.page)
        for i in html("div#BrowseResultsContainer > div"):
            one = pq(i)
            msg = one.text().replace("See Photos","")
            name = one("div > div > div > div >div >div > div > a ").text()
            show(name)
            face = None
            face_img = one("img").attr("src")
            for l in one("a")[:2]:
                link =l.attrib['href']
                if not link.endswith("photos"):
                    face = link
            p = People(name, desc=msg, face=face, face_img=face_img)
            result.append(p)

        return result,html, browser


            




class Google:
    def __init__(self, driver=None, proxy=None):
        self.google_url = "https://www.google.com/search?"
        self.base_key = {
            "num":100,
            "start":0,
            "meta":"",
            "hl":"en",
            "q": None,
        }
        if driver:
            self.web = driver
        else:
            self.web = WebDriver(proxy=proxy)

    def search(self, key):
        base_key = self.base_key
        base_key['q'] = key
        url = self.google_url + urlencode(base_key)
        self.web.get(url)
        return [GoogleMsg(pq(i)) for i in pq(self.web.page)("div.g")]

class GoogleMsg:

    def __init__(self, i):

        self.href = i("div.rc > h3.r > a").attr('href')
        self.name = i("h3 > a").text()
        if i("div.img-brk").text():
            self.text = ' Images Boxes'
        elif self.href and self.name:
            self.text = i.text().replace(self.href,'').replace(self.name,'')
        else:
            self.text = i.text()

        self.imgs = ''.join(['<img class="img-circle" src="{src}" style="height:50px;width:50px" ></img>'.format(src=im) for im in self.extract_img(i)])

    def extract_img(self, i):
        return GOT_IMG_RE.findall(i.html())

    def to_msg(self):
        t = """
            <div>
            <span id='title-span' style="border-left-color: rgba(209, 86, 104, 0.92);border-left-width: 7px;background-color:#f3f3f3; ">
                <a href="{href}" >{con}</a>
            </span>
                <div style="font-weight: 100;">{content}</div>
                <div class='content-imgs' >
                    {img}
                </div>
            <div  style="height: 1px;background-color: gray;left: 10px;width: 60%;margin-bottom: 2px;margin-left: -11px"></div>
                
            </div>
            """.format(href=self.href,con=self.name,content=self.text, img=self.imgs)
        return t

    def __repr__(self):
        if not self.name and not self.href:
            return super().__repr__()
        if not self.name:
            return "| " + self.href
        if not self.href:
            return self.name + " |"
        return self.name + " | " + self.href

class Linkedin(Google):
    
    def search(self, key):
        return super().search("site:linkedin.com/in " + key)

