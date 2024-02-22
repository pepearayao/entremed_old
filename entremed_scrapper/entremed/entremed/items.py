# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose
from scrapy.loader import ItemLoader


def remove_tabs(value):
    return value.replace("\t", "")

def remove_line_jumps(value):
    return value.replace("\r", "").replace("\n", "")

def remove_comma(value):
    return value.replace(",", "")

def strip_string(value):
    return value.strip()

def remove_single_quote(value):
    return value.replace("\'", "")


class BaseRawOfferItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    source_url = scrapy.Field()
    posting_url = scrapy.Field()
    geolocalization = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    experience = scrapy.Field()
    work_schedule = scrapy.Field()
    shift_type = scrapy.Field()
    employment_type = scrapy.Field()
    slots_available = scrapy.Field()
    urgency_required = scrapy.Field()
    seniority_level = scrapy.Field()
    driving_level = scrapy.Field()
    posting_service = scrapy.Field()
    description = scrapy.Field()
    requisites = scrapy.Field()
    pills = scrapy.Field()
    inclusive_posting = scrapy.Field()
    published_date = scrapy.Field()
    closing_date = scrapy.Field()
    scanned_date = scrapy.Field()
    normalized_date = scrapy.Field()
    filtered_posting = scrapy.Field()
    detailed_scan = scrapy.Field()

class BaseRawOfferLoader(ItemLoader):
    default_item_class = BaseRawOfferItem
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    geolocalization_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    company_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    salary_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    experience_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    work_schedule_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    shift_type_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    employment_type_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    slots_available_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    seniority_level_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)
    driving_level_in = MapCompose(remove_tabs, remove_comma, strip_string, remove_single_quote)

    pills_in = Compose(lambda v: " ".join(v),remove_tabs, remove_line_jumps, remove_single_quote)
    description_in = Compose(lambda v: " ".join(v), remove_tabs, remove_line_jumps, remove_single_quote)

class ClTrabItemLoader(BaseRawOfferLoader):
    inclusive_posting_in = MapCompose(lambda x: True if x != [] else False)
    
class CompuTrabItemLoader(BaseRawOfferLoader):
    posting_url_in = MapCompose(lambda v: "https://cl.computrabajo.com" + v.split("#")[0])

class LaborumItemLoader(BaseRawOfferLoader):
    posting_url_in = MapCompose(lambda v: "https://www.laborum.cl" + v.replace("'","\\'"))