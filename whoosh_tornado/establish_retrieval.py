# -*- encoding:utf-8 -*-
# -*- coding: utf-8 -*-
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from whoosh.sorting import FieldFacet
from whoosh.query import *
import xlrd

# 打开文件,获取创建查询的文本数据
workbook = xlrd.open_workbook(r'入院记录_全文检索 .xls')
# 获取sheet0,第7列内容
cols_text = workbook.sheet_by_index(0).col_values(6)[1:]


'''
    建立索引
'''
# 导入中文分词工具
analyser = ChineseAnalyzer()
# 创建索引结构
# schema = Schema(phone_name=TEXT(stored=True, analyzer=analyser), price=NUMERIC(stored=True),
#                 phoneid=ID(stored=True))
schema = Schema(content=TEXT(stored=True, analyzer=analyser), id=ID(stored=True))

# 索引创建的地址 schema:索引结构 indexname:索引名称
ix = create_in("whoosh_index", schema=schema, indexname='indexname')
writer = ix.writer()

# 添加内容
for index in range(len(cols_text)):
    writer.add_document(content=cols_text[index], id=str(index+1))
print("建立完成索引")
writer.commit()

'''
    搜索引擎
'''
new_list = []
# 读取建立好的索引
index = open_dir("whoosh_index", indexname='indexname')
with index.searcher() as searcher:
    # 要搜索的项目
    parser = QueryParser("content", index.schema)
    # myquery = parser.parse("精神尚可,体重减少")
    myquery = Or([Term("content", "精神"), Term("content", "体重")])
    print(myquery,type(myquery))
    # 按序id排列搜索结果
    facet = FieldFacet("id", reverse=True)
    # limit为搜索结果的限制,默认为10
    results = searcher.search(myquery, limit=10, sortedby=facet)
    for result1 in results:
        print(dict(result1))
        new_list.append(dict(result1))
