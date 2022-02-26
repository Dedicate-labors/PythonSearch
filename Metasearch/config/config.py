import os

class Config():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # 为保证不出错，提前再mongodb上创建数据库metasearch
    MONGODB = dict(
        MONGO_HOST=os.getenv('MONGO_HOST', ""),
        MONGO_PORT=int(os.getenv('MONGO_PORT', 27017)),
        MONGO_USERNAME=os.getenv('MONGO_USERNAME', ""),
        MONGO_PASSWORD=os.getenv('MONGO_PASSWORD', ""),
        DATABASE='metasearch',
    )
    # 查询文本
    search_txt = ''
    # 查询次数记录，一旦到一定次数清空数据库
    findNum = 0
    
print(Config.BASE_DIR)  #存储有路径
print(os.path.dirname(Config.BASE_DIR))