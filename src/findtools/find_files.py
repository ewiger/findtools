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


class FileTypeCondition(object):

    def __init__(self, filetype):
        if filetype in filetypes.keys():
            filetype = filetypes[filetype]
        self.type = filetype

    def match(self, pathname):
        '''
        Match type of the file system entry to satisfy a least of types.
        '''
        if self.type == 'directory' and not os.path.isdir(pathname):
            return False
        if self.type == 'file' and not os.path.isfile(pathname):
            return False
        if self.type == 'link' and not os.path.islink(pathname):
            return False
        return True


class MatchAllPatternsAndTypes(object):

    def __init__(self, filetypes=None, names=None):
        '''
        @param filetypes: a list of flags or names of the file type used as
                          matching condition

        @param names: a list of strings for fnmatch pattern to match file name
                      or compiled regexp object. A string surrounded with '/'
                      is interpreted as a regexp.
        '''
        # We need at least one of the criteria.
        assert names is not None or filetypes is not None
        # File type conditions.
        self.filetype_conditions = list()
        if filetypes is not None:
            assert type(filetypes) == list
            for filetype in filetypes:
                if isinstance(filetype, basestring):
                    filetype_condition = FileTypeCondition(filetype)
                    self.filetype_conditions.append(filetype_condition)
                else:
                    # Assume FileTypeCondition-like instance.
                    self.filetype_conditions.append(filetype)
        # File name conditions.
        self.name_patterns = list()
        if names is not None:
            assert type(names) == list
            for name in names:
                if isinstance(name, basestring):
                    if self.is_a_regexp(name):
                        # Don't forget to cut the '/' wrapping, which is
                        # useless for python re syntaxes.
                        self.name_patterns.append(re.compile(name[1:-1]))
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

    def matches(self, root, name):
        self._root = root
        self._name = name
        self._pathname = mkpathname(root, name)
        if self.filetype_conditions and not self.match_type():
            return False
        if self.name_patterns and not self.match_name():
            return False
        return True

    def __call__(self, root, name):
        return self.matches(root, name)

    def match_type(self):
        '''
        Match type of the file system entry to satisfy all file type condition.
        '''
        return all([(type_condition.match(self._pathname) is True)
                    for type_condition in self.filetype_conditions])

    def match_name(self):
        '''
        Match name of the file system entry to satisfy all of name patterns.
        '''
        return all([(pattern.match(self._name) is not None)
                   for pattern in self.name_patterns])


class MatchAnyPatternsAndTypes(MatchAllPatternsAndTypes):
    '''Overrides 'all' -> to 'any'.'''

    def match_type(self):
        '''
        Match type of the file system entry to satisfy all file type condition.
        '''
        return any([(type_condition.match(self._pathname) is True)
                    for type_condition in self.filetype_conditions])

    def match_name(self):
        '''
        Match name of the file system entry to satisfy all of name patterns.
        '''
        return any([(pattern.match(self._name) is not None)
                   for pattern in self.name_patterns])


class Match(MatchAllPatternsAndTypes):
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
            super(Match, self).__init__(filetypes=[filetype], names=[name])
        elif filetype is not None:
            super(Match, self).__init__(filetypes=[filetype])
        else:
            raise Exception('Either filetype or name argument is expected.')


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
