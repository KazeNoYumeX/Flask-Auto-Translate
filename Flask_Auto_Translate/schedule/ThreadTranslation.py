import gc
import time

from Flask_Auto_Translate.schedule.TranslationBasic import translate, update_translated, get_data
from Flask_Auto_Translate.flask_auto_translate_logger import logger


def translate_data(model, data):
    # thread_data map => translator text map form
    text_map = {}
    for thread_data in data:
        text_map[thread_data['tid']] = {'eng_text': thread_data['eng_subject']}

    # call translator
    translation_map = translate(model, text_map)

    # translator text map form => thread_data form
    threads = []
    for thread in data:
        threads.append(
            # Because the limit of discuz is to take only 250 chars
            {'tid': thread['tid'], 'subject': translation_map[thread['tid']]['hindi_text'][:250],
             'is_subject_translated': 1})

    return threads


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
                            for thread in translated:
                                logger.debug('tid: ' + str(thread['tid']) + ' Save finished')
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


class ThreadTranslation:
    def __init__(self, model, config):
        self.model = model
        self.config = config

    def start(self):
        logger.debug("Flask Auto Translate Mode: Thread Start!")
        run(self.model, self.config)
