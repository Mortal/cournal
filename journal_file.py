'''Wrapper for journal-file.h

Generated with:
./ctypesgen.py -I/home/rav/work/systemd/src/systemd -I/home/rav/work/systemd/src/basic -l/usr/lib/systemd/libsystemd-shared-232.so /home/rav/work/systemd/src/journal/journal-file.h -o ../journal_file.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, str):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return int(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, str):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, str):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, str):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, str):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, UserString)):
            self.data = str(obj).encode()
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))


def _c_divide(x, y):
    # Simulate C division
    return x // y if isinstance(x, int) and isinstance(y, int) else x / y

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import platform
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError as e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # FIXME / TODO return '.' and os.path.dirname(__file__)
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")
        dirs.append(os.path.dirname(__file__))

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")
        directories.append(os.path.dirname(__file__))

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        unix_lib_dirs_list = ['/lib', '/usr/lib', '/lib64', '/usr/lib64']
        if sys.platform.startswith('linux'):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            bitage = platform.architecture()[0]
            if bitage.startswith('32'):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ['/lib/i386-linux-gnu', '/usr/lib/i386-linux-gnu']
            elif bitage.startswith('64'):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ['/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu']
            else:
                # guess...
                unix_lib_dirs_list += glob.glob('/lib/*linux-gnu')
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["/usr/lib/systemd/libsystemd-shared-232.so"] = load_library("/usr/lib/systemd/libsystemd-shared-232.so")

# 1 libraries
# End libraries

# No modules

__dev_t = c_ulong # /usr/include/bits/types.h: 133

__uid_t = c_uint # /usr/include/bits/types.h: 134

__gid_t = c_uint # /usr/include/bits/types.h: 135

__ino_t = c_ulong # /usr/include/bits/types.h: 136

__mode_t = c_uint # /usr/include/bits/types.h: 138

__nlink_t = c_ulong # /usr/include/bits/types.h: 139

__off_t = c_long # /usr/include/bits/types.h: 140

__time_t = c_long # /usr/include/bits/types.h: 148

__blksize_t = c_long # /usr/include/bits/types.h: 162

__blkcnt_t = c_long # /usr/include/bits/types.h: 167

__syscall_slong_t = c_long # /usr/include/bits/types.h: 184

# /home/rav/work/systemd/src/systemd/sd-id128.h: 34
class union_sd_id128(Union):
    pass

sd_id128_t = union_sd_id128 # /home/rav/work/systemd/src/systemd/sd-id128.h: 32

union_sd_id128.__slots__ = [
    'bytes',
    'qwords',
]
union_sd_id128._fields_ = [
    ('bytes', c_uint8 * 16),
    ('qwords', c_uint64 * 2),
]

mode_t = __mode_t # /usr/include/sys/types.h: 70

# /usr/include/bits/types/struct_timespec.h: 8
class struct_timespec(Structure):
    pass

struct_timespec.__slots__ = [
    'tv_sec',
    'tv_nsec',
]
struct_timespec._fields_ = [
    ('tv_sec', __time_t),
    ('tv_nsec', __syscall_slong_t),
]

pthread_t = c_ulong # /usr/include/bits/pthreadtypes.h: 60

# /usr/include/bits/uio.h: 43
class struct_iovec(Structure):
    pass

struct_iovec.__slots__ = [
    'iov_base',
    'iov_len',
]
struct_iovec._fields_ = [
    ('iov_base', POINTER(None)),
    ('iov_len', c_size_t),
]

# /usr/include/bits/stat.h: 46
class struct_stat(Structure):
    pass

struct_stat.__slots__ = [
    'st_dev',
    'st_ino',
    'st_nlink',
    'st_mode',
    'st_uid',
    'st_gid',
    '__pad0',
    'st_rdev',
    'st_size',
    'st_blksize',
    'st_blocks',
    'st_atim',
    'st_mtim',
    'st_ctim',
    '__glibc_reserved',
]
struct_stat._fields_ = [
    ('st_dev', __dev_t),
    ('st_ino', __ino_t),
    ('st_nlink', __nlink_t),
    ('st_mode', __mode_t),
    ('st_uid', __uid_t),
    ('st_gid', __gid_t),
    ('__pad0', c_int),
    ('st_rdev', __dev_t),
    ('st_size', __off_t),
    ('st_blksize', __blksize_t),
    ('st_blocks', __blkcnt_t),
    ('st_atim', struct_timespec),
    ('st_mtim', struct_timespec),
    ('st_ctim', struct_timespec),
    ('__glibc_reserved', __syscall_slong_t * 3),
]

usec_t = c_uint64 # /home/rav/work/systemd/src/basic/time-util.h: 29

# /home/rav/work/systemd/src/basic/time-util.h: 40
class struct_dual_timestamp(Structure):
    pass

struct_dual_timestamp.__slots__ = [
    'realtime',
    'monotonic',
]
struct_dual_timestamp._fields_ = [
    ('realtime', usec_t),
    ('monotonic', usec_t),
]

dual_timestamp = struct_dual_timestamp # /home/rav/work/systemd/src/basic/time-util.h: 40

# /home/rav/work/systemd/src/basic/hashmap.h: 52
class struct_OrderedHashmap(Structure):
    pass

OrderedHashmap = struct_OrderedHashmap # /home/rav/work/systemd/src/basic/hashmap.h: 52

# /home/rav/work/systemd/src/basic/hashmap.h: 53
class struct_Set(Structure):
    pass

Set = struct_Set # /home/rav/work/systemd/src/basic/hashmap.h: 53

le32_t = c_uint32 # /home/rav/work/systemd/src/basic/sparse-endian.h: 38

le64_t = c_uint64 # /home/rav/work/systemd/src/basic/sparse-endian.h: 40

# /home/rav/work/systemd/src/journal/journal-def.h: 188
class struct_Header(Structure):
    pass

Header = struct_Header # /home/rav/work/systemd/src/journal/journal-def.h: 34

# /home/rav/work/systemd/src/journal/journal-def.h: 73
class struct_ObjectHeader(Structure):
    pass

ObjectHeader = struct_ObjectHeader # /home/rav/work/systemd/src/journal/journal-def.h: 36

# /home/rav/work/systemd/src/journal/journal-def.h: 140
class union_Object(Union):
    pass

Object = union_Object # /home/rav/work/systemd/src/journal/journal-def.h: 37

# /home/rav/work/systemd/src/journal/journal-def.h: 81
class struct_DataObject(Structure):
    pass

DataObject = struct_DataObject # /home/rav/work/systemd/src/journal/journal-def.h: 39

# /home/rav/work/systemd/src/journal/journal-def.h: 92
class struct_FieldObject(Structure):
    pass

FieldObject = struct_FieldObject # /home/rav/work/systemd/src/journal/journal-def.h: 40

# /home/rav/work/systemd/src/journal/journal-def.h: 105
class struct_EntryObject(Structure):
    pass

EntryObject = struct_EntryObject # /home/rav/work/systemd/src/journal/journal-def.h: 41

# /home/rav/work/systemd/src/journal/journal-def.h: 120
class struct_HashTableObject(Structure):
    pass

HashTableObject = struct_HashTableObject # /home/rav/work/systemd/src/journal/journal-def.h: 42

# /home/rav/work/systemd/src/journal/journal-def.h: 125
class struct_EntryArrayObject(Structure):
    pass

EntryArrayObject = struct_EntryArrayObject # /home/rav/work/systemd/src/journal/journal-def.h: 43

# /home/rav/work/systemd/src/journal/journal-def.h: 133
class struct_TagObject(Structure):
    pass

TagObject = struct_TagObject # /home/rav/work/systemd/src/journal/journal-def.h: 44

# /home/rav/work/systemd/src/journal/journal-def.h: 100
class struct_EntryItem(Structure):
    pass

EntryItem = struct_EntryItem # /home/rav/work/systemd/src/journal/journal-def.h: 46

# /home/rav/work/systemd/src/journal/journal-def.h: 115
class struct_HashItem(Structure):
    pass

HashItem = struct_HashItem # /home/rav/work/systemd/src/journal/journal-def.h: 47

enum_ObjectType = c_int # /home/rav/work/systemd/src/journal/journal-def.h: 62

ObjectType = enum_ObjectType # /home/rav/work/systemd/src/journal/journal-def.h: 62

struct_ObjectHeader.__slots__ = [
    'type',
    'flags',
    'reserved',
    'size',
    'payload',
]
struct_ObjectHeader._fields_ = [
    ('type', c_uint8),
    ('flags', c_uint8),
    ('reserved', c_uint8 * 6),
    ('size', le64_t),
    ('payload', POINTER(c_uint8)),
]

struct_DataObject.__slots__ = [
    'object',
    'hash',
    'next_hash_offset',
    'next_field_offset',
    'entry_offset',
    'entry_array_offset',
    'n_entries',
    'payload',
]
struct_DataObject._fields_ = [
    ('object', ObjectHeader),
    ('hash', le64_t),
    ('next_hash_offset', le64_t),
    ('next_field_offset', le64_t),
    ('entry_offset', le64_t),
    ('entry_array_offset', le64_t),
    ('n_entries', le64_t),
    ('payload', POINTER(c_uint8)),
]

struct_FieldObject.__slots__ = [
    'object',
    'hash',
    'next_hash_offset',
    'head_data_offset',
    'payload',
]
struct_FieldObject._fields_ = [
    ('object', ObjectHeader),
    ('hash', le64_t),
    ('next_hash_offset', le64_t),
    ('head_data_offset', le64_t),
    ('payload', POINTER(c_uint8)),
]

struct_EntryItem.__slots__ = [
    'object_offset',
    'hash',
]
struct_EntryItem._fields_ = [
    ('object_offset', le64_t),
    ('hash', le64_t),
]

struct_EntryObject.__slots__ = [
    'object',
    'seqnum',
    'realtime',
    'monotonic',
    'boot_id',
    'xor_hash',
    'items',
]
struct_EntryObject._fields_ = [
    ('object', ObjectHeader),
    ('seqnum', le64_t),
    ('realtime', le64_t),
    ('monotonic', le64_t),
    ('boot_id', sd_id128_t),
    ('xor_hash', le64_t),
    ('items', POINTER(EntryItem)),
]

struct_HashItem.__slots__ = [
    'head_hash_offset',
    'tail_hash_offset',
]
struct_HashItem._fields_ = [
    ('head_hash_offset', le64_t),
    ('tail_hash_offset', le64_t),
]

struct_HashTableObject.__slots__ = [
    'object',
    'items',
]
struct_HashTableObject._fields_ = [
    ('object', ObjectHeader),
    ('items', POINTER(HashItem)),
]

struct_EntryArrayObject.__slots__ = [
    'object',
    'next_entry_array_offset',
    'items',
]
struct_EntryArrayObject._fields_ = [
    ('object', ObjectHeader),
    ('next_entry_array_offset', le64_t),
    ('items', POINTER(le64_t)),
]

struct_TagObject.__slots__ = [
    'object',
    'seqnum',
    'epoch',
    'tag',
]
struct_TagObject._fields_ = [
    ('object', ObjectHeader),
    ('seqnum', le64_t),
    ('epoch', le64_t),
    ('tag', c_uint8 * (_c_divide(256, 8))),
]

union_Object.__slots__ = [
    'object',
    'data',
    'field',
    'entry',
    'hash_table',
    'entry_array',
    'tag',
]
union_Object._fields_ = [
    ('object', ObjectHeader),
    ('data', DataObject),
    ('field', FieldObject),
    ('entry', EntryObject),
    ('hash_table', HashTableObject),
    ('entry_array', EntryArrayObject),
    ('tag', TagObject),
]

struct_Header.__slots__ = [
    'signature',
    'compatible_flags',
    'incompatible_flags',
    'state',
    'reserved',
    'file_id',
    'machine_id',
    'boot_id',
    'seqnum_id',
    'header_size',
    'arena_size',
    'data_hash_table_offset',
    'data_hash_table_size',
    'field_hash_table_offset',
    'field_hash_table_size',
    'tail_object_offset',
    'n_objects',
    'n_entries',
    'tail_entry_seqnum',
    'head_entry_seqnum',
    'entry_array_offset',
    'head_entry_realtime',
    'tail_entry_realtime',
    'tail_entry_monotonic',
    'n_data',
    'n_fields',
    'n_tags',
    'n_entry_arrays',
]
struct_Header._fields_ = [
    ('signature', c_uint8 * 8),
    ('compatible_flags', le32_t),
    ('incompatible_flags', le32_t),
    ('state', c_uint8),
    ('reserved', c_uint8 * 7),
    ('file_id', sd_id128_t),
    ('machine_id', sd_id128_t),
    ('boot_id', sd_id128_t),
    ('seqnum_id', sd_id128_t),
    ('header_size', le64_t),
    ('arena_size', le64_t),
    ('data_hash_table_offset', le64_t),
    ('data_hash_table_size', le64_t),
    ('field_hash_table_offset', le64_t),
    ('field_hash_table_size', le64_t),
    ('tail_object_offset', le64_t),
    ('n_objects', le64_t),
    ('n_entries', le64_t),
    ('tail_entry_seqnum', le64_t),
    ('head_entry_seqnum', le64_t),
    ('entry_array_offset', le64_t),
    ('head_entry_realtime', le64_t),
    ('tail_entry_realtime', le64_t),
    ('tail_entry_monotonic', le64_t),
    ('n_data', le64_t),
    ('n_fields', le64_t),
    ('n_tags', le64_t),
    ('n_entry_arrays', le64_t),
]

# /home/rav/work/systemd/src/journal/mmap-cache.h: 28
class struct_MMapCache(Structure):
    pass

MMapCache = struct_MMapCache # /home/rav/work/systemd/src/journal/mmap-cache.h: 28

# /home/rav/work/systemd/src/systemd/sd-event.h: 42
class struct_sd_event(Structure):
    pass

sd_event = struct_sd_event # /home/rav/work/systemd/src/systemd/sd-event.h: 42

# /home/rav/work/systemd/src/systemd/sd-event.h: 43
class struct_sd_event_source(Structure):
    pass

sd_event_source = struct_sd_event_source # /home/rav/work/systemd/src/systemd/sd-event.h: 43

# /home/rav/work/systemd/src/journal/journal-file.h: 45
class struct_JournalMetrics(Structure):
    pass

struct_JournalMetrics.__slots__ = [
    'max_size',
    'min_size',
    'max_use',
    'min_use',
    'keep_free',
    'n_max_files',
]
struct_JournalMetrics._fields_ = [
    ('max_size', c_uint64),
    ('min_size', c_uint64),
    ('max_use', c_uint64),
    ('min_use', c_uint64),
    ('keep_free', c_uint64),
    ('n_max_files', c_uint64),
]

JournalMetrics = struct_JournalMetrics # /home/rav/work/systemd/src/journal/journal-file.h: 45

enum_direction = c_int # /home/rav/work/systemd/src/journal/journal-file.h: 50

DIRECTION_UP = 0 # /home/rav/work/systemd/src/journal/journal-file.h: 50

DIRECTION_DOWN = (DIRECTION_UP + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 50

direction_t = enum_direction # /home/rav/work/systemd/src/journal/journal-file.h: 50

enum_LocationType = c_int # /home/rav/work/systemd/src/journal/journal-file.h: 64

LOCATION_HEAD = 0 # /home/rav/work/systemd/src/journal/journal-file.h: 64

LOCATION_TAIL = (LOCATION_HEAD + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 64

LOCATION_DISCRETE = (LOCATION_TAIL + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 64

LOCATION_SEEK = (LOCATION_DISCRETE + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 64

LocationType = enum_LocationType # /home/rav/work/systemd/src/journal/journal-file.h: 64

enum_OfflineState = c_int # /home/rav/work/systemd/src/journal/journal-file.h: 74

OFFLINE_JOINED = 0 # /home/rav/work/systemd/src/journal/journal-file.h: 74

OFFLINE_SYNCING = (OFFLINE_JOINED + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 74

OFFLINE_OFFLINING = (OFFLINE_SYNCING + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 74

OFFLINE_CANCEL = (OFFLINE_OFFLINING + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 74

OFFLINE_AGAIN_FROM_SYNCING = (OFFLINE_CANCEL + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 74

OFFLINE_AGAIN_FROM_OFFLINING = (OFFLINE_AGAIN_FROM_SYNCING + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 74

OFFLINE_DONE = (OFFLINE_AGAIN_FROM_OFFLINING + 1) # /home/rav/work/systemd/src/journal/journal-file.h: 74

OfflineState = enum_OfflineState # /home/rav/work/systemd/src/journal/journal-file.h: 74

# /home/rav/work/systemd/src/journal/journal-file.h: 144
class struct_JournalFile(Structure):
    pass

struct_JournalFile.__slots__ = [
    'fd',
    'mode',
    'flags',
    'prot',
    'writable',
    'compress_xz',
    'compress_lz4',
    'seal',
    'defrag_on_close',
    'close_fd',
    'archive',
    'tail_entry_monotonic_valid',
    'last_direction',
    'location_type',
    'last_n_entries',
    'path',
    'last_stat',
    'last_stat_usec',
    'header',
    'data_hash_table',
    'field_hash_table',
    'current_offset',
    'current_seqnum',
    'current_realtime',
    'current_monotonic',
    'current_boot_id',
    'current_xor_hash',
    'metrics',
    'mmap',
    'post_change_timer',
    'post_change_timer_period',
    'chain_cache',
    'offline_thread',
    'offline_state',
]
struct_JournalFile._fields_ = [
    ('fd', c_int),
    ('mode', mode_t),
    ('flags', c_int),
    ('prot', c_int),
    ('writable', c_bool, 1),
    ('compress_xz', c_bool, 1),
    ('compress_lz4', c_bool, 1),
    ('seal', c_bool, 1),
    ('defrag_on_close', c_bool, 1),
    ('close_fd', c_bool, 1),
    ('archive', c_bool, 1),
    ('tail_entry_monotonic_valid', c_bool, 1),
    ('last_direction', direction_t),
    ('location_type', LocationType),
    ('last_n_entries', c_uint64),
    ('path', String),
    ('last_stat', struct_stat),
    ('last_stat_usec', usec_t),
    ('header', POINTER(Header)),
    ('data_hash_table', POINTER(HashItem)),
    ('field_hash_table', POINTER(HashItem)),
    ('current_offset', c_uint64),
    ('current_seqnum', c_uint64),
    ('current_realtime', c_uint64),
    ('current_monotonic', c_uint64),
    ('current_boot_id', sd_id128_t),
    ('current_xor_hash', c_uint64),
    ('metrics', JournalMetrics),
    ('mmap', POINTER(MMapCache)),
    ('post_change_timer', POINTER(sd_event_source)),
    ('post_change_timer_period', usec_t),
    ('chain_cache', POINTER(OrderedHashmap)),
    ('offline_thread', pthread_t),
    ('offline_state', OfflineState),
]

JournalFile = struct_JournalFile # /home/rav/work/systemd/src/journal/journal-file.h: 144

# /home/rav/work/systemd/src/journal/journal-file.h: 146
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_open'):
    journal_file_open = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_open
    journal_file_open.argtypes = [c_int, String, c_int, mode_t, c_bool, c_bool, POINTER(JournalMetrics), POINTER(MMapCache), POINTER(Set), POINTER(JournalFile), POINTER(POINTER(JournalFile))]
    journal_file_open.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 159
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_set_offline'):
    journal_file_set_offline = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_set_offline
    journal_file_set_offline.argtypes = [POINTER(JournalFile), c_bool]
    journal_file_set_offline.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 160
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_is_offlining'):
    journal_file_is_offlining = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_is_offlining
    journal_file_is_offlining.argtypes = [POINTER(JournalFile)]
    journal_file_is_offlining.restype = c_bool

# /home/rav/work/systemd/src/journal/journal-file.h: 161
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_close'):
    journal_file_close = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_close
    journal_file_close.argtypes = [POINTER(JournalFile)]
    journal_file_close.restype = POINTER(JournalFile)

# /home/rav/work/systemd/src/journal/journal-file.h: 162
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_close_set'):
    journal_file_close_set = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_close_set
    journal_file_close_set.argtypes = [POINTER(Set)]
    journal_file_close_set.restype = None

# /home/rav/work/systemd/src/journal/journal-file.h: 164
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_open_reliably'):
    journal_file_open_reliably = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_open_reliably
    journal_file_open_reliably.argtypes = [String, c_int, mode_t, c_bool, c_bool, POINTER(JournalMetrics), POINTER(MMapCache), POINTER(Set), POINTER(JournalFile), POINTER(POINTER(JournalFile))]
    journal_file_open_reliably.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 210
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_move_to_object'):
    journal_file_move_to_object = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_move_to_object
    journal_file_move_to_object.argtypes = [POINTER(JournalFile), ObjectType, c_uint64, POINTER(POINTER(Object))]
    journal_file_move_to_object.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 212
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_entry_n_items'):
    journal_file_entry_n_items = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_entry_n_items
    journal_file_entry_n_items.argtypes = [POINTER(Object)]
    journal_file_entry_n_items.restype = c_uint64

# /home/rav/work/systemd/src/journal/journal-file.h: 213
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_entry_array_n_items'):
    journal_file_entry_array_n_items = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_entry_array_n_items
    journal_file_entry_array_n_items.argtypes = [POINTER(Object)]
    journal_file_entry_array_n_items.restype = c_uint64

# /home/rav/work/systemd/src/journal/journal-file.h: 214
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_hash_table_n_items'):
    journal_file_hash_table_n_items = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_hash_table_n_items
    journal_file_hash_table_n_items.argtypes = [POINTER(Object)]
    journal_file_hash_table_n_items.restype = c_uint64

# /home/rav/work/systemd/src/journal/journal-file.h: 216
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_append_object'):
    journal_file_append_object = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_append_object
    journal_file_append_object.argtypes = [POINTER(JournalFile), ObjectType, c_uint64, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_append_object.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 217
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_append_entry'):
    journal_file_append_entry = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_append_entry
    journal_file_append_entry.argtypes = [POINTER(JournalFile), POINTER(dual_timestamp), POINTER(struct_iovec), c_uint, POINTER(c_uint64), POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_append_entry.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 219
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_find_data_object'):
    journal_file_find_data_object = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_find_data_object
    journal_file_find_data_object.argtypes = [POINTER(JournalFile), POINTER(None), c_uint64, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_find_data_object.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 220
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_find_data_object_with_hash'):
    journal_file_find_data_object_with_hash = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_find_data_object_with_hash
    journal_file_find_data_object_with_hash.argtypes = [POINTER(JournalFile), POINTER(None), c_uint64, c_uint64, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_find_data_object_with_hash.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 222
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_find_field_object'):
    journal_file_find_field_object = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_find_field_object
    journal_file_find_field_object.argtypes = [POINTER(JournalFile), POINTER(None), c_uint64, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_find_field_object.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 223
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_find_field_object_with_hash'):
    journal_file_find_field_object_with_hash = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_find_field_object_with_hash
    journal_file_find_field_object_with_hash.argtypes = [POINTER(JournalFile), POINTER(None), c_uint64, c_uint64, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_find_field_object_with_hash.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 225
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_reset_location'):
    journal_file_reset_location = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_reset_location
    journal_file_reset_location.argtypes = [POINTER(JournalFile)]
    journal_file_reset_location.restype = None

# /home/rav/work/systemd/src/journal/journal-file.h: 226
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_save_location'):
    journal_file_save_location = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_save_location
    journal_file_save_location.argtypes = [POINTER(JournalFile), POINTER(Object), c_uint64]
    journal_file_save_location.restype = None

# /home/rav/work/systemd/src/journal/journal-file.h: 227
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_compare_locations'):
    journal_file_compare_locations = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_compare_locations
    journal_file_compare_locations.argtypes = [POINTER(JournalFile), POINTER(JournalFile)]
    journal_file_compare_locations.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 228
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_next_entry'):
    journal_file_next_entry = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_next_entry
    journal_file_next_entry.argtypes = [POINTER(JournalFile), c_uint64, direction_t, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_next_entry.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 230
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_next_entry_for_data'):
    journal_file_next_entry_for_data = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_next_entry_for_data
    journal_file_next_entry_for_data.argtypes = [POINTER(JournalFile), POINTER(Object), c_uint64, c_uint64, direction_t, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_next_entry_for_data.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 232
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_move_to_entry_by_seqnum'):
    journal_file_move_to_entry_by_seqnum = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_move_to_entry_by_seqnum
    journal_file_move_to_entry_by_seqnum.argtypes = [POINTER(JournalFile), c_uint64, direction_t, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_move_to_entry_by_seqnum.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 233
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_move_to_entry_by_realtime'):
    journal_file_move_to_entry_by_realtime = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_move_to_entry_by_realtime
    journal_file_move_to_entry_by_realtime.argtypes = [POINTER(JournalFile), c_uint64, direction_t, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_move_to_entry_by_realtime.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 234
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_move_to_entry_by_monotonic'):
    journal_file_move_to_entry_by_monotonic = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_move_to_entry_by_monotonic
    journal_file_move_to_entry_by_monotonic.argtypes = [POINTER(JournalFile), sd_id128_t, c_uint64, direction_t, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_move_to_entry_by_monotonic.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 236
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_move_to_entry_by_offset_for_data'):
    journal_file_move_to_entry_by_offset_for_data = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_move_to_entry_by_offset_for_data
    journal_file_move_to_entry_by_offset_for_data.argtypes = [POINTER(JournalFile), c_uint64, c_uint64, direction_t, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_move_to_entry_by_offset_for_data.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 237
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_move_to_entry_by_seqnum_for_data'):
    journal_file_move_to_entry_by_seqnum_for_data = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_move_to_entry_by_seqnum_for_data
    journal_file_move_to_entry_by_seqnum_for_data.argtypes = [POINTER(JournalFile), c_uint64, c_uint64, direction_t, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_move_to_entry_by_seqnum_for_data.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 238
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_move_to_entry_by_realtime_for_data'):
    journal_file_move_to_entry_by_realtime_for_data = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_move_to_entry_by_realtime_for_data
    journal_file_move_to_entry_by_realtime_for_data.argtypes = [POINTER(JournalFile), c_uint64, c_uint64, direction_t, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_move_to_entry_by_realtime_for_data.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 239
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_move_to_entry_by_monotonic_for_data'):
    journal_file_move_to_entry_by_monotonic_for_data = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_move_to_entry_by_monotonic_for_data
    journal_file_move_to_entry_by_monotonic_for_data.argtypes = [POINTER(JournalFile), c_uint64, sd_id128_t, c_uint64, direction_t, POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_move_to_entry_by_monotonic_for_data.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 241
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_copy_entry'):
    journal_file_copy_entry = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_copy_entry
    journal_file_copy_entry.argtypes = [POINTER(JournalFile), POINTER(JournalFile), POINTER(Object), c_uint64, POINTER(c_uint64), POINTER(POINTER(Object)), POINTER(c_uint64)]
    journal_file_copy_entry.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 243
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_dump'):
    journal_file_dump = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_dump
    journal_file_dump.argtypes = [POINTER(JournalFile)]
    journal_file_dump.restype = None

# /home/rav/work/systemd/src/journal/journal-file.h: 244
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_print_header'):
    journal_file_print_header = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_print_header
    journal_file_print_header.argtypes = [POINTER(JournalFile)]
    journal_file_print_header.restype = None

# /home/rav/work/systemd/src/journal/journal-file.h: 246
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_rotate'):
    journal_file_rotate = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_rotate
    journal_file_rotate.argtypes = [POINTER(POINTER(JournalFile)), c_bool, c_bool, POINTER(Set)]
    journal_file_rotate.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 248
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_post_change'):
    journal_file_post_change = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_post_change
    journal_file_post_change.argtypes = [POINTER(JournalFile)]
    journal_file_post_change.restype = None

# /home/rav/work/systemd/src/journal/journal-file.h: 249
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_enable_post_change_timer'):
    journal_file_enable_post_change_timer = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_enable_post_change_timer
    journal_file_enable_post_change_timer.argtypes = [POINTER(JournalFile), POINTER(sd_event), usec_t]
    journal_file_enable_post_change_timer.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 251
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_reset_metrics'):
    journal_reset_metrics = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_reset_metrics
    journal_reset_metrics.argtypes = [POINTER(JournalMetrics)]
    journal_reset_metrics.restype = None

# /home/rav/work/systemd/src/journal/journal-file.h: 252
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_default_metrics'):
    journal_default_metrics = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_default_metrics
    journal_default_metrics.argtypes = [POINTER(JournalMetrics), c_int]
    journal_default_metrics.restype = None

# /home/rav/work/systemd/src/journal/journal-file.h: 254
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_get_cutoff_realtime_usec'):
    journal_file_get_cutoff_realtime_usec = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_get_cutoff_realtime_usec
    journal_file_get_cutoff_realtime_usec.argtypes = [POINTER(JournalFile), POINTER(usec_t), POINTER(usec_t)]
    journal_file_get_cutoff_realtime_usec.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 255
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_get_cutoff_monotonic_usec'):
    journal_file_get_cutoff_monotonic_usec = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_get_cutoff_monotonic_usec
    journal_file_get_cutoff_monotonic_usec.argtypes = [POINTER(JournalFile), sd_id128_t, POINTER(usec_t), POINTER(usec_t)]
    journal_file_get_cutoff_monotonic_usec.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 257
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_rotate_suggested'):
    journal_file_rotate_suggested = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_rotate_suggested
    journal_file_rotate_suggested.argtypes = [POINTER(JournalFile), usec_t]
    journal_file_rotate_suggested.restype = c_bool

# /home/rav/work/systemd/src/journal/journal-file.h: 259
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_map_data_hash_table'):
    journal_file_map_data_hash_table = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_map_data_hash_table
    journal_file_map_data_hash_table.argtypes = [POINTER(JournalFile)]
    journal_file_map_data_hash_table.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 260
if hasattr(_libs['/usr/lib/systemd/libsystemd-shared-232.so'], 'journal_file_map_field_hash_table'):
    journal_file_map_field_hash_table = _libs['/usr/lib/systemd/libsystemd-shared-232.so'].journal_file_map_field_hash_table
    journal_file_map_field_hash_table.argtypes = [POINTER(JournalFile)]
    journal_file_map_field_hash_table.restype = c_int

# /home/rav/work/systemd/src/journal/journal-file.h: 176
def ALIGN64(x):
    return ((x + 7) & (~7))

# /home/rav/work/systemd/src/journal/journal-file.h: 177
def VALID64(x):
    return ((x & 7) == 0)

JournalMetrics = struct_JournalMetrics # /home/rav/work/systemd/src/journal/journal-file.h: 45

JournalFile = struct_JournalFile # /home/rav/work/systemd/src/journal/journal-file.h: 144

# No inserted files

