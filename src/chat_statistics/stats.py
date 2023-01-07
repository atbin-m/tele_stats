import json
from pathlib import Path
from typing import Union

import arabic_reshaper
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from wordcloud import WordCloud

from src.data import DATA_DIR


class ChatStatistics:
    """ Generates word cloud from a Telegram chat json file 
    """
    def __init__(self, chat_json: Union[str, Path]):
        """ 
        :param chat_jason: path to Telegram export json file
        """
        logger.info(f'Loading data from {chat_json}')
        with open(chat_json) as f:
            self.chat_data = json.load(f)
        
        # load stopwords
        logger.info(f"Loading data from {DATA_DIR / 'stopwords.txt'}")
        self.normaliser = Normalizer()
        stop_words = open(DATA_DIR / 'stopwords.txt').readlines()
        stop_words = list(map(str.strip, stop_words))
        self.stop_words = list(map(self.normaliser.normalize, stop_words))

    def generate_word_cloud(
        self, 
        output_dir: Union[str, Path],
        width: int = 800, height: int = 800,
        max_font_size: int = 250,
    ):
        """ Generates a word cloud from a the chat data
        :param output_dir: path to output directory for word cloud image
        """
        logger.info('Loading text content...')
        text_content = ''

        for msg in self.chat_data['messages']:
            if type(msg['text']) == str:
                tokens = word_tokenize(msg['text'])
                tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                text_content += f" {' '.join(tokens)}"
                    
            elif type(msg['text']) == list:
                    for sub_msg in msg['text']:
                        if type(sub_msg) == str:
                            tokens = word_tokenize(sub_msg)
                            tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                            text_content += f" {' '.join(tokens)}"
                        elif type(sub_msg) == dict:
                            tokens = word_tokenize(sub_msg['text'])
                            tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                            text_content += f" {' '.join(tokens)}"
        
        # Normalise, reshape for final wordcloud
        text_content = self.normaliser.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        text_content = get_display(text_content)
        text_content = get_display(text_content)

        logger.info('Generating word cloud...')
        # generate word cloud 
        wordcloud = WordCloud(
            width=1200, height=1200,
            font_path=str(DATA_DIR / 'IRANSans.ttf'), 
            background_color='white',
            max_font_size=250,
        ).generate(text_content)

        logger.info('Saving word cloud')
        wordcloud.to_file(str(Path(output_dir) / 'wordcloud.png'))

if __name__ == '__main__':
    chat_stats = ChatStatistics(chat_json=str(DATA_DIR / 'PA_result.json'))
    chat_stats.generate_word_cloud(output_dir=str(DATA_DIR))
    print('Done!')


    # export PYTHONPATH=${PWD}