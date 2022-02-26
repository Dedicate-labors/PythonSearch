import sys
import time

from sanic import Blueprint
from sanic.response import json, text
# sys.path.append('/media/zxl/DATA/CODE/python_crazzy/搜索引擎学习/元搜索引擎')

from Metasearch.config import Config
from Metasearch.common.common_tools import gen_sortdb

bp_home = Blueprint(__name__)
# 开启异步特性  要求3.6+
enable_async = sys.version_info >= (3,6)

@bp_home.route('/search')
async def index(request):
    #query是查询参数
    query = str(request.args.get('q','')).strip()
    #fucnName是callback函数名
    funcName = str(request.args.get('callback', '')).strip()
    print(query)
    result = []
    if query:
        Config.search_txt = query
        result = await gen_sortdb(request.app.config['loop'], request.app.mongo_db)
        return json(result, funcName=funcName)
        # result = funcName + '(' + str(result) + ')'
        # return text(result)
        # cache_result = await request.app.cache.get(query)
        # if cache_result:
        #     # 如果存在缓存
        #     result = cache_result
        # else:
        #     result = await gen_sortdb()
        #     await request.app.cache.set(query, result)
    else:
        return text("请输入查询关键词！！")

@bp_home.route('/')
async def orign(request):
    funcName = str(request.args.get('callback', '')).strip()
    return text([{"name":"hello world"}], funcName=funcName)
