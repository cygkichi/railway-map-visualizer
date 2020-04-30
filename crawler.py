# -*- coding: utf-8 -*-
"""This module is xxx. """
import logging
from get_stationinfo import get_stationinfo

class Crawler(object):
    def __init__(self):
        self.mode          = None
        self.waiting_time  = None
        self.start_article = None
        self.max_distance  = None
        self.num_steps     = None
        self.count_steps   = 0
        self.station_infos = set()
        self.done_articles = set()
        self.task_articles = set()

    def select_next_article(self):
        pass

    def step(self):
        pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    start_article = '/wiki/淀屋橋駅'
    logging.debug('Start crawler.py !')
    logging.debug('start_article : '+start_article)
