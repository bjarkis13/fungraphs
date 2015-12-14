import functools
import locale

def IS_sort():
    locale.setlocale(locale.LC_ALL, 'is_IS.UTF-8')
    return lambda x: functools.cmp_to_key(locale.strcoll)(x)
