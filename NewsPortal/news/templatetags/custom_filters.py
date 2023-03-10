from django import template

register = template.Library()

@register.filter()
def censor(text):
    words = ('дурак', 'идиот', 'редиска')
    words_list = ''

    try:
        if type(text) == str:
            words_list = text.split()
            for n in range(len(words_list)):
                word = words_list[n]
                for m in range(len(words)):
                    if word.lower().find(words[m]) == 0:
                        words_list[n] = word.replace(words[m][1:], ''.join(['*' for i in range(len(words[m][1:]))]))
        else:
            raise ValueError(f'"{text}" is not string!')
    except ValueError as e:
        print("Censor error: " + e)

    return ' '.join(words_list)
