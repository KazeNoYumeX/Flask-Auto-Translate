import gc
import time
from html import escape

from Flask_Auto_Translate.schedule.TranslationBasic import get_data, make_line_table, translate, update_translated
from Flask_Auto_Translate.flask_auto_translate_logger import logger


def compile_content(code_list, content_map, translated_map):
    content = ''
    for code in code_list:
        if code in translated_map:
            hindi_html_encode = escape(translated_map[code]['hindi_text'])
            content += (hindi_html_encode + " ")
        else:
            content += content_map[code]
    return content


def translate_data(model, data):
    contents = []
    for article_content in data:
        code_list, content_map, translation_map = make_line_table(article_content['eng_content'])
        translated_content = compile_content(code_list, content_map, translate(model, translation_map))
        contents.append({'cid': article_content['cid'], 'content': translated_content, 'is_content_translated': 1})
    return contents


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
                            for content in translated:
                                logger.debug('cid: ' + str(content['cid']) + ' Save finished')
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


class ArticleContentTranslation:
    def __init__(self, model, config):
        self.model = model
        self.config = config

    def start(self):
        run(self.model, self.config)
