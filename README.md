# yp-120ask-spider

## 简介

这是一个采集 [快速问医生](http://120ask.com) 网站中 [药品库](https://yp.120ask.com) 信息的爬虫。

为 2019 Web信息处理 课程开放实验项目之一。

## 相关信息

+   Author: Censyu
+   Start Date: 2019/10/25
+   Deadline: 2019/11/9

## 实验要求

:arrow_right: [原地址](https://git.bdaa.pro/yxonic/data-specification/wikis/快速问医生%20药品)

###  网站描述

[快速问医生](http://tag.120ask.com)是一个医疗信息百科网站，主要有疾病、症状、检查、手术、药品五类信息。通过网站右上角的资料卡片，可以进入每类信息的专题页面。本实验的目标是采集[药品库](http://yp.120ask.com/)的数据。 

###  药品需求 

可直接利用网址构成遍历

http://yp.120ask.com/detail/ + 数字 +.html

对于某个药品的页面，我们需要以下信息：

药品名称、参考价、相关疾病、药品详情、药品说明书

###  药品数据格式

```json
[
    {
        类型: "药品",
        网址: "http://xxx..."
        名称: "xx",
        参考价: "",
        相关疾病: [
        	{名称: "aaa", 网址: ""},
        	{名称: "bbb", 网址: ""},
        	...
        ],
		药品详情: {
            商品名称: "",
            ...
            生产企业: ""
        },
        药品说明书: {
            商品名称: "",
            ...
            贮藏: ""
        }
    }
]
```

###  评分标准 

+   采集到100个页面的全部域：1分

+   采集到网站全部页面：2分

## 设计过程

### 网站分析

在药品库页面显示了该网站共有 154219 种药品（till 19/10/25）。

并且搜索页面提供了 20*100 共 2000 个药品详情的链接，这远小于所有药品数，因此需要遍历以获取全部内容。此外注意到最后一页最后一个药品的 id 为 5375，显然 id 并不是连续的，中间存在大量空隙。

### 数据分析

查看网页源码，找到所需信息位置，并写出相应的 CSS 选择器（使用 BeautifulSoup4 进行解析）：

```python
selector_name = '.details-right-drug p'  # [0]
selector_price = '.Drugs-Price span'   # [0]
selector_diseases = '.details-right-drug ul li var'
selector_details = '.cont-Drug-details .tab-dm-1 table'  # .tablerow(.td, .td-details)
selector_instructions = '.cont-Drug-details .tab-dm-2 table'
```

其中名称和参考价直接获取文本即可。相关疾病、药品详情和说明书有子结构，需要进一步解析，见代码中函数 `getDiseases()` `getDetails()`

对于相关疾病：

疾病名在 `var` 标签的 onclick 属性中函数调用参数里，直接用正则表达式提取即可

` tagSearch() ` 函数，查看该元素的 onclick 事件可以找到这个函数的实现：

```js
// 疾病词
function tagSearch(kw){
    window.open("//yp.120ask.com/search?kw="+kw);
}
```

从而找到疾病跳转网址（但事实上这段代码写错了...应该在 `?` 前加一个 `/`）

### 反爬机制

这个网站的反爬机制很简单，只用设置 User-Agent 即可直接获取内容