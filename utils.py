def text_to_binary(text):
    """ Преобразование текста в двоичный формат """
    return ''.join(format(ord(c), '08b') for c in text)