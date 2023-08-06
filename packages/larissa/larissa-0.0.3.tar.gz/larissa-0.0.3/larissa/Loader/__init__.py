import logging
logger = logging.getLogger("larissa.Loader")

class Loader(object):

    def __init__(self, project):

        self.shared_objects = OrderedDict()

        self.project = project
        self.file = open(self.project.filename,"rb")
        
        self._load_all_bins()

        self._set_triton_arch()

    def _set_triton_arch(self):
        """Triton needs to know what arch it's dealing with. Figure it out and set it."""

        if self.main_bin.arch in ["x86", "x64"]:
            if self.main_bin.bits == 32:
                triton.setArchitecture(triton.ARCH.X86)

            elif self.main_bin.bits == 64:
                triton.setArchitecture(triton.ARCH.X86_64)

            else:
                raise Exception("Unknown bits size of {0}".format(self.main_bin.bits))

        else:
            raise Exception("Unknown architecture of {0}".format(self.main_bin.arch))


    def _load_all_bins(self):
        """Load all the bins! Start with the initial main binary. Then load all the deps."""

        # Try to load the main binary
        self.main_bin = self._load_bin(self.project.filename)

        # Sanity check
        if self.main_bin == None:
            logger.error("Something went wrong. Unable to load specified file.")
            return

        # TODO: Be sure to check the deps of the deps... Maybe make this recursive?
        # Now try to load the deps
        for name in self.main_bin.shared_objects:
            
            path = self.main_bin.shared_objects[name]

            # If we couldn't find the dll, note it and move on
            if path == None:
                logger.warn("Could not find shared object for {0}".format(name))
                continue

            # Load it
            self.shared_objects[name] = self._load_bin(path)


    def _load_bin(self, path):
        """Attempt to determine file type and load sub-class appropriately.
            NOTE: This does NOT initialize any memory. Simply loads the object.
            
            Returns larissa object if successful, or None otherwise.
        """

        with open(path, "rb") as f:

            # Is it an ELF?
            try:
                self.elffile = ELFFile(self.file)
                del self.elffile
                return larissa.Loader.ELF.ELF(self.project, filename=path)

            except ELFError:
                logger.error("Unknown or unsupported file type.")
                return None

            # TODO: Support PE

    def symbol(self, symbol, first=None):
        """Input symbol string to resolve. Return first resolution of symbol as larissa class object.

        first == optional string argument of library name to lookup symbols in first. This is for objects loaded with DF_SYMBOLIC. If not given, normal loading preference is used.
        
        Returns None if the symbol could not be resolved."""

        # Check for first
        if first is not None:
            if symbol in self.shared_objects[first].symbols and self.shared_objects[first].symbols[symbol] != None:
                return self.shared_objects[first].symbols[symbol]

        # Check main object
        if symbol in self.main_bin.symbols and self.main_bin.symbols[symbol].addr != None:
            return self.main_bin.symbols[symbol]

        # Check all loaded shared objects
        for name in self.shared_objects:
            object = self.shared_objects[name]

            if symbol in object.symbols and object.symbols[symbol].addr != None:
                return object.symbols[symbol]

        return None


    def __repr__(self):
        return "<Loader arch={0} bits={1} endianness={2}>".format(self.main_bin.arch, self.main_bin.bits, self.main_bin.endianness)


    ##############
    # Properties #
    ##############

    @property
    def project(self):
        return self.__project

    @project.setter
    def project(self, project):
        if type(project) is not Project:
            raise Exception("Invalid project of type {0}".format(type(project)))

        self.__project = project

    @property
    def file(self):
        """Python file object for the binary opened in read-only mode."""
        return self.__file

    @file.setter
    def file(self, f):
        if type(f) is not file:
            raise Exception("Invalid file property of type {0}".format(type(f)))

        self.__file = f

from collections import OrderedDict

from elftools.elf.elffile import ELFFile
from elftools.elf.elffile import ELFError
from larissa.Project import Project
import larissa.Loader.ELF

import triton
