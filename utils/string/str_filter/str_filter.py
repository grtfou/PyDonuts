#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20130705
#  @date          20130719  - Added ascii function
#  @version       1.0
#  @brief         content string filter
import re
import string

class WordFilter(object):
    def __init__(self):
        pass

    ##
    #  @param       (String) text
    #  @return      (String) text
    def html_tag(self, text):
        ''' To Remove html tags from text '''

        html_tags = ("a", "abbr", "acronym", "address", "area",
                     "test2", "base", "bdo", "big", "blockquote",
                     "body", "br", "button", "caption", "cite",
                     "code", "col", "colgroup", "dd", "del",
                     "dfn", "div", "dl", "DOCTYPE", "dt",
                     "em", "fieldset", "form", "h1", "h2",
                     "h3", "h4", "h5", "h6", "head",
                     "html", "hr", "i", "img", "input",
                     "ins", "kbd", "label", "legend", "li",
                     "link", "map", "meta", "noscript", "object",
                     "ol", "optgroup", "option", "p", "param",
                     "pre", "q", "samp", "script", "select",
                     "small", "span", "strong", "style", "sub",
                     "sup", "table", "tbody", "td", "textarea",
                     "tfoot", "th", "thead", "title", "tr",
                     "tt", "ul", "var", 'strike', 'font', 'u')

        tag_patterns = '|'.join(html_tags)

        starting_tags = re.compile(r"<({0}){{1}}(>|\s+[^<>]*>)".format(tag_patterns))
        ending_tags = re.compile(r"</({0}){{1}}>".format(tag_patterns))
        html_comment_tag = re.compile(r'<![^>]*>')

        text = starting_tags.sub('', text)
        text = ending_tags.sub('', text)
        text = html_comment_tag.sub('', text)

        return text

    ##
    #  @param       (String) text
    #  @return      (String) text
    def url(self, text):
        """
        To remove url string from text

            TODO: 1. clean Chinese url
        """

        regex = re.compile(r' \w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))* ')

        return regex.sub(' ', text)

    ##
    #  @param       (String) text
    #  @return      (String) text
    def email(self, text):
        """
        To remove email string from text
        """

        regex = re.compile(r' ([\w\.-]+)@([\w\.-]+) ')

        return regex.sub(' ', text)

    ##
    #  @param       (String) text
    #               (Boolean) Use html filter?
    #  @return      (String) text
    def all(self, text, html_enable=True):
        """
        To all filter to clean text
        """

        func = set([self.url, self.email])

        if html_enable:
            func.add(self.html_tag)

        return reduce(lambda x, y: y(x), func, text)

    ##
    #  @param       (String-utf8) text
    #               (Boolean) Use sign to split words?
    #               (String) Sign for split words
    #  @return      (String) text
    def ascii(self, text, is_sign=True, sign=','):
        if is_sign:
            table = string.maketrans(string.printable, ' ' * len(string.printable))
            return sign.join(self.all(text).translate(table).split())
        else:
            return self.all(text).translate(None, string.printable)

    def ptt_word(self, text):
        content_lines = text.split('\n')
        new_content = []
        for line in content_lines:
            if line.startswith(':'):
                continue

            if line.startswith('--'):
                break

            new_content.append(line)

        return '\n'.join(new_content)

if __name__ == '__main__':
    import timeit

    test1 = """blah blah <div class='abc'><a href="blah">link<ul></a></div> END"""
    test2 = """大家好
    A wrapper of format_html, <div class='abc'>for http://中文網址.com the common arguments
    need to be formatted https://asdfasdf.COM.TW using the same format string, and aeiou
    'sep'. 'sep' is abc.@yahoo.co.jp also passed t@#$@hrough conditional_escape."""

    my_filter = WordFilter()

    print("Html Tag:", timeit.Timer(
            'f().html_tag(test1)', 'from __main__ import test1, WordFilter as f').timeit(10000))
    print("Email:", timeit.Timer(
            'f().email(test2)', 'from __main__ import test2, WordFilter as f').timeit(10000))
    print("Url:", timeit.Timer(
            'f().url(test2)', 'from __main__ import test2, WordFilter as f').timeit(10000))

    print("All:", timeit.Timer(
            'f().all(test2)', 'from __main__ import test2, WordFilter as f').timeit(10000))

    print my_filter.all(test2)

    print("Alls:", timeit.Timer(
            'f().ascii(test2)', 'from __main__ import test2, WordFilter as f').timeit(10000))

    print my_filter.ascii(test2)
