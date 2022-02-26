import os
import sys
import jieba

# sys.path.append('/media/zxl/DATA/CODE/python_crazzy/搜索引擎学习/元搜索引擎')
from Metasearch.database.motor_base import MotorBase
from Metasearch.config import Config
from Metasearch.spider.spider_console import spider_console

def gen_stop_words():
    print(Config.BASE_DIR)
    with open(os.path.join(Config.BASE_DIR, 'common/stop_words.txt'), 'r') as fp:
        stop_words = [_.strip() for _ in fp.readlines()]
    return stop_words

def text_seg(text: str, stop_words: list = None) -> list:
    seg_list = []
    if not stop_words:
        stop_words = gen_stop_words()
    for each in jieba.cut(text):
        if each not in stop_words and not each.isspace():
            # 对于单词 全部默认小写
            seg_list.append(each.lower())

    return seg_list

def dbSearch_segList():
    ret = text_seg(Config.search_txt)
    # db.lookan.find({'$and':[{'compstr':{'$regex':'高数'}},{'compstr':{'$regex':'思考'}}]})
    L = []
    print(ret)
    for it in ret:
        mb  = {'compstr':{'$regex':it,'$options':'i'}}
        L.append(mb)
    return L

async def ret_json(db_cursor):
    result_list = []
    async for item in db_cursor:
        doc_data = {
            'title':item.get('title'),
            'url':item.get('url'),
            'hint_text':item.get('hint_text')
        }
        result_list.append(doc_data)
    return result_list

async def gen_sortdb(loop,mongo_db):
    """
    对搜索结果排序
    """
    # 进行数据库查询
    Config.findNum += 1
    if Config.findNum >= 30:
        mongo_db.lookan.deleteMany({})
    #返回数据库查询seg_list
    L = dbSearch_segList()
    print(L)
    #sort：1为升序，-1为降序，默认升序
    db_cursor = mongo_db.lookan.find({'$and':L}).sort('value',-1)
    final_list = await ret_json(db_cursor)
    # 可能出现的问题：上一次爬取的结果被这一次搜索使用到；但只要爬取的多就行
    if final_list:
        return final_list
    else:
        # 存储搜索结果
        print('开始搜索:',loop)
        # spider_console(loop)
        await spider_console(loop)
        db_cursor = mongo_db.lookan.find({'$and':L}).sort('value',-1)
        return await ret_json(db_cursor)

if __name__ == "__main__":
    Config.search_txt = 'CPU组成'
    L = dbSearch_segList()
    print(L)
