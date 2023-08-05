#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re

from enum import IntEnum, unique

from pypinyin import phonetic_symbol, pinyin_dict
from pypinyin.compat import SUPPORT_UCS4

# 词语拼音库
if os.environ.get('PYPINYIN_NO_PHRASES'):
    PHRASES_DICT = {}
else:
    from pypinyin import phrases_dict
    PHRASES_DICT = phrases_dict.phrases_dict.copy()

# 单字拼音库
PINYIN_DICT = pinyin_dict.pinyin_dict.copy()
# 声母表
_INITIALS = 'b,p,m,f,d,t,n,l,g,k,h,j,q,x,zh,ch,sh,r,z,c,s'.split(',')
# 声母表, 把 y, w 也当作声母
_INITIALS_NOT_STRICT = _INITIALS + ['y', 'w']
# 带声调字符与使用数字标识的字符的对应关系，类似： {u'ā': 'a1'}
PHONETIC_SYMBOL = phonetic_symbol.phonetic_symbol.copy()
# 所有的带声调字符
re_phonetic_symbol_source = ''.join(PHONETIC_SYMBOL.keys())
# 匹配带声调字符的正则表达式
RE_PHONETIC_SYMBOL = r'[' + re.escape(re_phonetic_symbol_source) + r']'
# 匹配使用数字标识声调的字符的正则表达式
RE_TONE2 = r'([aeoiuvnm])([1-4])$'
# 匹配 TONE2 中标识韵母声调的正则表达式
RE_TONE3 = re.compile('^([a-z]+)([1-4])([a-z]*)$')
# 有拼音的汉字
if SUPPORT_UCS4:
    RE_HANS = re.compile(
        r'^(?:['
        r'\u3400-\u4dbf'           # CJK扩展A:[3400-4DBF]
        r'\u4e00-\u9fff'           # CJK基本:[4E00-9FFF]
        r'\uf900-\ufaff'           # CJK兼容:[F900-FAFF]
        r'\U00020000-\U0002A6DF'   # CJK扩展B:[20000-2A6DF]
        r'\U0002A703-\U0002B73F'   # CJK扩展C:[2A700-2B73F]
        r'\U0002B740-\U0002B81D'   # CJK扩展D:[2B740-2B81D]
        r'\U0002F80A-\U0002FA1F'   # CJK兼容扩展:[2F800-2FA1F]
        r'])+$'
    )
else:
    RE_HANS = re.compile(
        r'^(?:['
        r'\u3400-\u4dbf'           # CJK扩展A:[3400-4DBF]
        r'\u4e00-\u9fff'           # CJK基本:[4E00-9FFF]
        r'\uf900-\ufaff'           # CJK兼容:[F900-FAFF]
        r'])+$'
    )


@unique
class Style(IntEnum):
    """拼音风格"""

    #: 普通风格，不带声调。如： 中国 -> ``zhong guo``
    NORMAL = 0
    #: 标准声调风格，拼音声调在韵母第一个字母上（默认风格）。如： 中国 -> ``zhōng guó``
    TONE = 1
    #: 声调风格2，即拼音声调在各个韵母之后，用数字 [1-4] 进行表示。如： 中国 -> ``zho1ng guo2``
    TONE2 = 2
    #: 声调风格3，即拼音声调在各个拼音之后，用数字 [1-4] 进行表示。如： 中国 -> ``zhong1 guo2``
    TONE3 = 8
    #: 声母风格，只返回各个拼音的声母部分（注：有的拼音没有声母，详见 `#27`_）。如： 中国 -> ``zh g``
    INITIALS = 3
    #: 首字母风格，只返回拼音的首字母部分。如： 中国 -> ``z g``
    FIRST_LETTER = 4
    #: 韵母风格，只返回各个拼音的韵母部分，不带声调。如： 中国 -> ``ong uo``
    FINALS = 5
    #: 标准韵母风格，带声调，声调在韵母第一个字母上。如：中国 -> ``ōng uó``
    FINALS_TONE = 6
    #: 韵母风格2，带声调，声调在各个韵母之后，用数字 [1-4] 进行表示。如： 中国 -> ``o1ng uo2``
    FINALS_TONE2 = 7
    #: 韵母风格3，带声调，声调在各个拼音之后，用数字 [1-4] 进行表示。如： 中国 -> ``ong1 uo2``
    FINALS_TONE3 = 9
    #: 注音风格，带声调，阴平（第一声）不标。如： 中国 -> ``ㄓㄨㄥ ㄍㄨㄛˊ``
    BOPOMOFO = 10
    #: 注音风格，仅首字母。如： 中国 -> ``ㄓ ㄍ``
    BOPOMOFO_FIRST = 11
    #: 汉语拼音与俄语字母对照风格，声调在各个拼音之后，用数字 [1-4] 进行表示。如： 中国 -> ``чжун1 го2``
    CYRILLIC = 12
    #: 汉语拼音与俄语字母对照风格，仅首字母。如： 中国 -> ``ч г``
    CYRILLIC_FIRST = 13


