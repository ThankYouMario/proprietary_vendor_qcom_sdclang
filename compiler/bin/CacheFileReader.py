'''===------ CacheFileReader.py--------------------------------------------------===
   (c) 2020 Qualcomm Innovation Center, Inc. All rights reserved.

  ===----------------------------------------------------------------------='''

import sys
import os
import cache_file_pb2


class Header:

    def __init__(self, header):
        self.header = header

    def getToolsVersion(self):
        return str(self.header.tools_major_version) + '.' + str(self.header.tools_minor_version)

    def linker_script_hash(self):
        return self.header.linker_script_hash

    def printHeader(self):
        print("Tools Version : " + self.getToolsVersion())
        print("Linker Script Hash : " + str(self.linker_script_hash()))


class InputFileKind:
    Undef = 0
    ObjectFile = 1
    ArchiveMember = 2
    Archive = 3
    ArchiveFileWithMember = 4


class InputFile(object):

    def __init__(self):
        self.kind = InputFileKind.Undef

    def getKind(self):
        return self.kind

    def setKind(self, kind):
        self.kind = kind

    def isObjectFile(self):
        return self.kind == InputFileKind.ObjectFile

    def dump(self):
        return

    def getDecoratedPath(self):
        return None


class ObjectFile(InputFile):

    def __init__(self, name, hash):
        super(InputFile, self).__init__()
        self.filename = name
        self.hash = hash
        self.setKind(InputFileKind.ObjectFile)

    def getHash(self):
        return self.hash

    def getFileName(self):
        return self.filename

    def dump(self):
        print('{} \t {}'.format(self.getFileName(), self.getHash()))

    def dumpFile(self):
        print('{}'.format(self.getFileName()))

    def getDecoratedPath(self):
        return self.getFileName()


class ArchiveMember(ObjectFile):

    def __init__(self, name, hash):
        super(ArchiveMember, self).__init__(name, hash)
        self.setKind(InputFileKind.ArchiveMember)


class ArchiveFile(InputFile):

    def __init__(self, name, hash):
        super(InputFile, self).__init__()
        self.filename = name
        self.hash = hash
        self.setKind(InputFileKind.Archive)

    def getHash(self):
        return self.hash

    def getFileName(self):
        return self.filename

    def dump(self):
        print('{} \t {}'.format(self.getFileName(), self.getHash()))

    def dumpFile(self):
        print('{}'.format(self.getFileName()))

    def getDecoratedPath(self):
        return self.getFileName()


class ArchiveFileWithMember(InputFile):

    def __init__(self, archivefile, archivemember):
        super(InputFile, self).__init__()
        self.archivefile = archivefile
        self.archivemember = archivemember
        self.setKind(InputFileKind.ArchiveFileWithMember)

    def dump(self):
        print('{}[{}]({}[{}])'.format(self.archivefile.getFileName(),
                                      self.archivefile.getHash(),
                                      self.archivemember.getFileName(),
                                      self.archivemember.getHash()))

    def dumpFile(self):
        print('{}({})'.format(self.archivefile.getFileName(),
                              self.archivemember.getFileName()))

    def getDecoratedPath(self):
        return self.archivefile.getFileName(
        ) + '(' + self.archivemember.getFileName() + ')'


class OutputSection(object):

    def __init__(self, section_name, hash, section_index):
        self.section_name = section_name
        self.hash = hash
        self.section_index = section_index

    def getSectionName(self):
        return self.section_name

    def getSectionHash(self):
        return self.section_hash

    def getSectionIndex(self):
        return self.section_index

    def dump(self):
        print('{}\t{}'.format(self.getSectionName(), self.getSectionIndex()))


class RuleContainer(object):

    def __init__(self, rule_hash):
        self.rule_hash = rule_hash

    def getRuleHash(self):
        return self.rule_hash


