import sys
import threading
import queue
import time

from crawler import *
from bloom_filter import *


def working(max_page, thread):
    '''
    Task for a single thread.

    Input: `max_page`: rough limit to the number of pages to be crawled
                       (Likely to exceed)
           `thread`: label of current thread
    Output: None
    Global: `crawled`: URLs of the crawled pages
            `varLock`: lock of `crawled`
            `q`: tasks to be done
    '''
    while True:
        page = q.get()  # Get a URL to be crawled

        terminate, to_crawl = False, False
        if varLock.acquire():  # Try to acquire the lock
            terminate = len(crawled) >= max_page  # Terminate the current thread
            to_crawl = not crawled.find(page)  # URL not recorded
            varLock.release()
        
        if terminate:
            return
        
        if to_crawl:
            print(page, thread)  # Indicate the thread crawling the page
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            for link in outlinks:
                q.put(link)
            if varLock.acquire():  # Try to acquire the lock
                crawled.add(page)
                varLock.release()
            time.sleep(0.5)  # Added for politeness
        q.task_done()  # Task finished


# Variables here are shared by multiple threads
NUM = 4
crawled = None  # To be initialized in `main`
varLock = threading.Lock()
q = queue.Queue()


def crawl_bloom_filter(seed, max_page):
    q.put(seed)
    
    threads = []  # Store all the threads
    for i in range(NUM):
        t = threading.Thread(target=working, args=(max_page, i))  # Add the arguments for `working`
        threads.append(t)
        t.setDaemon(True)
        t.start()
    
    for t in threads:
        t.join()  # Wait for all the threads to terminate


if __name__ == '__main__':

    seed = sys.argv[1]
    max_page = int(sys.argv[2])

    crawled = BloomFilter(max_page, BKDRHash)  # Initialize `crawled` as BloomFilter
    crawl_bloom_filter(seed, max_page)