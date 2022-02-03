import requests
from bs4 import BeautifulSoup
from time import sleep
from functools import reduce
import re


class Reverso_translator:
    def __init__(self, meta, translations=5, examples=5, examples_to_pairs=True, to_file=None):
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
    #     for i, lang in enumerate(('English', 'Russian')):
    #         languages.insert(i, languages.pop(languages.index(lang)))
    #     self.lang_dict = {str(i + 1): el for i, el in enumerate(languages)}

    def get_welcome(self):
        print('Hello, you\'re welcome to the translator. Translator supports: ')
        for k, v in self.lang_dict.items():
            print(k + '.', v)

    def get_input(self):
        self.from_lang = self.lang_dict[input('Type the number of your language:')]
        to_lang = input(
            'Type the number of language you want to translate to:')
        if not to_lang == '0':
            self.to_lang = self.lang_dict[to_lang]
        else:
            self.to_lang = 'all'
            self.translations = self.examples = 1
        self.word = input('Type the word you want to translate:')
        print()

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
        if self.translations:
            return [el.text.strip() for el in self.soup.find_all(
                self.trs_tag, class_=re.compile(self.trs_cls_regex))][:self.translations]
        return None

    def get_examples(self):
        if self.examples:
            examples = [el.text.strip() for el in self.soup.find(self.exs_tag, id=self.exs_id).findAll(
                self.ex_tag, class_=self.ex_cl)][:self.examples]
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
            self.update_results(translations, heading=f'Translation{"s"[:self.translations^1]}')
            self.update_results(examples, heading=f'Example{"s"[:self.examples^1]}')
        print(self.results_string)
        if self.to_file:
            self.save_txt()

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

my_translator = Reverso_translator(known_ids,
                                   translations=5, examples=5,
                                   examples_to_pairs=True,
                                   to_file='pls')
my_translator.main()
