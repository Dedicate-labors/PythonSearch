from sanic import Sanic
import sys, os
# 下面的库用于异步缓存
# from aiocache import SimpleMemoryCache
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from Metasearch.views.bp_home import bp_home
from Metasearch.config import Config
from Metasearch.database.motor_base import MotorBase

app = Sanic(__name__)
app.blueprint(bp_home)

@app.listener('before_server_start')
def init_cache(app, loop):
    """
    初始化操作 对一些参数进行配置
    :param app:
    :param loop:
    :return:
    """
    # app.config['metasearch_config'] = Config
    # app.cache = SimpleMemoryCache()
    # eventloop获得
    app.config['loop'] = loop
    app.mongo_db = MotorBase(loop=loop).get_db()

if __name__ == "__main__":
    app.run(host='0.0.0.0', workers=2, port=8001, debug=False)
