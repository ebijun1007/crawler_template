# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
from dataclasses import dataclass, field
from typing import Optional

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

@dataclass
class BaseItem(scrapy.Item):
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)

class BaseProcessor():
    def extract_numbers(text):
      match = re.match(r'(\d+)', text)
      if match:
          return match.group(0)

class BaseItemLoader(ItemLoader):
    item_class = BaseItem
    processor = BaseProcessor()

    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
