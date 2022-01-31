import requests
from bs4 import BeautifulSoup
from time import sleep
import re


class Reverso_translator:
    def __init__(self, meta, translations=5, examples=5, to_file=None):
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
        self.trs_tag = meta['translations_tag']
        self.trs_cls_regex = meta['translations_class_regex']
        self.exs_tag = meta['examples_tag']
        self.exs_id = meta['examples_id']
        self.ex_tag = meta['example_tag']
        self.ex_cl = meta['example_class']
        self.translations_end = translations
        self.examples_end = examples * 2
        self.to_file = to_file
        self.to_file_body = ''
        self.session = requests.Session()

    def get_welcome(self):
        print('Hello, you\'re welcome to the translator. Translator supports: ')
        for k, v in self.lang_dict.items():
            print(k + '.', v)

    def get_input(self):
        self.from_lang = self.lang_dict[input('Type the number of your language:')]
        to_lang = input(
            'Type the number of a language you want to translate to or \'0\' to translate to all languages:')
        if not to_lang == '0':
            self.to_lang = self.lang_dict[to_lang]
        else:
            self.to_lang = 'all'
            self.translations_end = 1
            self.examples_end = 2
        self.word = input('Type the word you want to translate:')

    def get_links(self):
        if not self.to_lang == 'all':
            self.translations_links.append(
                self.url + self.from_lang.lower() + '-' + self.to_lang.lower() + f'/{self.word}')
            self.translations_languages.append(self.to_lang)
        else:
            for _, to_lang in self.lang_dict.items():
                if not self.from_lang == to_lang:
                    self.translations_links.append(
                        self.url + self.from_lang.lower() + '-' + to_lang.lower() + f'/{self.word}')
                    self.translations_languages.append(to_lang)

    def get_soup(self):
        r = self.session.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        while not r.status_code == requests.codes.ok:
            sleep(1)
            r = self.session.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        self.soup = BeautifulSoup(r.content, 'html.parser')

    def get_translations(self):
        translations_list = [el.text.strip() for el in \
                             self.soup.find_all(self.trs_tag, class_=re.compile(self.trs_cls_regex))][
                            :self.translations_end]
        translations_heading = f'{self.to_lang} Translations:'
        translations_string = '\n'.join([translations_heading, *translations_list])
        self.print_out(translations_string, 'tr')
        if self.to_file:
            self.update_body(translations_string, 'tr')

    def get_examples(self):
        examples_list = [el.text.strip() for el in \
                         self.soup.find(self.exs_tag, id=self.exs_id).findAll(self.ex_tag, class_=self.ex_cl)][
                        :self.examples_end]
        i = 2
        while i < len(examples_list):
            examples_list.insert(i, '')
            i += 2 + 1

        examples_heading = f'{self.to_lang} Examples:'
        examples_string = '\n'.join([examples_heading, *examples_list])
        self.print_out(examples_string, 'ex')
        if self.to_file:
            self.update_body(examples_string, 'ex')

    def print_out(self, what, tr_ex):
        if tr_ex == 'tr':
            print(what + '\n')
        if tr_ex == 'ex':
            if not self.to_lang == self.translations_languages[-1]:
                print(what + '\n\n')
            else:
                print(what)

    def update_body(self, what, tr_ex):
        if tr_ex == 'tr':
            self.to_file_body += what + '\n\n'
        if tr_ex == 'ex':
            if not self.to_lang == self.translations_languages[-1]:
                self.to_file_body += what + '\n\n\n'
            else:
                self.to_file_body += what

    def save_txt(self):
        with open(f'{self.word}.txt', 'wb') as file:
            file.write(self.to_file_body.encode('UTF-8'))

    def main(self):
        self.get_welcome()
        self.get_input()
        self.get_links()
        print()
        for link, language in zip(self.translations_links, self.translations_languages):
            self.to_lang = language
            self.url = link
            self.get_soup()
            self.get_translations()
            self.get_examples()
        if self.to_file_body:
            self.save_txt()


known_ids = {
    'translations_tag': 'a',
    'translations_class_regex': 'translation.*ltr|rtl',
    'examples_tag': 'section',
    'examples_id': 'examples-content',
    'example_tag': 'span',
    'example_class': 'text'
}

my_translator = Reverso_translator(known_ids, translations=1, examples=1, to_file='pls')
my_translator.main()
