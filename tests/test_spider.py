# import requests

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie': 'BIDUPSID=70C2AB724E6A8CC77B7599D4D5FDDDF8; PSTM=1575694359; BAIDUID=70C2AB724E6A8CC771CBD31FC27A4D7D:FG=1; BD_UPN=123353; BDUSS=UF0LWR5WVAxTjNMVDBtdUx2cWVGSjdKZUtuWWZCTlhUTVNvYXU1bHVUNGdzcTllRUFBQUFBJCQAAAAAAAAAAAEAAAD6Ea18AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAliF4gJYheV; BDRCVFR[n9IS1zhFc9f]=mk3SLVN4HKm; delPer=0; BD_CK_SAM=1; PSINO=7; BD_HOME=1; H_PS_PSSID=1442_31122_21081_30826_31186_30908_31055_30824_31086_31163_31195; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; sugstore=0; H_PS_645EC=efceiTIeoM3gAnADPHVUhY2TRqt8IUuoYiB6xm%2FMsr49hbJDmAV%2BHMv1bSY',
#     'Host': 'www.baidu.com',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'none',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
# }

# url = "https://www.baidu.com/s?wd=%E6%96%B9%E6%B3%95"

# res = requests.get(url, headers=headers)
# with open('bai.html', 'w') as f:
#     f.write(res.text)

# 爬取猫眼电影排行榜
import requests
import re
import json

def get_one_page(url):
    """
    param:一个url地址
    return：str类型的html文本
    """
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_one_page(html:str):
    """
    param:html  要解析的html文本
    return：正确的数据list
    """
    pattern = re.compile("")
    items = re.findall(pattern, html)
    print(items)

def write_file(content):
    """
    将文本内容写入文件
    param:content
    return:none
    """
    with open('result.txt', 'a', encoding='utf8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')

def main():
    # 要验证码了现在
    url = "http://maoyan.com/board/4"
    html = get_one_page(url)
    print(html)
    for item in parse_one_page(html):
        write_file(item)
