import hashlib
import json
import re

import dl_translate as dlt
import nltk
import requests


def translate(mt, text):
    for code in text:
        text[code]['hindi_text'] = mt.translate(text[code]['eng_text'], source=dlt.lang.ENGLISH,
                                                target=dlt.lang.HINDI)

        # If you want to see the translation process
        # print(text[code]['eng_text'], "=>", text[code]['hindi_text'])
    return text


def is_special_string(special_string_regex, t):
    return re.search(special_string_regex, t)


def md5hash(text):
    m = hashlib.md5()
    m.update(text.encode("utf-8"))
    md5 = m.hexdigest()
    return md5


def split_html_content(special_string_regex, html_content):
    subst = "※\\1\\2\\3\\4\\5\\6※"
    result = re.sub(special_string_regex, subst, html_content, 0, re.MULTILINE)
    t_list = result.split('※')
    return t_list


def is_blank_string(t):
    return len(t.strip()) == 0


def make_line_table(html_content):
    special_string_regex = r"(<[^<]+>)|(\[attach]\d+\[\/attach])|((http|https):\/\/[^\s]+)|(\[a[^]]+])|(\[\/[^]]+])"
    t_list = split_html_content(special_string_regex, html_content)
    code_list = []
    content_map = {}
    translation_map = {}

    for t in t_list:
        if t == '':
            continue
        elif is_special_string(special_string_regex, t) or is_blank_string(t):
            md5 = md5hash(t)
            code_list.append(md5)
            content_map[md5] = t
        else:
            # normal sentence 正常句子
            # 分解段落成句子，然後要加入翻譯的袋子裡
            sets = nltk.tokenize.sent_tokenize(t, "english")
            for s in sets:
                s_md5 = md5hash(s)
                code_list.append(s_md5)
                content_map[s_md5] = s
                translation_map[s_md5] = {'eng_text': s}

    return code_list, content_map, translation_map


def get_data(url):
    return requests.get(url).json()


def update_translated(url, data):
    return requests.put(url, headers={'Content-Type': 'application/json'},
                        data=json.dumps({"data": data}))
