from urllib.parse import quote, parse_qs
import random 
import sys
import asyncio
import re

from ruia import AttrField, Item, Request, Spider, TextField
# 请求头等信息在middleware中
from ruia_ua import middleware
# sys.path.append('/media/zxl/DATA/CODE/python_crazzy/搜索引擎学习/元搜索引擎')
from Metasearch.database.motor_base import MotorBase

class ArticleListItem(Item):
    """
    爬取单页面的内容
    """
    target_item = TextField(css_select="div.results_container > div.general_result")
    title = TextField(css_select='h3 > a')
    href = TextField(css_select='span.general_result_url')
    # 要保留的描述性文本
    hint_text = TextField(css_select='p.general_result_desc')

class LooKaoSpider(Spider):
    """
    针对搜索引擎：https://lookao.com/的爬虫
    """
    # 设置启动URL
    start_urls = []
    # 爬虫模拟请求的配置参数
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    # 请求信号量
    concurrency = 10
    web_nums = 0
    # 设置分数
    value = 0

    async def parse(self, res):
        # self.value = int(parse_qs(self.start_urls[0]).get('pageno')[0])
        # self.value = self.value*(-1) + 6
        self.value = self.page*(-1) + 6
        # rel_val是它本页的基本分
        # rel_val = self.value
        print(self.value) #基本分数不可以轻易改变

        self.mongo_db = MotorBase(loop=self.loop).get_db()
        async for item in ArticleListItem.get_items(html=res.html):
            rel_val = self.value
            is_url = await self.mongo_db.lookan.find_one({'url':item.href}) #查询是否有相同url

            new_title = "".join(re.findall('\w+', item.title)) #创建新的用于比较的title
            is_title = await self.mongo_db.lookan.find_one({'compstr':new_title})

            if not is_url and not is_title:
                # 随机休眠
                # self.request_config['DELAY'] = random.randint(5, 10)
                await self.save(item, rel_val,new_title)
            else:
                # 存在相同的就加原来的分
                # 1. url相同　２．compstr相同
                if is_url:
                    # url相同
                    rel_val += is_url.get('value')
                elif is_title:
                    # compstr相同
                    rel_val += is_title.get('value')
                    item.href = is_title.get('url')
                await self.save(item,rel_val,new_title)
    
    async def save(self, res, rel_val,new_title):
        hint_text = res.hint_text.replace('\n','').strip()
        title = res.title.replace('\n','').replace('\t','').strip()
        data = {
            'url':res.href,
            'title':title,
            'hint_text':hint_text,
            'compstr':new_title,
            'value':rel_val,
            'name':'lookan搜索'
        }

        try:
            await self.mongo_db.lookan.update_one({
                'url':data['url']},
                {'$set':data},
                upsert=True
            )
        except Exception as e:
            # 这里的self.logger是他默认本身的
            self.logger.exception(e)


async def main(search_text,loop):
    """
    param:参数，即要搜索的字段
    """
    for page in range(1, 6):
        print('start')
        url = "https://lookao.com/search?q=" + quote(search_text) + '&category_general=1&pageno='+str(page)
        await LooKaoSpider.async_start(middleware=middleware, loop=loop, url=url, page=page)
        break
    print('end')

if __name__ == "__main__":
    pass
