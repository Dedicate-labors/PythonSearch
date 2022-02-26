import os
import sys
import asyncio

sys.path.append('/media/zxl/DATA/CODE/python_crazzy/搜索引擎学习/元搜索引擎')
from Metasearch.database.motor_base import MotorBase
from Metasearch.config import Config
from Metasearch.spider.spider_console import spider_console

async def gen_sortdb():
    """
    对搜索结果排序
    """
    # 缓存爬取的数据
    # spider_console(Config.search_txt)

    # 进行数据库查询
    db = MotorBase().get_db()
    # .sort({"value": -1}).pretty()
    db_cursor = db.lookan.find().sort('value',-1)
    #sort：1为升序，-1为降序，默认升序
    result_list = []
    async for item in db_cursor:
        doc_data = {
            'title':item.get('title'),
            'url':item.get('url')
            # 'hint_text':item.hint_text
        }
        result_list.append(doc_data)
    return result_list

if __name__ == "__main__":
    rest = asyncio.run(gen_sortdb())
    print(rest)
