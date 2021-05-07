# -*- encoding:utf-8 -*-
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh.sorting import FieldFacet
from whoosh.query import *
import jieba
import json


class SearchDemo(tornado.web.RequestHandler):
    def post(self):
        # 跨域响应头
        self.set_header("Access-Control-Allow-Origin", "*")
        word = self.get_argument('word', '')
        print(f'word: {word}')

        # 查询输入框,暂时使用jieba分词 占位,检索条件处理
        # 检索条件分词,全模式
        condition_list = jieba.cut(word, cut_all=True)

        # 搜索引擎 占位,调用对方ES查询功能
        new_list = []
        # 读取建立好的索引
        index = open_dir("whoosh_index", indexname='indexname')

        with index.searcher() as searcher:
            # 创建查询条件or
            myquery = Or([Term("content", condition) for condition in condition_list])
            # 按序id排列搜索结果
            facet = FieldFacet("id", reverse=True)

            # limit 搜索结果条数的限制,默认为10
            results = searcher.search(myquery, limit=10, sortedby=facet)
            for result1 in results:
                new_list.append(dict(result1))

        # 反馈数据
        data = [text['content'] for text in new_list]
        self.write(json.dumps(data, ensure_ascii=False))


def make_app():
    return tornado.web.Application(
        [
            (r"/SearchDemo", SearchDemo),
        ])


if __name__ == "__main__":
    # 创建一个应用对象
    app = make_app()
    app.listen(8888)  # 设置端口
    tornado.ioloop.IOLoop.current().start()
