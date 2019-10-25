from bs4 import BeautifulSoup
import re
import json
import requests

# url
index_url = "https://yp.120ask.com/search/0-0-{0}--0-0-0-0.html"
drug_url = "https://yp.120ask.com/detail/{0}.html"
total_drugs_count = 154219  # till 19/10/25

# CSS selector
selector_name = '.details-right-drug p'  # [0]
selector_price = '.Drugs-Price span'  # [0]
selector_diseases = '.details-right-drug ul li var'
selector_details_key = '.cont-Drug-details .tab-dm-1 .table .td'
selector_details_val = '.cont-Drug-details .tab-dm-1 .table .td-details'
selector_instructions_key = '.cont-Drug-details .tab-dm-2 .table .td'
selector_instructions_val = '.cont-Drug-details .tab-dm-2 .table .td-details'

# headers
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML\
        , like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}


def CrawlPage(id):
    data = requests.get(drug_url.format(id), headers=headers).text
    bs = BeautifulSoup(data, "lxml")
    return CreateItem(id, bs)


def CreateItem(id, bs):
    drug = {}
    drug['类型'] = '药品'
    drug['网址'] = 'https://yp.120ask.com/detail/{0}.html'.format(id)
    drug['名称'] = bs.select(selector_name)[0].get_text()
    drug['参考价'] = bs.select(selector_price)[0].get_text()
    drug['相关疾病'] = getDiseases(bs.select(selector_diseases))
    drug['药品详情'] = getDetails(bs.select(selector_details_key),
                              bs.select(selector_details_val))
    drug['药品说明书'] = getDetails(bs.select(selector_instructions_key),
                               bs.select(selector_instructions_val))
    return drug


def getDiseases(content):
    diseases = []
    for s in content:
        name = re.search('tagSearch\\(\'(.*?)\'\\)', str(s)).group(1)
        diseases.append({
            '名称': name,
            '网址': 'https://yp.120ask.com/search/?kw=' + name
        })
    return diseases


def getDetails(list_key, list_val):
    l1 = []
    l2 = []
    for i in list_key:
        l1.append(i.get_text())
    for i in list_val:
        l2.append(i.get_text())
    return dict(zip(l1, l2))


# TODO: save to file
def SaveJson(dict, path):
    pass


# Start
# TODO: traverse all pages using index
# TODO: save valid ids!!!
id = 1
save_data = []
save_data.append(CrawlPage(id))
print(save_data)
