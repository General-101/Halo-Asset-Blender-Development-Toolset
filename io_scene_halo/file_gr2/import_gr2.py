# ##### BEGIN MIT LICENSE BLOCK #####
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Norbyte
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

import io
import os
import bpy
import sys
import zlib

from .. import config
from enum import Enum

class Magic(object):
    def __init__(self):
        self.MagicSize = b'\x20' # Size of magic value structure, in bytes
        self.signature = None # 16-byte long file signature, one of the *Magic constants.
        self.headersSize = None # Size of file header; offset of the start of section data
        self.headerFormat = None # Header format (0 = uncompressed, 1-2 = Oodle0/1 ?)
        self.reserved1 = None # Reserved field
        self.reserved2 = None # Reserved field
        self.format = None # Endianness and address size of the file (derived from the signature)

    # Magic value used for version 7 little-endian 32-bit Granny files
    LittleEndian32Magic = b'\x29\xDE\x6C\xC0\xBA\xA4\x53\x2B\x25\xF5\xB7\xA5\xF6\x66\xE2\xEE'

    # Magic value used for version 7 little-endian 32-bit Granny files
    LittleEndian32Magic2 = b'\x29\x75\x31\x82\xBA\x02\x11\x77\x25\x3A\x60\x2F\xF6\x6A\x8C\x2E'

    # Magic value used for version 6 little-endian 32-bit Granny files
    LittleEndian32MagicV6 = b'\xB8\x67\xB0\xCA\xF8\x6D\xB1\x0F\x84\x72\x8C\x7E\x5E\x19\x00\x1E'

    # Magic value used for version 7 big-endian 32-bit Granny files
    BigEndian32Magic = b'\x0E\x11\x95\xB5\x6A\xA5\xB5\x4B\xEB\x28\x28\x50\x25\x78\xB3\x04'

    # Magic value used for version 7 big-endian 32-bit Granny files
    BigEndian32Magic2 =  b'\x0E\x74\xA2\x0A\x6A\xEB\xEB\x64\xEB\x4E\x1E\xAB\x25\x91\xDB\x8F'

    # Magic value used for version 7 little-endian 64-bit Granny files
    LittleEndian64Magic = b'\xE5\x9B\x49\x5E\x6F\x63\x1F\x14\x1E\x13\xEB\xA9\x90\xBE\xED\xC4'

    # Magic value used for version 7 little-endian 64-bit Granny files
    LittleEndian64Magic2 = b'\xE5\x2F\x4A\xE1\x6F\xC2\x8A\xEE\x1E\xD2\xB4\x4C\x90\xD7\x55\xAF'

    # Magic value used for version 7 big-endian 64-bit Granny files
    BigEndian64Magic = b'\x31\x95\xD4\xE3\x20\xDC\x4F\x62\xCC\x36\xD0\x3A\xB1\x82\xFF\x89'

    # Magic value used for version 7 big-endian 64-bit Granny files
    BigEndian64Magic2 = b'\x31\xC2\x4E\x7C\x20\x40\xA3\x25\xCC\xE1\xC2\x7A\xB1\x32\x49\xF3'

    # Defines endianness and address size
    class Format(Enum):
        LittleEndian32 = 0
        BigEndian32 = 1
        LittleEndian64 = 2
        BigEndian64 = 3

    # Indicates the 32-bitness of the GR2 file.
    @property
    def Is32Bit(self):
        return format == self.Format.LittleEndian32 or format == self.Format.BigEndian32

    # Indicates the 64-bitness of the GR2 file.
    @property
    def Is64Bit(self):
        return format == self.Format.LittleEndian64 or format == self.Format.BigEndian64

    # Indicates the endianness of the GR2 file.
    @property
    def IsLittleEndian(self):
        return format == self.Format.LittleEndian32 or format == self.Format.LittleEndian64

    @staticmethod
    def FormatFromSignature(sig, report):
        if sig == Magic.LittleEndian32Magic or sig == Magic.LittleEndian32Magic2 or sig == Magic.LittleEndian32MagicV6:
            return Magic.Format.LittleEndian32

        elif sig == Magic.BigEndian32Magic or sig == Magic.BigEndian32Magic2:
            return Magic.Format.BigEndian32

        elif sig == Magic.LittleEndian64Magic or sig == Magic.LittleEndian64Magic2:
            return Magic.Format.LittleEndian64

        elif sig == Magic.BigEndian64Magic or sig == Magic.BigEndian64Magic2:
            return Magic.Format.BigEndian64

        else:
            report({'ERROR'}, "Incorrect header signature (maybe not a Granny .GR2 file?)")
            return {'CANCELLED'}

    @staticmethod
    def SignatureFromFormat(format, report):
        if format == Magic.Format.LittleEndian32:
            return  Magic.LittleEndian32Magic

        elif format == Magic.Format.LittleEndian64:
            return  Magic.LittleEndian64Magic

        elif format == Magic.Format.BigEndian32:
            return  Magic.BigEndian32Magic

        elif format == Magic.Format.BigEndian64:
            return Magic.BigEndian64Magic

        else:
            report({'ERROR'}, "Bad format")
            return {'CANCELLED'}

    def SetFormat(self, format, alternateSignature):
        self.format = format
        if alternateSignature:
            if format == Magic.Format.LittleEndian32:
                self.signature = self.LittleEndian32Magic2

            elif format == Magic.Format.LittleEndian64:
                self.signature = self.LittleEndian64Magic2

            elif format == Magic.Format.BigEndian32:
                self.signature = self.BigEndian32Magic2

            elif format == Magic.Format.BigEndian64:
                self.signature = self.BigEndian64Magic2
        else:
            if format == Magic.Format.LittleEndian32:
                self.signature = self.LittleEndian32Magic

            elif format == Magic.Format.LittleEndian64:
                self.signature = self.LittleEndian64Magic

            elif format == Magic.Format.BigEndian32:
                self.signature = self.BigEndian32Magic

            elif format == Magic.Format.BigEndian64:
                self.signature = self.BigEndian64Magic

