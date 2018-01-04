
# coding: utf-8

# In[ ]:


import os
import json
import requests
from uuid import uuid4
from bs4 import BeautifulSoup

class PttCrawler:
    
    def __init__(self, board, page, write=False):
        self.ptt_url = 'http://www.ptt.cc'
        self.board = board
        self.page = page
        
        self.session = requests.Session()
        self.session.cookies.update({
            'over18': '1'
        })
        
        self.write=write
        
    def run(self):
        url = self.ptt_url + '/bbs/' + self.board
        post_link_list = self.fetchPostLinkList(url)
        post_list = [self.fetchPost(post_link) for post_link in post_link_list]
#        if self.write:
#            result_dir = os.path.join('ptt_crawler/', str(uuid4()))
#            os.makefirs(result_dir, exist_ok=True)
#            
#            for post in post_list:
#                with open(os.path.join(result_dir, post['id']), 'w') as f:
#                    f.write(json.dumps(post, indent= 4))
        
        return post_list
    
    def fetchPostLinkList(self, url):
        if not url.startswith('http'):
            url = self.ptt_url + url
            
        html_list = []
        
        resp = self.session.get(url)
        
        soup = BeautifulSoup(resp.text.encode("utf-8"), "lxml")
        gossip_list = soup.find('div', {'class': 'r-list-container action-bar-margin bbs-screen'})
        
        link_list = gossip_list.find_all('a')
        for i in range(len(link_list)):
            html_list.append('http://www.ptt.cc' + link_list[i].get('href'))
#        html_list = [link.get('href') for link in link_list]
        
        if self.page > 1:
            for p in range(self.page - 1):
                paging_group = soup.find('div', {'class': 'btn-group btn-group-paging'})
                p_link = paging_group.find_all('a')
                p_link = p_link[1].get('href')
                new_url = 'http://www.ptt.cc' + p_link
            
                resp = self.session.get(new_url)
                soup = BeautifulSoup(resp.text.encode("utf-8"), "lxml")
                gossip_list = soup.find('div', {'class': 'r-list-container action-bar-margin bbs-screen'})
                link_list = gossip_list.find_all('a')
                
                for i in range(len(link_list)):
                    html_list.append('http://www.ptt.cc' + link_list[i].get('href'))
            
#        return 'http://www.ptt.cc' + p_link
        return html_list
    
    def fetchPost(self, url):
        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text.encode("utf-8"), "lxml")

        if soup.find('div', {'class': 'article-metaline'}):
            metaline = soup.find_all('div',{'class': 'article-metaline'})
            author = metaline[0].text
            title = metaline[1].text
            date = metaline[2].text
            content = metaline[2].next_sibling.strip()
        else:
            author = None
            title = None
            date = None
            content = None
            
                 
        return{'title': title, 'author': author, 'date': date, 'content': content}

