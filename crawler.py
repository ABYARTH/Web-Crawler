#!usr/bin/env python
from sys import argv
from collections import deque
from retriever import Retriever
from urlparse import urlparse
from time import ctime
from downloader import Downloader
from os.path import splitext

class Crawler(object):
    "crawler goes out to the web and downloads the web pages"
    _invalidExt=['.pdf','jpg','jpeg','.doc','docx','.gif','.zip','.rar','.PDF']
    def __init__(self):
        self.visited_links=[]
        self.links_queue=deque([])
        self.domain=''
        self.same_domain=True
      
            
    def crawlPage(self,url,same_domain=True):
        pageRetriever=Retriever()
        downloader=Downloader()
        retrieverResponse=downloader.download(url)
        
        if retrieverResponse==0:
            print retrieverResponse,"Invalid Url.....parsing skipped\n"
            return
        
        self.visited_links.append(url)
        
        try:
            links=pageRetriever.getLinks(url)
        except Exception:
            return
   
        
        for link in links:
            if link not in self.visited_links:
                if same_domain==True:
                    if urlparse(link)[1]!=self.domain:
                        print link," *** discarded for crawl .. not in domain\n"
                        pageRetriever.log.write("%s %s*** discarded for crawl .. not in domain\n"%(ctime(),link))
                    else:
                        if link not in self.links_queue:
                            if splitext(link)[1] not in self._invalidExt:
                                self.links_queue.append(link)
                                print link," *** new link added to crawl queue\n"
                                pageRetriever.log.write("%s %s *** new link added to crawl queue\n"%(ctime(),link))
                        else:
                            print link,"*** discarded already visited"
                            pageRetriever.log.write("%s %s *** discarded already visited\n"%(ctime(),link))
                    
                if same_domain==False:
                    if link not in self.links_queue:
                            self.links_queue.append(link)
                            print link," *** new link added to crawl queue\n"
                            pageRetriever.log.write("%s *** new link added to crawl queue\n"%link)
                    else:
                        print link,"*** discarded already visited"
                        pageRetriever.log.write("%s *** discarded already visited"%link)
                      
        print "lemgth of queue is ",len(self.links_queue), "len of visited queue is ",len(self.visited_links)
        pageRetriever.log.write("\n\nlength of queue is %d   length of visited queue is %d\n\n"%(len(self.links_queue),len(self.visited_links)))            
                    
                    
    def start_crawl(self,url,same_domain=True):
        self.links_queue.append(url)
        self.domain=urlparse(url)[1] 
        self.same_domain=same_domain              # process links in queue
        while self.links_queue:
            url = self.links_queue.popleft()
            self.crawlPage(url)
            
            
            
def main():
    if len(argv) > 1:
        url = argv[1]
    else:
        try:
            url = raw_input('Enter starting URL: ')
            
        except (KeyboardInterrupt, EOFError):
            url = ''

    if not url: return
    robot = Crawler()
    robot.start_crawl(url)

if __name__ == '__main__':
    main()