NORMAL = STYLE_NORMAL = Style.NORMAL
TONE = STYLE_TONE = Style.TONE
TONE2 = STYLE_TONE2 = Style.TONE2
TONE3 = STYLE_TONE3 = Style.TONE3
INITIALS = STYLE_INITIALS = Style.INITIALS
FIRST_LETTER = STYLE_FIRST_LETTER = Style.FIRST_LETTER
FINALS = STYLE_FINALS = Style.FINALS
FINALS_TONE = STYLE_FINALS_TONE = Style.FINALS_TONE
FINALS_TONE2 = STYLE_FINALS_TONE2 = Style.FINALS_TONE2
FINALS_TONE3 = STYLE_FINALS_TONE3 = Style.FINALS_TONE3
BOPOMOFO = STYLE_BOPOMOFO = Style.BOPOMOFO
BOPOMOFO_FIRST = STYLE_BOPOMOFO_FIRST = Style.BOPOMOFO_FIRST
CYRILLIC = STYLE_CYRILLIC = Style.CYRILLIC
CYRILLIC_FIRST = STYLE_CYRILLIC_FIRST = Style.CYRILLIC_FIRST

# 注音转换表
BOPOMOFO_REPLACE = (
    (re.compile('^m(\d)$'), 'mu\\1'),  # 呣
    (re.compile('^n(\d)$'), 'N\\1'),  # 嗯
    (re.compile('^r5$'), 'er5'),  # 〜兒
    (re.compile('iu'), 'iou'),
    (re.compile('ui'), 'uei'),
    (re.compile('ong'), 'ung'),
    (re.compile('^yi?'), 'i'),
    (re.compile('^wu?'), 'u'),
    (re.compile('iu'), 'v'),
    (re.compile('^([jqx])u'), '\\1v'),
    (re.compile('([iuv])n'), '\\1en'),
    (re.compile('^zhi?'), 'Z'),
    (re.compile('^chi?'), 'C'),
    (re.compile('^shi?'), 'S'),
    (re.compile('^([zcsr])i'), '\\1'),
    (re.compile('ai'), 'A'),
    (re.compile('ei'), 'I'),
    (re.compile('ao'), 'O'),
    (re.compile('ou'), 'U'),
    (re.compile('ang'), 'K'),
    (re.compile('eng'), 'G'),
    (re.compile('an'), 'M'),
    (re.compile('en'), 'N'),
    (re.compile('er'), 'R'),
    (re.compile('eh'), 'E'),
    (re.compile('([iv])e'), '\\1E'),
    (re.compile('([^0-4])$'), '\\g<1>0'),
    (re.compile('1$'), ''),
)
BOPOMOFO_TABLE = dict(zip(
    'bpmfdtnlgkhjqxZCSrzcsiuvaoeEAIOUMNKGR2340',
    'ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙㄧㄨㄩㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦˊˇˋ˙'
))

# 俄语转换表
CYRILLIC_REPLACE = (
    (re.compile('ong'), 'ung'),
    (re.compile('([zcs])i'), '\\1U'),
    (re.compile('([xqj])u'), '\\1v'),
    (re.compile('^wu(.?)$'), 'u\\1'),
    (re.compile('(.+)r(.?)$'), '\\1R\\2'),
    (re.compile('^zh'), 'Cr'),
    (re.compile('^ch'), 'C'),
    (re.compile('^j'), 'qZ'),
    (re.compile('^z'), 'qZ'),
    (re.compile('^x'), 's'),
    (re.compile('^sh'), 'S'),
    (re.compile('([^CSdst])uo'), '\\1o'),
    (re.compile('^y(.*)$'), 'I\\1'),
    (re.compile('Iai'), 'AI'),
    (re.compile('Ia'), 'A'),
    (re.compile('Ie'), 'E'),
    (re.compile('Ii'), 'i'),
    (re.compile('Iou'), 'V'),
    (re.compile('Iu'), 'v'),
    (re.compile('(.v)(\d?)$'), '\\1I\\2'),
    (re.compile('Io'), 'O'),
    (re.compile('iu'), 'v'),
    (re.compile('ie'), 'E'),
    (re.compile('hui'), 'huei'),
    (re.compile('ui'), 'uI'),
    (re.compile('ai'), 'aI'),
    (re.compile('ei'), 'eI'),
    (re.compile('ia'), 'A'),
    (re.compile('(.*[^h])n([^g]?)$'), '\\1nM\\2'),
    (re.compile('(.*[^h])ng(.?)$'), '\\1n\\2'),
    (re.compile('^v(\d?$)'), 'vI'),
)
CYRILLIC_TABLE = dict(zip(
    u'abwgdEOrZiIklmnopRstufhqcCSHTMUevAV',
    u'абвгдеёжзийклмнопрстуфхццчшщъьыэюяю'
))
