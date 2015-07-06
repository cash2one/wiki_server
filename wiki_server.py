#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json
import sys
import logging
import os

filename = 'abstract.dat'
logger = logging.getLogger()


def init_logger():
    global logger

    log_dir = "log"
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)

    fmt = '%(levelname)s %(asctime)s %(filename)s|%(lineno)d %(message)s'
    formatter = logging.Formatter(fmt)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("{}/wiki.log".format(log_dir))
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

class WikiAbstract(tornado.web.RequestHandler):
    '''WikiAbstract CLass

    A class for URI wikiabs.

    Attributes:
        abstracts_pron: All the abstracts extracted from wikipedia.org.
        abstracts_word: All the abstracts extracted from wikipedia.org.
        invalid_ret: An invalid return json.
    '''

    abstracts_pron = {}
    abstracts_word = {}
    invalid_ret = json.dumps({
        'errno': 1,  # errno equals to 1 means INVALID PARAMS
        'reason': 'invalid params',
    })
    with open(filename) as f:
        for line in f:
            line = line.strip()
            try:
                pron, word, abstract, url = line.split("\t")
                '''
                abstracts_pron[pron.decode("utf-8")] = json.dumps({
                    'errno': 0,  # errno equals to 0 means OK.
                    'word': word,
                    'abstract': abstract,
                    'url': url,
                })
                '''
                abstracts_word[word.decode("utf-8")] = json.dumps({
                    'errno': 0,
                    'pron': pron,
                    'abstract': abstract,
                    'url': url,
                })
            except:
                continue
    logger.info("Data loaded! Ready to serve.")

    def get(self):
        '''Get the wiki abstract of given pronunciation or word.

        Args:
            pron: A given pronunciation.
            word: A given word.
        '''
        pron = self.get_argument("pron", None)
        word = self.get_argument("word", None)
        log_data = json.dumps({'pron': pron, 'word': word})
        #logger.info(log_data)

        # one of pronunciation and word is required.
        if pron is None and word is None:
            self.write(self.invalid_ret)
            logger.error("invalid_params {}".format(log_data))
            return

        # the priority of word is higher than pronunciation.
        ret_json = None
        if word is not None:
            ret_json = self.__class__.abstracts_word.get(word,
                self.__class__.invalid_ret)
        else:
            ret_json = self.__class__.invalid_ret
        '''
        else:
            ret_json = self.__class__.abstracts_pron.get(pron,
                self.__class__.invalid_ret)
        '''

        self.write(ret_json)

    def post(self):
        '''POST method is invalid.
        We not support this method.
        '''
        self.write(self.__class__.invalid_ret)

# URI list
application = tornado.web.Application([
    (r'/wiki', WikiAbstract),
])
# port of this server
port = 8084


if __name__ == '__main__':
    init_logger()

    server = tornado.httpserver.HTTPServer(application)
    server.bind(port)
    server.start(0)
    tornado.ioloop.IOLoop.instance().start()