class Header(object):
    def __init__(self):
        self.DefaultTag =  b'\x80\x00\x00\x37' # Default GR2 tag used for serialization (D:OS)
        self.Tag_DOS = b'\x80\x00\x00\x37' # D:OS vanilla version tag
        self.Tag_DOSEE = b'\x80\x00\x00\x39' # D:OS EE version tag
        self.Tag_DOS2DE = b'\xE5\x7F\x00\x39' # D:OS:2 DE LSM version tag
        self.Version = 7 # Granny file format we support for writing (currently only version 7)
        self.HeaderSize_V6 = b'\x38' # Size of header structure for V6 headers, in bytes
        self.HeaderSize_V7 = b'\x48' # Size of header structure for V7 headers, in bytes
        self.ExtraTagCount = 4 # Number of user-defined tags in the header
        self.version = None # File format version; should be Header.Version
        self.fileSize = None # Total size of .GR2 file, including headers
        self.crc = None # CRC-32 hash of the data starting after the header (offset = HeaderSize) to the end of the file (Header.fileSize - HeaderSize bytes)
        self.sectionsOffset = None # Offset of the section list relative to the beginning of the file
        self.numSections = None # Number of Sections in the .GR2 file
        self.rootType = None # Reference to the type descriptor of the root element in the hierarchy
        self.rootNode = None
        self.tag = None # File format version tag
        self.extraTags = None # Extra application-defined tags
        self.stringTableCrc = None # CRC of string table; seems to be unused?
        self.reserved1 = None
        self.reserved2 = None
        self.reserved3 = None
        
    def Size(self, report):
        if self.version == 6:
            headerSize = self.HeaderSize_V6

        elif self.version == 7:
            headerSize = self.HeaderSize_V7

        else:
            report({'ERROR'}, "Cannot calculate CRC for unknown header versions.")
            return {'CANCELLED'}

        return headerSize

    def CalculateCRC(self, stream, magic, report):
        originalPos = stream.tell()
        int_size = int.from_bytes(self.Size(report), "little")
        int_magic = int.from_bytes(magic.MagicSize, "little")
        totalHeaderSize = int_size + int_magic
        stream.seek(totalHeaderSize)
        body = stream.read((self.fileSize - totalHeaderSize))
        crc = zlib.crc32(body)
        stream.seek(originalPos)

        return crc