class InputSection(object):

    def __init__(self, section_name, out_section_id,
                 input_id, out_sections, input_files):
        self.section_name = section_name
        self.out_section_id = out_section_id
        self.input_id = input_id
        self.input_files = input_files
        self.out_sections = out_sections

    def getSectionName(self):
        return self.section_name

    def getOutSectionName(self, index):
        return self.out_sections[index].getSectionName()

    def getInputPath(self, index):
        return self.input_files[index].getDecoratedPath()

    def dump(self):
        out_section_name = self.getOutSectionName(self.out_section_id)
        input_path = self.getInputPath(self.input_id)
        print('{}\t{}\t{}'.format(self.section_name,
                                  out_section_name, input_path))


class CommonSymbol(object):

    def __init__(self, symbol_name, out_section_id,
                 input_id, out_sections, input_files):
        self.symbol_name = symbol_name
        self.out_section_id = out_section_id
        self.input_id = input_id
        self.input_files = input_files
        self.out_sections = out_sections

    def getSymbolName(self):
        return self.symbol_name

    def getOutSectionName(self, index):
        return self.out_sections[index].getSectionName()

    def getInputPath(self, index):
        return self.input_files[index].getDecoratedPath()

    def dump(self):
        out_section_name = self.getOutSectionName(self.out_section_id)
        input_path = self.getInputPath(self.input_id)
        print('{}\t{}\t{}'.format(self.symbol_name,
                                  out_section_name, input_path))


class CachingInfoDictReader:

    def __init__(self, filename):
        self.dictfile = filename
        self.caching_info_dict = None

    def readDictionary(self):
        self.caching_info_dict = cache_file_pb2.CachingInfoDict()
        if not os.path.exists(self.dictfile):
            print(self.dictfile + " does not exist")
            return
        # Read the dictionary.
        try:
            f = open(self.dictfile, "rb")
            self.caching_info_dict.ParseFromString(f.read())
            f.close()
        except IOError:
            print(self.dictfile + "Could not read dictionary")

    def getHeader(self):
        return Header(self.caching_info_dict.dictionary_header)

    def getInputFiles(self):
        files = []
        if self.caching_info_dict is None:
            return
        caching_info_dict = self.caching_info_dict
        for inputobj in self.caching_info_dict.input_files:
            if inputobj.archive_file_id == 0:
                obj = caching_info_dict.object_files[inputobj.object_file_id]
                files.append(ObjectFile(obj.file_name,
                                        obj.file_hash))
            else:
                obj = caching_info_dict.archive_members[
                    inputobj.object_file_id]
                archivemember = ArchiveMember(
                    obj.member_name, obj.member_hash)
                obj = caching_info_dict.archive_files[inputobj.archive_file_id]
                archivefile = ArchiveFile(obj.file_name,
                                          obj.file_hash)
                files.append(ArchiveFileWithMember(archivefile,
                                                   archivemember))
        return files

    def getOutputSections(self):
        out_sections = []
        if self.caching_info_dict is None:
            return
        caching_info_dict = self.caching_info_dict
        for section_entry in caching_info_dict.output_sections:
            out_sections.append(
                OutputSection(
                    section_entry.section_name,
                    section_entry.hash,
                    section_entry.section_index))
        return out_sections

    def getInputSections(self, outsections, inputfiles):
        inp_sections = []
        if self.caching_info_dict is None:
            return
        caching_info_dict = self.caching_info_dict
        for section_entry in caching_info_dict.input_sections:
            inp_sections.append(
                InputSection(
                    section_entry.section_name, section_entry.out_section_id,
                    section_entry.input_id, outsections, inputfiles))
        return inp_sections

    def getCommonSymbols(self, outsections, inputfiles):
        symbols = []
        if self.caching_info_dict is None:
            return
        caching_info_dict = self.caching_info_dict
        for symbol_entry in caching_info_dict.common_symbols:
            symbols.append(
                CommonSymbol(
                    symbol_entry.symbol_name, symbol_entry.out_section_id,
                                  symbol_entry.input_id,
                                 outsections, inputfiles))
        return symbols
