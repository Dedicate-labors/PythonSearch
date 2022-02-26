from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test():
    client = AsyncIOMotorClient()
    db = client['metasearch']
    # print(is_exist)
    value = 5
    data = {
        'url':'https://wx.qq.com/',
        'title':'微信网页版 - QQ',
        'value':value
    }
    # await db.lookan.update_one({
    #     'url':'http://www.baidu.com'},
    #     {'$set':data},
    #     upsert=True
    # )
    is_exist = await db.source_docs.find_one({'url':'https://wx.qq.com/'})
    print(type(is_exist),is_exist.get('value'))

if __name__ == "__main__":
    # 获取find_one的内容
    asyncio.run(test())
