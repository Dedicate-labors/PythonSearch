import os
import sys
import time

from importlib import import_module
# sys.path.append('/media/zxl/DATA/CODE/python_crazzy/搜索引擎学习/元搜索引擎')
from Metasearch.utils.log import logger
from Metasearch.config import Config

def file_name(file_dir=os.path.join(Config.BASE_DIR, 'spider/sources'))->list:
    """
    得到爬虫类
    :param file_dir:
    :return list
    """
    all_files = []
    for file in os.listdir(file_dir):
        if file.endswith('_spider.py'):
            all_files.append(file.replace('.py', ''))
    return all_files

async def spider_console(loop):
    """
    该程序自动找到ｓources文件下的爬虫文件，并执行
    """
    start = time.time()
    all_files = file_name()
    for spider in all_files:
        spider_module = import_module(
            "Metasearch.spider.sources.{}".format(spider)
        )
        # print(spider_module)
        # spider_module.main(Config.search_txt,loop)
        await spider_module.main(Config.search_txt,loop)

if __name__ == "__main__":
    pass
