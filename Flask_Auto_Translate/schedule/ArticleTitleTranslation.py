import gc
import time

from Flask_Auto_Translate.schedule.TranslationBasic import get_data, translate, update_translated
from Flask_Auto_Translate.flask_auto_translate_logger import logger


def translate_data(model, data):
    # article_title_data map => translator text map form
    text_title_map = {}
    text_summary_map = {}
    for article_title in data:
        text_title_map[article_title['aid']] = {'eng_text': article_title['eng_title']}
        text_summary_map[article_title['aid']] = {'eng_text': article_title['eng_summary']}

    # call translator
    text_title = translate(model, text_title_map)
    summary_title = translate(model, text_summary_map)

    # translator text map form => article_title_data form
    translated = []
    for article_title in data:
        translated.append({'aid': article_title['aid'],
                           'title': text_title[article_title['aid']]['hindi_text'][:250],
                           'summary': summary_title[article_title['aid']]['hindi_text'][:250],
                           'is_title_translated': 1,
                           'is_summary_translated': 1})

    return translated


def run(model, config):
    while True:
        try:
            data = get_data(config['url'])
            while len(data):
                translated = data[-config['count']:]
                data = data[0:-config['count']]
                translated = translate_data(model, translated)
                if len(translated):
                    r = update_translated(config['url'], translated)
                    if r.status_code == 200:
                        status = r.json()['status']

                        if status == 200:
                            for title in translated:
                                logger.debug('aid: ' + str(title['aid']) + ' Save finished')
                        else:
                            logger.error(str(r.json()))

                # Sleep and clear cache
                del translated
                gc.collect()
                time.sleep(3)
            else:
                logger.debug('No data, sleep %s seconds' % config['interval'])

            del data
            gc.collect()
            time.sleep(config['interval'])
        except Exception as e:
            logger.error(e)
            break


class ArticleTitleTranslation:
    def __init__(self, model, config):
        self.model = model
        self.config = config

    def start(self):
        run(self.model, self.config)
