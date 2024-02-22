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
        return

    def process_item(self,item,spider):
        if re.search(r"listing",spider.name):
            self.save_new_entry_locally(ItemAdapter(item), spider)
        elif re.search(r"post",spider.name):
            self.save_detailed_entry_locally(ItemAdapter(item), spider)

# class StoreRawJobOfferPipeline:

#     def save_new_entry(self, adapter, spider):
        
#         request_url = RAW_JOBS_API_ROOT_URL + ":" + RAW_JOBS_API_PORT + RAW_JOBS_API_JOBS_EXTENSION + '/create'
#         jwt = spider.jwt
#         headers = {'Authorization': f'Bearer {jwt}'}
#         adapter['scanned_date'] = datetime.now(timezone.utc)
#         line = json.dumps(adapter.asdict(), default=str) + "\n"
        
#         response = requests.request("POST", request_url, headers=headers, data=line)
#         if response.status_code == 201:
#             return_dict = {'id': response.json()["new_entry_id"], 'posting_url': adapter["posting_url"]}
#             response = requests.request("POST", "http://localhost:6800/schedule.json", data={'project':'entremed', 'spider': 'cltrabpost', 'id': return_dict['id'], 'url':return_dict["posting_url"]})
#             return 
#         else:
#             return {}
    
#     def save_detailed_entry(self, adapter, spider):
        
#         request_url = RAW_JOBS_API_ROOT_URL + ":" + RAW_JOBS_API_PORT + RAW_JOBS_API_JOBS_EXTENSION + '/update/' + str(adapter["id"])
#         jwt = spider.jwt
#         headers = {'Authorization': f'Bearer {jwt}'}
#         line = json.dumps(adapter.asdict(), default=str) + "\n"

#         response = requests.request("PUT", request_url, headers=headers, data=line)
#         if response.status_code == 204:
#             return
#         else:
#             return

#     def process_item(self,item,spider):

#         if re.search(r"listing",spider.name):
#             self.save_new_entry(ItemAdapter(item), spider)
#         elif re.search(r"post",spider.name):
#             self.save_detailed_entry(ItemAdapter(item), spider)

#         return item 
    