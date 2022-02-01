import requests
from bs4 import BeautifulSoup
from time import sleep
import re
from functools import reduce


class Reverso_translator:
    def __init__(self, meta, translations=5, examples=5):
        self.soup = None
        self.url = 'https://context.reverso.net/translation/'
        self.to_lang = self.from_lang = self.word = None
        self.translations_links = []
        self.translations_languages = []
        self.lang_dict = {
            '1': 'Arabic',
            '2': 'German',
            '3': 'English',
            '4': 'Spanish',
            '5': 'French',
            '6': 'Hebrew',
            '7': 'Japanese',
            '8': 'Dutch',
            '9': 'Polish',
            '10': 'Portuguese',
            '11': 'Romanian',
            '12': 'Russian',
            '13': 'Turkish'
        }
        # self.lang_dict = None
        # self.lang_tag = meta['languages_tag']
        # self.lang_tag_attr = meta['languages_tag_attr']
        # self.lang_tag_attr_len = meta['languages_tag_attr_len']
        self.trs_tag = meta['translations_tag']
        self.trs_cls_regex = meta['translations_class_regex']
        self.exs_tag = meta['examples_tag']
        self.exs_id = meta['examples_id']
        self.ex_tag = meta['example_tag']
        self.ex_cl = meta['example_class']
        self.translations = translations
        self.examples = examples * 2
        self.session = requests.Session()

    # def get_languages(self):
    #     self.get_soup()
    #     languages = list(set([el.text.strip() for el in self.soup.find_all(
    #         lambda tag: tag.name == self.lang_tag and \
    #                     tag.get(self.lang_tag_attr) and \
    #                     len(tag.get(self.lang_tag_attr)) == self.lang_tag_attr_len)]))
    #     for i, lang in enumerate(('English', 'Russian')):
    #         languages.insert(i, languages.pop(languages.index(lang)))
    #     self.lang_dict = {str(i + 1): el for i, el in enumerate(languages)}

    def get_welcome(self):
        print('Hello, you\'re welcome to the translator. Translator supports: ')
        print(self.lang_dict)
        for k, v in self.lang_dict.items():
            print(k + '.', v)

    def get_input(self):
        self.from_lang = self.lang_dict[input('Type the number of your language:')]
        to_lang = input(
            'Type the number of language you want to translate to:')
        self.to_lang = self.lang_dict[to_lang]
        self.word = input('Type the word you want to translate:')

    def get_links(self):
        self.translations_links.append(self.url + self.from_lang.lower() + '-' + self.to_lang.lower() + f'/{self.word}')
        self.translations_languages.append(self.to_lang)

    def get_soup(self):
        r = self.session.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        while not r.status_code == requests.codes.ok:
            sleep(1)
            r = self.session.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        self.soup = BeautifulSoup(r.content, 'html.parser')

    def get_translations(self):
        return [el.text.strip() for el in self.soup.find_all(
            self.trs_tag, class_=re.compile(self.trs_cls_regex))][:self.translations]

    def get_examples(self):
        if self.examples:
            return [el.text.strip() for el in self.soup.find(self.exs_tag, id=self.exs_id).findAll(
                self.ex_tag, class_=self.ex_cl)][:self.examples]
        return None

    def display(self, what, heading):
        if what and heading == 'Examples':
            what = reduce(lambda x, y: x + y, [[el, ''] if i % 2 and i != len(what) - 1
                                               else [el] for i, el in enumerate(what)])
        if what:
            print('\n'.join(['', f'{self.to_lang} {heading}:', *what]))

    def main(self):
        # self.get_languages()
        self.get_welcome()
        self.get_input()
        self.get_links()
        for link, language in zip(self.translations_links, self.translations_languages):
            self.to_lang = language
            self.url = link
            self.get_soup()
            translations = self.get_translations()
            examples = self.get_examples()
            self.display(translations, heading='Translations')
            self.display(examples, heading='Examples')


known_ids = {
    # 'languages_tag': 'span',
    # 'languages_tag_attr': 'data-value',
    # 'languages_tag_attr_len': 2,
    'translations_tag': 'a',
    'translations_class_regex': 'translation.*ltr|rtl',
    'examples_tag': 'section',
    'examples_id': 'examples-content',
    'example_tag': 'span',
    'example_class': 'text'
}

my_translator = Reverso_translator(known_ids, translations=5, examples=5)
my_translator.main()
