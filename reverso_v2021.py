import requests
from bs4 import BeautifulSoup
from time import sleep
from functools import reduce
import re
from support import *


class Reverso_translator:
    def __init__(self, terminal_inp, meta, languages,
                 translations=5, examples=5, examples_to_pairs=True,
                 to_file=None):
        self.url = 'https://context.reverso.net/translation/'
        self.from_lang, self.to_lang = terminal_inp['from_lang'], terminal_inp['to_lang']
        self.word = terminal_inp['word']
        self.translations_links = []
        self.translations_languages = []
        self.lang_dict = languages
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
        self.examples = examples
        self.examples_to_pairs = examples_to_pairs
        self.to_file = to_file
        self.results_string = ''
        self.session = requests.Session()
        self.soup = None

    # def get_languages(self):
    #     self.get_soup()
    #     languages = list(set([el.text.strip() for el in self.soup.find_all(
    #         lambda tag: tag.name == self.lang_tag and \
    #                     tag.get(self.lang_tag_attr) and \
    #                     len(tag.get(self.lang_tag_attr)) == self.lang_tag_attr_len)]))
    #     languages.sort()
    #     for i, lang in enumerate(('English', 'Russian')):
    #         languages.insert(i, languages.pop(languages.index(lang)))
    #     self.lang_dict = {'0': 'All'} | {str(i + 1): el for i, el in enumerate(languages)}

    def get_welcome(self):
        print('Hello, you\'re welcome to the translator. Translator supports: ')
        for k, v in self.lang_dict.items():
            print(k + '.', v)

    def get_input(self):
        self.from_lang = self.lang_dict[input('Type the number of your language:')]
        to_lang = input('Type the number of language you want to translate to:')
        self.to_lang = self.lang_dict[to_lang]
        self.word = input('Type the word you want to translate:')
        print()

    def get_links(self):
        if not self.to_lang == 'All':
            self.translations_links.append(
                self.url + self.from_lang.lower() + '-' + self.to_lang.lower() + f'/{self.word}')
            self.translations_languages.append(self.to_lang)
        else:
            self.translations = self.examples = 1
            for _, to_lang in self.lang_dict.items():
                if not to_lang == 'All' and not self.from_lang == to_lang:
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
        if self.translations:
            return [el.text.strip() for el in self.soup.find_all(
                self.trs_tag, class_=re.compile(self.trs_cls_regex))][:self.translations]
        return None

    def get_examples(self):
        if self.examples:
            examples = [el.text.strip() for el in self.soup.find(self.exs_tag, id=self.exs_id).findAll(
                self.ex_tag, class_=self.ex_cl)][:self.examples * 2]
            if self.examples_to_pairs:
                paired_examples = reduce(lambda x, y: x + y, [[el, ''] if i % 2 and i != len(examples) - 1
                                                              else [el] for i, el in enumerate(examples)])
                return paired_examples
            return examples
        return None

    def update_results(self, result_list, heading):
        if result_list:
            spacer = self.get_spacer(heading)
            result_string = '\n'.join([*spacer, f'{self.to_lang} {heading}:', *result_list])
            self.results_string += result_string

    def get_spacer(self, heading):
        if self.to_lang == self.translations_languages[0] and heading.startswith('Tr'):
            n = 0
        elif len(self.translations_languages) > 1:
            n = 3 if heading.startswith('Tr') else 2
        else:
            n = 2 if heading.startswith('Ex') else 1
        return [''] * n if n else ''

    def save_txt(self):
        with open(f'{self.word}.txt', 'wb') as file:
            file.write(self.results_string.encode('UTF-8'))

    def run(self):
        # self.get_languages()
        if self.word is None:
            self.get_welcome()
            self.get_input()
        self.get_links()
        for link, language in zip(self.translations_links, self.translations_languages):
            self.to_lang = language
            self.url = link
            self.get_soup()
            translations = self.get_translations()
            examples = self.get_examples()
            self.update_results(translations, heading=f'Translation{"s"[:self.translations ^ 1]}')
            self.update_results(examples, heading=f'Example{"s"[:self.examples ^ 1]}')
        print(self.results_string)
        if self.to_file:
            self.save_txt()

def terminal_error():
    print(f'{FAIL}<!!FAILED> wrong call or language\nExpected >python file.py from_language to_language which_word{ENDC}')
    print(f'Supported >', ', '.join(language.lower() for _, language in supported_languages.items()))


def create_and_run():
    my_translator = Reverso_translator(terminal_entry, known_ids, supported_languages,
                                       translations=5, examples=5,
                                       examples_to_pairs=True,
                                       to_file='pls')
    my_translator.run()

def main():
    if not len(arguments) in (1, 4):
        terminal_error()
    elif len(arguments) > 2:
        if not terminal_entry['from_lang'] in supported_languages.values() or \
                not terminal_entry['to_lang'] in supported_languages.values():
            terminal_error()
        else:
            create_and_run()
    else:
        create_and_run()

main()
