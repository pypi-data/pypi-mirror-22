#########################################################################
#  The MIT License (MIT)
#
#  Copyright (c) 2014~2015 CIVA LIN (林雪凡)
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files
#  (the "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so,
#  subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##########################################################################


######################################################################
#
# Term description:
#
#   codename:
#     A analyzer short name.
#     e.g., 8c
#
#   comic_id: (str)
#     A comic identifier scope in the whole program.
#     Most internal interface using the comic_id to identify one comic.
#     e.g., 8c/123a97
#
#   local_comic_id: (str)
#     A comic identifier scope in the analyzer (comic site)
#     It is a string and a part of comic's url.
#     e.g., 123a97
#
#   (you should convert local_comic_id <-> comic_id by
#    `analyzer.convert_*` function)
#
#   volume_id: (str)
#     A volume identifier scope in a comic.
#     e.g., "13"
#
#   name: (str)
#     A short volume description.
#     e.g., "vol1"
#
#   comic_entry_url: (str)
#     A url which reference a comic (in this site)
#     This url must contain the local_comic_id.
#
#   extra_data: (dict)
#     A comic level cache data.
#     Analyzer designer can define it structure by her(his) self.
#     e.g., {}
#
######################################################################

import abc


class ComicAnalyzerException(Exception):
    pass


class ComicAnalyzerDisableException(ComicAnalyzerException):
    '''
    Raise in ComicAnalyzer's __init__() will disable this analyzer
    without warning messages.
    '''


class ComicAnalyzer(metaclass=abc.ABCMeta):
    '''Base class of all comic analyzer'''

    @classmethod
    @abc.abstractmethod
    def codename(cls):
        '''
        Return analyzer code name.
        Keep it SHORT and CLEAR. and not conflict with other analyzer.
        Recommend use 2 chars.

        e.g., co, sm, rd
        '''

    @classmethod
    @abc.abstractmethod
    def name(cls):
        '''
        Return analyzer name.
        Recommand include the target site name.

        E.g., 8comic
        '''

    @classmethod
    @abc.abstractmethod
    def site(cls):
        '''
        Return short site url.

        E.g., "vipcomic.com"
        '''

    @abc.abstractmethod
    def info(self):
        '''
        Return Multi-line info message for end user. Include everything
        which the end user need to known.
        Recommend include:
            1. Author, Maintainer,
            2. E-mail,
            3. Custom data fields description.
            4. etc.
        '''

    def __init__(self, custom_data):
        '''
        args:
            custom_data:
                A dict format datapack which setting by end user.
                Analyzer can use those datas to do some user independent
                task (e.g., login, filename pattern).

                The default custom_data == {}.
                All keys and values will be *str* type. parsing by yourself
                and beware user may assign invalid data.

                Make sure __init__() never raise a exception to outside.
        '''

    def convert_to_local_comic_id(self, comic_id):
        if comic_id.startswith(self.codename() + '/'):
            return comic_id[len(self.codename()) + 1:]
        else:
            return None

    def convert_to_comic_id(self, local_comic_id):
        return self.codename() + '/' + local_comic_id

    @abc.abstractmethod
    def url_to_comic_id(self, comic_entry_url):
        '''
            Convert comic_entry_url to comic_id.
            If convert success return a str format url, else return None.
        '''

    @abc.abstractmethod
    def comic_id_to_url(self, comic_id):
        '''
            Convert comic_id to comic_entry_url
            If convert success return a str format comic_id, else return None.
        '''

    @abc.abstractmethod
    def get_comic_info(self, comic_id):
        '''
            Get comic info from the internet
            The return data will be saved into user's comic_db

            return:
                {
                    comic_id: <comic_id>,
                    title: <comic_title>,
                    desc: <comic_desc>,
                    extra_data: {...},
                    volumes: [
                        {
                            'volume_id': <volume_id>,  # e.g., '16', '045'
                            'name': <volume_name>,
                        },
                        {...},
                        ...
                    ]
                }
        '''

    @abc.abstractmethod
    def get_volume_pages(self, comic_id, volume_id, extra_data):
        '''
            Get images url for future download.

            args:
                comic_id:
                    which comic you want to analysis
                volume_id:
                    which volume you want to analysis
                extra_data:
                    the comic extradata create by self.get_comic_info()

            yield:
                {
                    'url': <image_url>,
                    'local_filename': <local_filename>,  # e.g., 012.jpg
                }
        '''
