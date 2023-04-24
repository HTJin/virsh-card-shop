def wrap_letters(text, class_name):
    return "".join(f'<span class="{class_name}" data-letter="{letter}">{letter}</span>' for letter in text)

def wrap_words(text, class_name, letter_class_name, space_class_name):
    words = text.split()
    result = [
        f'<h1 class="{class_name}">'
        + "".join([f'<span class="{letter_class_name}" data-letter="{letter}">{letter}</span>' for letter in word])
        + (f'<span class="{space_class_name}">&nbsp;</span>' if i <
           len(words) - 1 else '')
        + '</h1>'
        for i, word in enumerate(words)
    ]
    return "".join(result)