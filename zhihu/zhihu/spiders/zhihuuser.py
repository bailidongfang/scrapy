# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import json
from zhihu.items import ZhihuItem,FollowItem

class ZhihuuserSpider(Spider):
    name = 'zhihuuser'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user = 'excited-vczh'
    user_url='https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query='allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def dict_user(self,json_dict):
        useritem=ZhihuItem()
        for a in useritem.fields:
            if a in json_dict.keys():
               useritem[a]=json_dict.get(a)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('++++++++++++++++++++++++++++++user+++++++++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(useritem)
        return useritem
    def dict_follow(self,json_dict):
        followitem=FollowItem()
        for a in json_dict.get('data'):
            for b in followitem.fields:
                if b in a.keys():
                    followitem[b]=a.get(b)
            print('++++++++++++++++++++++follow++++++++++++++++++++++')
            for x in followitem.fields:
                print(x+':'+followitem[x])

    def parse_user(self, response):
        json_dict_user=json.loads(response.text)
        self.dict_user(json_dict_user)


        # yield Request(self.follows_url.format(user=json_dict_user.get('url_token'),include=self.follows_query,limit=20, offset=0),self.parse_follows)

    def parse_follows(self, response):
        json_dict_follow=json.loads(response.text)
        self.dict_follow(json_dict_follow)

    def start_requests(self):
        # yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,limit=20,offset=0),self.parse_follows)
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)