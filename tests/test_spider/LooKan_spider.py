from urllib.parse import quote, parse_qs
import random 
import sys
import asyncio
import re

from ruia import AttrField, Item, Request, Spider, TextField
# 请求头等信息在middleware中
from ruia_ua import middleware
sys.path.append('/media/zxl/DATA/CODE/python_crazzy/搜索引擎学习/元搜索引擎')
from Metasearch.database.motor_base import MotorBase

class ArticleListItem(Item):
    """
    爬取单页面的内容
    """
    target_item = TextField(css_select="div.results_container > div.general_result")
    title = TextField(css_select='h3 > a')
    href = TextField(css_select='span.general_result_url')
    hint_text = TextField(css_select='p.general_result_desc')

async def save(res, mongo_db,value,new_title):
    data = {
            'url':res.href,
            'title':res.title,
            'hint_text':res.hint_text,
            'compstr':new_title,  #用于比较的字符串
            'value':value 
        }
    try:
        await mongo_db.lookan.update_one({
            'url':data['url']},
            {'$set':data},
            upsert=True
        )
    except Exception as e:
        pass

async def read():
    with open('LooKan.html', 'r') as f:
        html = f.read()
    mongo_db = MotorBase().get_db()
    async for item in ArticleListItem.get_items(html=html):
        is_url = await mongo_db.lookan.find_one({'url':item.href}) #查询是否有相同url

        new_title = "".join(re.findall('\w+', item.title)) #创建新的用于比较的title
        is_title = await mongo_db.lookan.find_one({'compstr':new_title})

        value = 5
        if not is_url and not is_title:
            await save(item,mongo_db,value,new_title)
        else:
            # 存在相同的就加分
            # 1. url相同　２．compstr相同
            if is_url:
                # url相同
                value += is_url.get('value')
            elif is_title:
                # compstr相同
                value += is_title.get('value')
                item.href = is_title.get('url')
            await save(item,mongo_db,value,new_title)
            
if __name__ == "__main__":
    asyncio.run(read())