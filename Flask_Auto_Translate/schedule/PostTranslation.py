import gc
import time
from html import escape

from Flask_Auto_Translate.schedule.TranslationBasic import make_line_table, translate, update_translated, get_data
from Flask_Auto_Translate.flask_auto_translate_logger import logger


def compile_message(code_list, content_map, translated_message_map):
    message = ''
    for code in code_list:
        if code in translated_message_map:
            hindi_html_encode = escape(translated_message_map[code]['hindi_text'])
            message += (hindi_html_encode + " ")
        else:
            message += content_map[code]
    return message


def translate_data(model, data):
    posts = []
    for post in data:
        code_list, content_map, translation_map = make_line_table(post['eng_message'])
        translated_message = compile_message(code_list, content_map, translate(model, translation_map))
        posts.append({'pid': post['pid'], 'message': translated_message, 'is_message_translated': 1})
    return posts


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
                            for post in translated:
                                logger.debug('pid: ' + str(post['pid']) + ' Save finished')
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


class PostTranslation:
    def __init__(self, model, config):
        self.model = model
        self.config = config

    def start(self):
        logger.debug("Flask Auto Translate Mode: Post Start!")
        run(self.model, self.config)
