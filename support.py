import sys


known_ids = {
    'translations_tag': 'a',
    'translations_class_regex': 'translation.*ltr|rtl',
    'examples_tag': 'section',
    'examples_id': 'examples-content',
    'example_tag': 'span',
    'example_class': 'text'
}
arguments = sys.argv
supported_languages = {
    '0': 'all',
    '1': 'arabic', '2': 'german',
    '3': 'english', '4': 'spanish',
    '5': 'french', '6': 'hebrew',
    '7': 'japanese', '8': 'dutch',
    '9': 'polish', '10': 'portuguese',
    '11': 'romanian', '12': 'russian',
    '13': 'turkish', '14': 'chinese'
}
user_data = {'from_lang': arguments[1] if len(arguments) == 4 else None if len(arguments) == 1 else '',
             'to_lang': arguments[2] if len(arguments) == 4 else None if len(arguments) == 1 else '',
             'word': arguments[3] if len(arguments) == 4 else None if len(arguments) == 1 else ''}
