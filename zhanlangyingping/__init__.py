# /usr/bin/python
# encoding:utf-8
# __author__ = 'hang'

import re
import sys
import urllib2
import numpy
import jieba
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["figure.figsize"] = (10.0, 5.0)
from wordcloud import WordCloud
from bs4 import BeautifulSoup


class Enjoy:
    def __init__(self, url):
        self.url = url
        self.html_data = ""
        self.number = 0

    def enterweb(self):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        soup = BeautifulSoup(response.read(), features="html.parser")
        number = soup.find_all("li", class_="list-item")[0]["data-subject"]
        target_url = "https://movie.douban.com/subject/" + number + "/comments?start=0&limit=20"
        target_request = urllib2.Request(target_url)
        target_response = urllib2.urlopen(target_request).read()
        target_soup = BeautifulSoup(target_response, features="html.parser")
        comment_list = target_soup.find_all("div", class_="comment-item")

        each_comment = []
        for item in comment_list:
            if item.find_all("p")[0].string is not None:
                each_comment.append(item.find_all("p")[0].string)

        comments = ""
        for k in range(len(each_comment)):
            comments = comments + (str(each_comment[k])).strip()

        # 使用正则表达式去除标点符号
        # pattern = re.compile(r"^[\u4e00-\u9fa5]+")
        # filterdata = re.findall(pattern, comments)
        # cleaned_comments = ''.join(filterdata)
        comments = comments.decode("utf-8")
        cleaned_comments = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？：；《》“”、~@#￥%……&*（）]+".decode("utf8"),
                                  "".decode("utf8"),
                                  comments)
        segment = jieba.lcut(cleaned_comments)
        words_df = pd.DataFrame({'segment': segment})

        stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                                encoding='utf-8')  # quoting=3全不引用
        words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

        words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
        words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)

        wordcloud = WordCloud(font_path="heiti.ttf", background_color="white", max_font_size=80)  # 指定字体类型、字体大小和字体颜色
        word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
        # word_frequence_list = []
        # print word_frequence
        # for key in word_frequence:
        #     temp = (key, word_frequence[key])
        #     word_frequence_list.append(temp)

        wordcloud = wordcloud.fit_words(word_frequence)
        plt.imshow(wordcloud)
        plt.show()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")

    url = "https://movie.douban.com/cinema/nowplaying/changsha/"
    enjoy = Enjoy(url)
    enjoy.enterweb()
