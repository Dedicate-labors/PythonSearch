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
    target_item = TextField(css_select="div#content_left > div")
    title = TextField(css_select='h3.t > a')
    href = AttrField(css_select='h3.t > a', attr='href')
    # 可能要保留的文本 这里有错
    hint_text = TextField(css_select='div.c-abstract', default='')

def main(search_text):
    """
    param:参数，即要搜索的字段
    """
    for page in range(0, 6):
        print('start')
        url = "https://www.baidu.com/s?wd=" + quote(search_text) + '&pn='+str(page*10)+'&oq='+quote(search_text)+'&ie=utf-8'
        print(url)
        LooKaoSpider.start(middleware=middleware, url=url)
        break
    print('end')

async def save(res, mongo_db,value,new_title):
    data = {
            'url':res.href,
            'title':res.title,
            'hint_text':res.hint_text,
            'compstr':new_title,
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
    with open('baidu.html', 'r') as f:
        html = f.read()
    mongo_db = MotorBase().get_db()
    async for item in ArticleListItem.get_items(html=html):
        if item.title:
            is_url = await mongo_db.lookan.find_one({'url':item.href}) #查询是否有相同url
            new_title = "".join(re.findall('\w+',item.title)) #创建新的用于比较的title
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
    # main('微信')
    asyncio.run(read())
    """
    根据观察得pn掌管翻页，wd和oq掌管查询对象 sum对象要变-->去掉
    保留wd，pn, oq, ie
    """
    'wd=python3&pn=0&oq=python3&ie=utf-8&usm=2'
    'wd=python3&pn=10&oq=python3&ie=utf-8&usm=2'
    'wd=python3&pn=20&oq=python3&ie=utf-8&usm=2'
    'wd=python3&pn=30&oq=python3&ie=utf-8&usm=2'

    'ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=微信&oq=python'
    'wd=微信&pn=10&oq=微信&ie=utf-8&usm=4'
    'wd=微信&pn=20&oq=微信&ie=utf-8&usm=4'