class SectionType(Enum):
    Main = 0
    RigidVertex = 1
    RigidIndex = 2
    DeformableVertex = 3
    DeformableIndex = 4
    Texture = 5
    Discardable = 6
    Unloaded = 7
    Max = Unloaded
    Invalid = 0

# Reference to an absolute address within the GR2 file
class SectionReference(object):
    # Returns if the reference points to a valid address within the file
    @property
    def IsValid(self):
        return (self.Section != SectionType.Invalid)

    def __init__(self):
        Section = None # Zero-based index of referenced section (0 .. Header.numSections - 1)
        Offset = None # Offset in bytes from the beginning of the section

    def EqualsObject(self, o):
        if (o == None):
            return False

        reference = o

        return (((reference != None) and (reference.Section == self.Section)) and (reference.Offset == self.Offset))

    def Equals(self, reference):
        return (((reference != None) and (reference.Section == self.Section)) and (reference.Offset == self.Offset))

    def GetHashCode(self):
        return ((self.Section * 31) + ((self.Offset * 31) * 23))

class SectionHeader(object):
    def __init__(self):
        self.compression = None # Type of compression used; 0 = no compression; 1-2 = Oodle 1/2 compression
        self.offsetInFile = None # Absolute position of the section data in the GR2 file
        self.compressedSize = None # Uncompressed size of section data
        self.uncompressedSize = None # Compressed size of section data
        self.alignment = None
        self.first16bit = None # Oodle1 compressor stops
        self.first8bit = None
        self.relocationsOffset = None # Absolute position of the relocation data in the GR2 file
        self.numRelocations = None # Number of relocations for this section
        self.mixedMarshallingDataOffset = None # Absolute position of the mixed-endianness marshalling data in the GR2 file
        self.numMixedMarshallingData = None # Number of mixed-marshalling entries for this section

class Section(object):
    def __init__(self):
        self.SectionHeader = None

def ReadMagic(InputReader, report):
    magic = Magic()
    magic.signature = InputReader.read(16)
    magic.format = Magic.FormatFromSignature(magic.signature, report)
    magic.headersSize = int.from_bytes(InputReader.read(4), "little")
    magic.headerFormat = int.from_bytes(InputReader.read(4), "little")
    magic.reserved1 = int.from_bytes(InputReader.read(4), "little")
    magic.reserved2 = int.from_bytes(InputReader.read(4), "little")
    if (magic.headerFormat != 0):
        report({'ERROR'}, "Compressed GR2 files are not supported")
        return {'CANCELLED'}

    assert (magic.reserved1 == 0)
    assert (magic.reserved2 == 0)

    if True:
        print(" ===== GR2 Magic ===== ")
        print("Format: {0}".format(magic.format))
        print("Headers size: {0}, format: {1}".format(magic.headersSize, magic.headerFormat))
        print("Reserved1-2: {0} {1}".format(magic.reserved1, magic.reserved2))

    return magic

def ReadSectionReferenceUnchecked(reader):
    reference = SectionReference()
    reference.Section = int.from_bytes(reader.read(4), "little")
    reference.Offset = int.from_bytes(reader.read(4), "little")

    return reference

