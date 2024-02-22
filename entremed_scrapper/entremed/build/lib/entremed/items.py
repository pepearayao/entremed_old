# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join


def clean_description(value):
    return value.replace("\r", "").replace("\n", "").replace("\t", "")

def clean_company(value):
    return clean_description(value.strip().replace(",", ""))


class RawJobItem(scrapy.Item):
    id = scrapy.Field(
        output_processor = TakeFirst()
    )
    title = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst() 
    )
    source_url = scrapy.Field(
        output_processor = TakeFirst() 
    )
    posting_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    geolocalization = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    company = scrapy.Field(
        input_processor = MapCompose(clean_company),
        output_processor = TakeFirst() 
    )
    salary = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    experience = scrapy.Field()
    work_schedule = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()        
    )
    shift_type = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()        
    )
    employment_type = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst() 
    )
    slots_available = scrapy.Field()
    urgency_required = scrapy.Field()
    seniority_level = scrapy.Field()
    driving_level = scrapy.Field()
    posting_service = scrapy.Field(
        output_processor = TakeFirst() 
    )
    description = scrapy.Field(
        input_processor = MapCompose(clean_description),
        output_processor = TakeFirst()
    )
    requisites = scrapy.Field()
    pills = scrapy.Field(
        output_processor = TakeFirst()
    )
    inclusive_posting = scrapy.Field(
        input_processor = MapCompose(lambda x: True if x != [] else False),
        output_processor = TakeFirst()
    )
    published_date = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()           
    )
    closing_date = scrapy.Field()
    scanned_date = scrapy.Field()
    normalized_date = scrapy.Field()
    filtered_posting = scrapy.Field()
    detailed_scan = scrapy.Field()

    


