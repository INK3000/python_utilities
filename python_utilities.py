def translit(text):
    '''
    Функция транслитерации с кирилицы в латиницу. Строчные и заглавные буквы сохраняют свое состояние.

    Пример:
    translit('Строка') вернет 'Stroka'

    Пример:
    l = ['С', 'т', 'р', 'о', 'к', 'а']
    translit(l) вернет 'Stroka'


    :param text: может быть строкой, списком или кортежем
    :return: независимо от типа принятой переменной возвращает строку, транслитерированную по словарю ru_lt_dict
    '''
    cy_lt_dict = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'jo',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'j',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'c',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sch',
        'ъ': '',
        'ы': 'y',
        'ь': '',
        'э': 'je',
        'ю': 'ju',
        'я': 'ja'
    }

    pre_result = list(text)
    for idx, char in enumerate(pre_result):
        char_is_upper = char.isupper()
        char = char.lower()
        if char in cy_lt_dict:
            pre_result[idx] = cy_lt_dict[char].upper() if char_is_upper else cy_lt_dict[char]
    result = ''.join(pre_result)
    return result
