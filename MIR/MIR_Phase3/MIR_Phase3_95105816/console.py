import os
from elasticsearch import Elasticsearch
import json

import scrapy
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.dupefilters import RFPDupeFilter
import os
sys.path.append("..")
from items import MirPhase3Item
import re
import time

import json
from collections import defaultdict
from math import fabs
import json

import sys
sys.path.append('../MIR_Phase3/spiders/')


typ = input("Enter file to run:\n")
if typ == "1":
    from my_spider import *
elif typ == "2":
    from index import *
elif typ == "3":
    from page_rank import *
elif typ == "4":
    from search import *
elif typ == "5":
    from HITS import *

else:
    print("Invalid option.")
