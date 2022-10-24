import nltk

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


def start(model):
    # Reset task status to idle
    translation_mode = translation_map[config['DEFAULT']["mode"]](model, {
        'interval': int(config['DEFAULT']['interval']),
        'url': url_map[config['DEFAULT']['mode']],
        'count': int(config['DEFAULT']['count'])
    })
    translation_mode.start()
