# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from datetime import datetime, timezone

class StoreRawJobOfferPipeline:
    def save_new_entry_locally(self, adapter, spider):

        adapter['scanned_date'] = datetime.now(timezone.utc)
        spider.jobpostings.append(adapter)

        return

    def save_detailed_entry_locally(self, adapter, spider):
        spider.detailed_scan = adapter
        return

    def process_item(self,item,spider):
        if re.search(r"listing",spider.name):
            self.save_new_entry_locally(ItemAdapter(item), spider)
        elif re.search(r"post",spider.name):
            self.save_detailed_entry_locally(ItemAdapter(item), spider)
