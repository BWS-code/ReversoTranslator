import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import sys


class Reverso_translator:
    def __init__(self, inp, meta, languages, translations=5, examples=5, to_file=None):
        self.soup = None
        self.url = 'https://context.reverso.net/translation/'
        self.from_lang = inp['from_lang']
        self.to_lang = inp['to_lang']
        self.word = inp['word']
        self.translations_links = []
        self.translations_languages = []
        self.lang_dict = languages
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
            print(k + '.', v.capitalize())

    def get_input(self):
        self.from_lang = self.lang_dict[input('Type the number of your language:')]
        self.to_lang = self.lang_dict[\
            input('Type the number of a language you want to translate to or \'0\' to translate to all languages:')]
        self.word = input('Type the word you want to translate:')

    def get_links(self):
        if not self.to_lang == 'all':
            self.translations_links.append(
                self.url + self.from_lang + '-' + self.to_lang + f'/{self.word}')
            self.translations_languages.append(self.to_lang)
        else:
            for _, to_lang in self.lang_dict.items():
                if not to_lang == 'all' and not self.from_lang == to_lang:
                    self.translations_links.append(
                        self.url + self.from_lang + '-' + to_lang + f'/{self.word}')
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
        translations_heading = f'{self.to_lang.capitalize()} Translations:'
        translations_string = '\n'.join([translations_heading, *translations_list])
        self.print_out(translations_string, 'tr')
        if self.to_file:
            self.update_body(translations_string, 'tr')

    def get_examples(self):
        examples_list = [el.text.strip() for el in \
                         self.soup.find(self.exs_tag, id=self.exs_id).findAll(self.ex_tag, class_=self.ex_cl)][:self.examples_end]
        i = 2
        while i < len(examples_list):
            examples_list.insert(i, '')
            i += 2 + 1

        examples_heading = f'{self.to_lang.capitalize()} Examples:'
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
        if self.word is None:
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


def terminal_error():
    print('<!!> wrong call or language\nExpected >python file.py from_language to_language which_word')
    print('Supported >', ', '.join(language for _, language in languages.items()))


known_ids = {
    'translations_tag': 'a',
    'translations_class_regex': 'translation.*ltr|rtl',
    'examples_tag': 'section',
    'examples_id': 'examples-content',
    'example_tag': 'span',
    'example_class': 'text'
}
arguments = sys.argv
user_data = {'from_lang': arguments[1] if len(arguments) == 4 else None if len(arguments) == 1 else '',
             'to_lang': arguments[2] if len(arguments) == 4 else None if len(arguments) == 1 else '',
             'word': arguments[3] if len(arguments) == 4 else None if len(arguments) == 1 else ''
             }
supported_languages = {
    '0': 'all',
    '1': 'arabic',
    '2': 'german',
    '3': 'english',
    '4': 'spanish',
    '5': 'french',
    '6': 'hebrew',
    '7': 'japanese',
    '8': 'dutch',
    '9': 'polish',
    '10': 'portuguese',
    '11': 'romanian',
    '12': 'russian',
    '13': 'turkish',
    '14': 'chinese'
}

if not len(arguments) in (1, 4):
    terminal_error()
elif len(arguments) > 2:
    if not arguments[1] in supported_languages.values() or not arguments[2] in supported_languages.values():
        terminal_error()
    else:
        my_translator = Reverso_translator(user_data, known_ids, supported_languages, translations=1, examples=1, to_file='pls')
        my_translator.main()
