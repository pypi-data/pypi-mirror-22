# coding=utf-8
from cla.util import util


def test_read_strength():
    strength_path = "cla/res/dict/s.txt"
    most = util.read_as_set(strength_path, encoding="gbk", skip=3)
    ish = util.read_as_set(strength_path, encoding="gbk", skip=157)

    assert most.__sizeof__() > 0
    assert ish.__sizeof__() > 0
    assert most.__contains__(u"百分之百")
    assert ish.__contains__(u"点点滴滴")


def test_cut_words_in():
    test_file_path = "cla/res/test/sentences.txt"
    result_path = util.cut_words_in(test_file_path, )
    with open(result_path, 'r') as result_file:
        first_line = result_file.readline()
        assert first_line is not None
        assert first_line.split(" ").__sizeof__() > 0
