from urllib.parse import quote, parse_qs
import random 
import sys
import asyncio

from ruia import AttrField, Item, Request, Spider, TextField
# 请求头等信息在middleware中
from ruia_ua import middleware
sys.path.append('/media/zxl/DATA/CODE/python_crazzy/搜索引擎学习/元搜索引擎')
from Metasearch.database.motor_base import MotorBase

class ArticleListItem(Item):
    """
    爬取单页面的内容
    """
    # target_item = TextField(css_select="#main_results > div.default-container > h4")
    title = TextField(css_select='h4.result_header > a')
    href = AttrField(css_select='h4.result_header > a', attr='href')
    # 可能要保留的文本 有的并没有这个
    hint_text = TextField(css_select='p.result-content',default="")

class LooKaoSpider(Spider):
    """
    针对搜索引擎：https://www.baidu.com/ 的爬虫
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
        self.value = self.page*(-1) + 6
        print(self.value) #基本分数不可以轻易改变

        # self.mongo_db = MotorBase(loop=self.loop).get_db()
        with open('miji.html', 'w') as f:
            f.write(res.html)
        results = await ArticleListItem.get_multiitems(html=html)
        length = len(results['href'])
        # 存储字段
        item_href =  ''
        item_title = ''
        hint_text = ''
        for i in range(0, length):
            rel_val = self.value
            item_href = results['href'][i]
            item_title = results['title'][i]
            hint_text = results['hint_text'][i]

            is_url = await self.mongo_db.lookan.find_one({'url':item_href}) #查询是否有相同url

            new_title = "".join(re.findall('\w+', item_title)) #创建新的用于比较的title
            is_title = await mongo_db.lookan.find_one({'compstr':new_title})

            if not is_url and not is_title:
                # 随机休眠
                # self.request_config['DELAY'] = random.randint(5, 10)
                await self.save(item_href, item_title, hint_text, rel_val,new_title)
            else:
                # 存在相同的就加原来的分
                # 1. url相同　２．compstr相同
                if is_url:
                    # url相同
                    rel_val += is_url.get('value')
                elif is_title:
                    # compstr相同
                    rel_val += is_title.get('value')
                    item_href = is_title.get('url')
                await self.save(item_href, item_title, hint_text, rel_val,new_title)
                
    
    async def save(self,item_href,item_title,hint_text, rel_val, new_title):
        data = {
            'url':item_href,
            'title':item_title,
            'hint_text':hint_text,
            'compstr':new_title,
            'value':rel_val
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


def main(search_text):
    """
    param:参数，即要搜索的字段
    """
    for page in range(1, 6):
        print('start')
        url = "https://mijisou.com/?q="+quote(search_text)+"&category_general=on&time_range=&language=zh-CN&pageno="+str(page)
        print(url)
        LooKaoSpider.start(middleware=middleware, url=url, page=(page+1))
        break
    print('end')

async def read():
    with open('miji.html', 'r') as f:
        html = f.read()
    # mongo_db = MotorBase().get_db()
    # async for item in ArticleListItem.get_items(html=html):
    results = await ArticleListItem.get_multiitems(html=html)
    length = len(results['href'])
    print(length)
    for i in range(0, length):
        print(i)
        data = {
            'url':results['href'][i],
            'title':results['title'][i],
            'hint_text':results['hint_text'][i]
            # 'compstr':new_title,
            # 'value':rel_val
        }

        print(data)
        # try:
        #     await self.mongo_db.lookan.update_one({
        #         'url':data['url']},
        #         {'$set':data},
        #         upsert=True
        #     )
        # except Exception as e:
        #     # 这里的self.logger是他默认本身的
        #     self.logger.exception(e)

if __name__ == "__main__":
    # main('神之塔')
    asyncio.run(read())
