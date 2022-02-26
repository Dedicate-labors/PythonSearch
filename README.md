### 项目介绍：
本项目由Dedicate_labors和他的朋友一起完成，如有不妥求见谅

### 项目使用的开发工具和包
- 后端：
    - 环境：Liunx + python3.6+ + python异步
    - 使用的python包：
        - ruia异步爬取模块
        - 安装对应的ruia中间件第三方包，目的是为每次请求自动加上ua头pip install ruia-ua
            - 对ruia库进行了三次修改：两次在spider上，一次在item上
        - jieba模块进行字符串进行分词
        - MongoDB作为数据库，motor库操作数据库
        - sanic异步web框架，jinja2做html渲染
        - urllib.parse
    - 对spider库进行修改2-3处，现在有对sanic的json库进行修改

- 后端核心目录结构
    - Metaserach
        - app.py 总的启动项目的py文件
        - spider目录 爬取数据的爬虫   OK
        - config目录 存放配置(主要是Database的) OK
        - database目录 管理数据库   OK
        - utils目录 此文件狭存放自己封装的工具类函数，是一个共享的方法  OK
        - common目录 存放搜索部分的核心文件  --->记得清理二次查询时数据库的数据(达到一定量时)，这个也是要动脑的部分
        - views目录 视图文件目录
        - statics, templates存放前端的文件(这里可能不需要使用)
    - 使用的pageRank算法
        - 每页越靠前分值越高，每个浏览器爬去５页
        - 不同浏览器要是有相同的网址，分数叠加
        - 依靠分数进行排名

搜索引擎整理：
baidu,lookan

--  使用
- iData: https://search.cn-ki.net/search?keyword=..db=CFLS　//查询论文　慢
- 问答库: https://www.asklib.com/s/...  //问答案　　快
- 秘迹搜索：https://mijisou.com/?q=。。&category_general=on&time_range=&language=zh-CN&pageno=2　//通用　较快 
