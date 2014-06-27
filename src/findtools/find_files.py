import os
from os.path import join
import fnmatch
import re


def mkpathname(root, name):
    return join(root, name)


def anypathname(root, name):
    return True


filetypes = {
    # block (buffered) special
    'b': 'block',
    # character (unbuffered) special
    'c': 'character',
    'd': 'directory',
    # named pipe (FIFO)
    'p': 'namedpipe',
    # regular file
    'f': 'file',
    # symbolic link; this is never true if the -L option or the -follow
    # option is in effect, unless the symbolic link is broken.  If you want
    # to search  for  symbolic  links  when  -L  is  in
    # effect, use -xtype.
    'l': 'link',
    's': 'socket',
    # door (Solaris)
    'D': 'door',
}


class MatchPatterns(object):

    def __init__(self, filetype=None, names=None):
        '''
        @param filetype: flag or name of the file type used as matching
                         condition

        @param names: a string for fnmatch pattern to match file name or
                      compiled regexp object. A string surrounded with '/'
                      is interpreted as a regexp.
        '''
        # File type condition.
        if filetype in filetypes.keys():
            filetype = filetypes[filetype]
        self.type = filetype
        # File name condition.
        self.name_patterns = list()
        if names is not None:
            assert type(names) == list
            for name in names:
                if isinstance(name, basestring):
                    if self.is_a_regexp(name):
                        self.name_patterns.append(re.compile(name))
                    else:
                        self.name_patterns.append(
                            self.compile_fnmatch_pattern(name)
                        )
                else:
                    # Assume it is already a regexp.
                    self.name_pattern = name
        # Initialize private attributes as empty.
        self.__pathname = None
        self.__root = None
        self.__name = None

    def is_a_regexp(self, pattern):
        return pattern.startswith('/') and pattern.endswith('/')

    def compile_fnmatch_pattern(self, pattern):
        return re.compile(fnmatch.translate(pattern))

    def match_type(self):
        if self.type == 'directory' and not os.path.isdir(self.__pathname):
            return False
        if self.type == 'file' and not os.path.isfile(self.__pathname):
            return False
        return True

    def match_name(self):
        return all([(pattern.match(self.__name) is not None)
                   for pattern in self.name_patterns])

    def matches(self, root, name):
        self.__root = root
        self.__name = name
        self.__pathname = mkpathname(root, name)
        if self.type is not None:
            if not self.match_type():
                return False
        if not self.name_patterns:
            return True
        return self.match_name()

    def __call__(self, root, name):
        return self.matches(root, name)


class Match(MatchPatterns):
    '''
    Left for backwards compatibility. Use MatchPatterns which is more general.
    '''

    def __init__(self, filetype=None, name=None):
        '''
        @param filetype: flag or name of the file type used as matching
                         condition

        @param name: a string for fnmatch pattern to match file name or
                     compiled regexp object.
        '''
        if name is not None:
            super(Match, self).__init__(filetype=filetype, names=[name])
        else:
            super(Match, self).__init__(filetype=filetype)


def collect_size(root, name):
    pathname = mkpathname(root, name)
    filesize = os.path.getsize(pathname)
    return (pathname, filesize)


def find_files(path, match=anypathname, collect=mkpathname, recursive=True):
    if not os.path.exists(path):
        raise Exception('Path does not exists: %s' % path)
    walker = os.walk(path)
    if not recursive:
        walker = [next(walker)]
    for root, dirs, files in walker:
        names = dirs + files
        for name in names:
            if match(root, name):
                yield collect(root, name)