def ReadHeader(InputReader, filepath, magic, report):
    header = Header()
    header.version = int.from_bytes(InputReader.read(4), "little")
    header.fileSize = int.from_bytes(InputReader.read(4), "little")
    header.crc = int.from_bytes(InputReader.read(4), "little")
    header.sectionsOffset = int.from_bytes(InputReader.read(4), "little")
    header.numSections = int.from_bytes(InputReader.read(4), "little")
    header.rootType = ReadSectionReferenceUnchecked(InputReader)
    header.rootNode = ReadSectionReferenceUnchecked(InputReader)
    header.tag = int.from_bytes(InputReader.read(4), "little")
    header.extraTags = []
    for tag in range(header.ExtraTagCount):
        header.extraTags.append(int.from_bytes(InputReader.read(4), "little"))
        
    if (header.version >= 7):
        header.stringTableCrc = int.from_bytes(InputReader.read(4), "little")
        header.reserved1 = int.from_bytes(InputReader.read(4), "little")
        header.reserved2 = int.from_bytes(InputReader.read(4), "little")
        header.reserved3 = int.from_bytes(InputReader.read(4), "little")

    if ((header.version < 6) or (header.version > 7)):
            report({'ERROR'}, "Unsupported GR2 version; file is version {0}, supported versions are 6 and 7".format(header.version))
            return {'CANCELLED'}

    #if self.tag != self.Tag:
    #    report({'ERROR'}, "Incorrect header tag; expected {0:X8}, got {1:X8}".format(self.Tag, self.tag))
    #    return {'CANCELLED'}

    assert (header.fileSize <= os.stat(filepath).st_size), "File length is greater than what the header states it should be."
    assert (header.CalculateCRC(InputReader, magic, report) == header.crc), "Calculated CRC32 does not match what is written in the file"
    assert (header.sectionsOffset == int.from_bytes(header.Size(report), "little")), "Your section offset does not have the correct size"
    assert (header.rootType.Section < header.numSections), "Your rootType section has a lower value compared to the number of sections"
    # TODO: check rootTypeOffset after serialization
    assert (header.stringTableCrc == 0), "This value goes unused. It should always be zero"
    assert (header.reserved1 == 0), "This value goes unused. It should always be zero"
    assert (header.reserved2 == 0), "This value goes unused. It should always be zero"
    assert (header.reserved3 == 0), "This value goes unused. It should always be zero"

    if True:
        print(" ===== GR2 Header ===== ")
        print("Version {0}, Size {1}, CRC {2}".format(header.version, header.fileSize, header.crc))
        print("Offset of sections: {0}, num sections: {1}".format(header.sectionsOffset, header.numSections))
        print("Root type section {0}, Root type offset {1}".format(header.rootType.Section, header.rootType.Offset))
        print("Root node section {0} {1}".format(header.rootNode.Section, header.rootNode.Offset))
        print("Tag: {0}, Strings CRC: {1}".format(header.tag, header.stringTableCrc))
        print("Extra tags: {0} {1} {2} {3}".format(header.extraTags[0], header.extraTags[1], header.extraTags[2], header.extraTags[3]))
        print("Reserved: {0} {1} {2}".format(header.reserved1, header.reserved2, header.reserved3))

    return header

