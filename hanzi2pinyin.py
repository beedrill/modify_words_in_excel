import pinyin
def hanzi2pinyin(s):
    return pinyin.get(s, delimiter=" ")