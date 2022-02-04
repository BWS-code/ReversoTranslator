import sys


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

supported_languages = {
    '0': 'All',
    '1': 'Arabic', '2': 'German', '3': 'English', '4': 'Spanish', '5': 'French',
    '6': 'Hebrew', '7': 'Japanese', '8': 'Dutch', '9': 'Polish', '10': 'Portuguese',
    '11': 'Romanian', '12': 'Russian', '13': 'Turkish'
}

arguments = sys.argv
terminal_entry = {
    'from_lang': arguments[1].capitalize() if len(arguments) == 4 else None if len(arguments) == 1 else '',
    'to_lang': arguments[2].capitalize() if len(arguments) == 4 else None if len(arguments) == 1 else '',
    'word': arguments[3] if len(arguments) == 4 else None if len(arguments) == 1 else ''
}

WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
