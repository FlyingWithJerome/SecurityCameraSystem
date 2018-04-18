'''
tag.py

This module includes a simple class Tag.
It tags each frame.
'''

class Tag(object):

    def __init__(self, frame=None, tag=None):
        self.__frame = frame
        self.__tag   = tag

    def add_tag(self, tag):
        self.__tag = tag

    def add_frame(self, frame):
        self.__frame = frame

    def __eq__(self, another_tag):
        if isinstance(another_tag, str):
            return another_tag == self.__tag

        elif isinstance(another_tag, Tag):
            return another_tag.__tag == self.__tag and \
            another_tag.__frame == self.__frame

        else:
            raise TypeError("What are you doing")