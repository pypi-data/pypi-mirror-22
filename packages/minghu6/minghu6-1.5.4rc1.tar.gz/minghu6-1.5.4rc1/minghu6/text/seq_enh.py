# coding: utf-8

import re
# In[15]:
import sys

__all__ = ['self_input',
           'parseInts',
           'parseStr',
           'filter_invalid_char',
           'INVALID_FILE_CHAR_SET',
           'self_input_eh',
           'split',
           'split_whitespace']


def split_whitespace(src):
    src = src.strip()
    return re.split('\s+', src)


def split_blankline(src):
    src = src.strip()
    return re.split('\s+\n+', src)


def parseInts(Iteration):
    ints = [int(cell) for cell in Iteration]
    return ints


def parseStr(Iteration):
    ss = [item.strip() for item in Iteration]
    return ss


INVALID_FILE_CHAR_SET = {'\\', '/', ':', '*', '?', '"', '<', '>', '|', '%', '&'}


def filter_invalid_char(basefn, invalid_set=INVALID_FILE_CHAR_SET):
    return ''.join((list(filter(lambda x: x not in invalid_set, basefn))))


def self_input(prompt=''):
    '''Implement with BIF input()'''
    src = split_whitespace(input(prompt))
    while len(src[0]) == 0:
        # print('??')
        src = split_whitespace(input())

    return src


def self_input_eh(stream_in=sys.stdin, stream_out=sys.stdout, prompt=''):
    stream_out.write(prompt)
    src = split_whitespace(stream_in.readline())
    while len(src[0]) == 0:
        # print('??')
        src = split_whitespace(stream_in.readline())

    return src


def split(s, esc='\\', sep=' '):
    '''
    enhance the split func of str,
    support escape default '\' single-back-slash
    >>> split('www.abc.com\.a', sep='.')
    ['www', 'abc', 'com.a']
    '''
    l = []
    ss = []
    for c in s:
        if c == esc:
            l.append(c)
        else:
            [ss.append(esc) for i in range(len(l) // 2)]
            if c == sep:
                if len(l) % 2 != 0:  # is escaped char
                    ss.append(sep)
                else:
                    ss.append(' ')

                l.clear()

            else:
                ss.append(c)

    return ''.join(ss).split(' ')


if __name__ == '__main__':
    # src=self_input_eh(prompt='输入两个数\n')
    src = self_input_eh(open(
        'E:\Coding\Java\myscripts\MyselfPackage\Minghu6JavaClass\dist\README.TXT'))
    print(src)