def ReadSectionHeader(InputReader, header):
    section_header = SectionHeader()
    section_header.compression = int.from_bytes(InputReader.read(4), "little")
    section_header.offsetInFile = int.from_bytes(InputReader.read(4), "little")
    section_header.compressedSize = int.from_bytes(InputReader.read(4), "little")
    section_header.uncompressedSize = int.from_bytes(InputReader.read(4), "little")
    section_header.alignment = int.from_bytes(InputReader.read(4), "little")
    section_header.first16bit = int.from_bytes(InputReader.read(4), "little")
    section_header.first8bit = int.from_bytes(InputReader.read(4), "little")
    section_header.relocationsOffset = int.from_bytes(InputReader.read(4), "little")
    section_header.numRelocations = int.from_bytes(InputReader.read(4), "little")
    section_header.mixedMarshallingDataOffset = int.from_bytes(InputReader.read(4), "little")
    section_header.numMixedMarshallingData = int.from_bytes(InputReader.read(4), "little")

    assert (section_header.offsetInFile <= header.fileSize)
    if section_header.compression != 0:
        assert ((section_header.offsetInFile + section_header.compressedSize) <= header.fileSize)

    else:
        assert (section_header.compressedSize == section_header.uncompressedSize)
        assert ((section_header.offsetInFile + section_header.uncompressedSize) <= header.fileSize)

    if True:
        print(" ===== Section Header ===== ")
        print("Compression: {0}".format(section_header.compression))
        print("Offset {0} Comp/UncompSize {1}/{2}".format(section_header.offsetInFile, section_header.compressedSize, section_header.uncompressedSize))
        print("Alignment {0}".format(section_header.alignment))
        print("First 16/8bit: {0}/{1}".format(section_header.first16bit, section_header.first8bit))
        print("Relocations: {0} count {1}".format(section_header.relocationsOffset, section_header.numRelocations))
        print("Marshalling data: {0} count {1}".format(section_header.mixedMarshallingDataOffset, section_header.numMixedMarshallingData))

    return section_header

def UncompressStream(InputStream, Sections):
    if True:
        print(" ===== Repacking sections ===== ")

    totalSize = 0
    for section in Sections:
        totalSize += section.SectionHeader.uncompressedSize

    # Copy the whole file, as we'll update its contents because of relocations and marshalling fixups
    uncompressedStream = totalSize
    Stream = io.BytesIO()
    Reader = Stream
    for i in range(len(Sections)):
        section = Sections[i]
        hdr = section.SectionHeader
        InputStream.seek(hdr.offsetInFile)
        sectionContents = InputStream.read(hdr.compressedSize)
        originalOffset = hdr.offsetInFile
        hdr.offsetInFile = Stream.tell()
        if (section.SectionHeader.compression == 0):
            Stream.write(bytes(sectionContents))

        elif (section.SectionHeader.uncompressedSize > 0):
            if (hdr.compression == 4):
                uncompressed = LSLib.Utils.GrannyWrapper.Decompress4(sectionContents, int(hdr.uncompressedSize))
                Stream.write(bytes(uncompressed))

            else:
                uncompressed = LSLib.Utils.GrannyWrapper.Decompress(int(hdr.compression), sectionContents, int(hdr.uncompressedSize), int(hdr.first16bit), int(hdr.first8bit), int(hdr.uncompressedSize))
                Stream.write(bytes(uncompressed))

        if True:
            print("    {0}: {1} ({2}) --> {3} ({4})".format(i, originalOffset, hdr.compressedSize, hdr.offsetInFile, hdr.uncompressedSize))


def load_file(context, filepath, report):
    InputStream = open(filepath, "rb")
    Magic = ReadMagic(InputStream, report)
    if ((Magic.format != Magic.Format.LittleEndian32) and (Magic.format != Magic.Format.LittleEndian64)):
        report({'ERROR'}, "Only little-endian GR2 files are supported")
        return {'CANCELLED'}

    Header = ReadHeader(InputStream, filepath, Magic, report)
    Sections = []
    for i in range(Header.numSections):
        section = Section()
        section.SectionHeader = ReadSectionHeader(InputStream, Header)
        Sections.append(section)

    assert (InputStream.tell() == Magic.headersSize)

    UncompressStream(InputStream, Sections)
#    for section in Sections:
#        ReadSectionRelocations(section)
#    if (Magic.IsLittleEndian != BitConverter.IsLittleEndian):
#        for section in Sections:
#            ReadSectionMixedMarshallingRelocations(section)
#    rootStruct = StructReference()
#    rootStruct.Offset = (Sections[int(Header.rootType.Section)].Header.offsetInFile + Header.rootType.Offset)
#    Seek(Header.rootNode)
#    ReadStruct(rootStruct.Resolve(self), MemberType.Inline, root, None)

    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.gr2()
