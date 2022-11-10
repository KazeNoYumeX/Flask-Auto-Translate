import nltk
import multiprocessing
from Flask_Auto_Translate.config_loader import config
from Flask_Auto_Translate.schedule.ArticleContentTranslation import ArticleContentTranslation
from Flask_Auto_Translate.schedule.ArticleTitleTranslation import ArticleTitleTranslation
from Flask_Auto_Translate.schedule.PostTranslation import PostTranslation
from Flask_Auto_Translate.schedule.ThreadTranslation import ThreadTranslation

nltk.download("punkt")

translation_map = {
    "ArticleContent": ArticleContentTranslation,
    "ArticleTitle": ArticleTitleTranslation,
    "Post": PostTranslation,
    "Thread": ThreadTranslation,
}

url_map = {
    "ArticleContent": config['DEFAULT']['base_url'] + "content",
    "ArticleTitle": config['DEFAULT']['base_url'] + "title",
    "Post": config['DEFAULT']['base_url'] + "post",
    "Thread": config['DEFAULT']['base_url'] + "thread",
}


def trans_modes(i):
    modes = ['ArticleContent', 'ArticleTitle', 'Post', 'Thread']
    return modes[i]


def start(model):
    process = 4
    p_list = []

    for i in range(process):
        # Reset task status to idle
        translation_mode = translation_map[trans_modes(i)](model, {
            'interval': int(config['DEFAULT']['interval']),
            'url': url_map[trans_modes(i)],
            'count': int(config['DEFAULT']['count'])
        })

        p_list.append(multiprocessing.Process(target=translation_mode.start))
        p_list[i].start()

    for i in range(process):
        p_list[i].join()
