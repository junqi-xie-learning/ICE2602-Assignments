# SJTU EE208

import sys
import threading
import queue
import time

from crawler import *


def crawl_multi_thread(max_page, thread):
    while True:
        page = q.get()

        to_crawl = False
        if varLock.acquire():
            to_crawl = page not in crawled and len(crawled) < max_page
            varLock.release()
        
        if to_crawl:
            print(page, thread)
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            for link in outlinks:
                q.put(link)
            if varLock.acquire():
                graph[page] = outlinks
                crawled.append(page)
                varLock.release()
            time.sleep(0.5) # Added for politeness
        q.task_done()


NUM = 4
crawled = []
graph = {}
varLock = threading.Lock()
q = queue.Queue()


def main(seed, max_page):
    q.put(seed)
    
    for i in range(NUM):
        t = threading.Thread(target=crawl_multi_thread, args=(max_page, i))
        t.setDaemon(True)
        t.start()
    q.join()


if __name__ == '__main__':

    seed = sys.argv[1]
    max_page = int(sys.argv[2])

    crawled = main(seed, max_page)