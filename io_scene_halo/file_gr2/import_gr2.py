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

import os
import bpy
import sys
import zlib

from .. import config
from enum import Enum

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

# Size of magic value structure, in bytes
MagicSize =  b'\x20'

# Size of header structure for V6 headers, in bytes
HeaderSize_V6 = b'\x38'
# Size of header structure for V7 headers, in bytes
HeaderSize_V7 = b'\x48'

Sections = []

class Section:
    Header = None

class SectionReference:
    section = 0
    offset = 0

class Format(Enum):
    LittleEndian32 = 0
    BigEndian32 = 1
    LittleEndian64 = 2
    BigEndian64 = 3

class ReadMagic:
    def __init__(self, import_file, report):
        self.signature = import_file.read(16)
        self.format = FormatFromSignature(self.signature)

        self.headersSize = int.from_bytes(import_file.read(4), "little")
        self.headerFormat = int.from_bytes(import_file.read(4), "little")
        self.reserved1 = int.from_bytes(import_file.read(4), "little")
        self.reserved2 = int.from_bytes(import_file.read(4), "little")

        if self.headerFormat != 0:
            report({'ERROR'}, "Compressed GR2 files are not supported")
            return {'CANCELLED'}

        assert (self.reserved1 == 0), "This value goes unused. It should always be zero"
        assert (self.reserved2 == 0), "This value goes unused. It should always be zero"

        if config.ENABLE_DEBUG:
            print(" ===== GR2 Magic ===== ")
            print("Format: {0}".format(self.format))
            print("Headers size: {0:X8}, format: ".format(self.headersSize, self.headerFormat))
            print("Reserved1-2: {0:X8} {1:X8}".format(self.reserved1, self.reserved2))

class ReadHeader:
    def __init__(self, import_file, filepath, report):
        self.version = int.from_bytes(import_file.read(4), "little")
        self.fileSize = int.from_bytes(import_file.read(4), "little")
        self.crc = int.from_bytes(import_file.read(4), "little")
        self.sectionsOffset = int.from_bytes(import_file.read(4), "little")
        self.numSections = int.from_bytes(import_file.read(4), "little")
        self.rootType = ReadSectionReferenceUnchecked(import_file)
        self.rootNode = ReadSectionReferenceUnchecked(import_file)
        self.tag = int.from_bytes(import_file.read(4), "little")
        self.extraTagsCount = int.from_bytes(import_file.read(4), "little")
        self.extraTags = []
        self.stringTableCrc = 0
        self.reserved1 = 0
        self.reserved2 = 0
        self.reserved3 = 0
        for tag in range(self.extraTagsCount):
            self.extraTags.append(int.from_bytes(import_file.read(4), "little"))

        if self.version >= 7:
            self.stringTableCrc = int.from_bytes(import_file.read(4), "little")
            self.reserved1 = int.from_bytes(import_file.read(4), "little")
            self.reserved2 = int.from_bytes(import_file.read(4), "little")
            self.reserved3 = int.from_bytes(import_file.read(4), "little")

        if self.version < 6 or self.version > 7:
            report({'ERROR'}, "Unsupported GR2 version; file is version {0}, supported versions are 6 and 7".format(self.version))
            return {'CANCELLED'}

        #if self.tag != self.Tag:
        #    report({'ERROR'}, "Incorrect header tag; expected {0:X8}, got {1:X8}".format(self.Tag, self.tag))
        #    return {'CANCELLED'}

        assert (self.fileSize <= os.stat(filepath).st_size), "File length is greater than what the header states it should be."
        assert (CalculateCRC(import_file, filepath, self.version) == self.crc), "File length is greater than what the header states it should be."
        assert (self.sectionsOffset == Size(self.version, True)), "Your section offset does not have the correct size"
        assert (self.rootType.Section < self.numSections), "Your rootType section has a lower value compared to the number of sections"
        # TODO: check rootTypeOffset after serialization
        assert (self.stringTableCrc == 0), "This value goes unused. It should always be zero"
        assert (self.reserved1 == 0), "This value goes unused. It should always be zero"
        assert (self.reserved2 == 0), "This value goes unused. It should always be zero"
        assert (self.reserved3 == 0), "This value goes unused. It should always be zero"

        if config.ENABLE_DEBUG:
            print(" ===== GR2 Header ===== ")
            print("Version {0}, Size {1}, CRC {2:X8}".format(self.version, self.fileSize, self.crc))
            print("Offset of sections: {0}, num sections: {1}".format(self.sectionsOffset, self.numSections))
            print("Root type section {0}, Root type offset {1:X8}".format(self.rootType.Section, self.rootType.Offset))
            print("Root node section {0} {1:X8}".format(self.rootNode.Section, self.rootNode.Offset))
            print("Tag: {0:X8}, Strings CRC: {1:X8}".format(self.tag, self.stringTableCrc))
            print("Extra tags: {0:X8} {1:X8} {2:X8} {3:X8}".format(self.extraTags[0], self.extraTags[1], self.extraTags[2], self.extraTags[3]))
            print("Reserved: {0:X8} {1:X8} {2:X8}".format(self.reserved1, self.reserved2, self.reserved3))

class ReadSectionHeader:
    def __init__(self, import_file):
        self.compression = int.from_bytes(import_file.read(4), "little")
        self.offsetInFile = int.from_bytes(import_file.read(4), "little")
        self.compressedSize = int.from_bytes(import_file.read(4), "little")
        self.uncompressedSize = int.from_bytes(import_file.read(4), "little")
        self.alignment = int.from_bytes(import_file.read(4), "little")
        self.first16bit = int.from_bytes(import_file.read(4), "little")
        self.first8bit = int.from_bytes(import_file.read(4), "little")
        self.relocationsOffset = int.from_bytes(import_file.read(4), "little")
        self.numRelocations = int.from_bytes(import_file.read(4), "little")
        self.mixedMarshallingDataOffset = int.from_bytes(import_file.read(4), "little")
        self.numMixedMarshallingData = int.from_bytes(import_file.read(4), "little")

        #Debug.Assert(header.offsetInFile <= Header.fileSize)

        #if (header.compression != 0)
            #Debug.Assert(header.offsetInFile + header.compressedSize <= Header.fileSize)
        #else
            #Debug.Assert(header.compressedSize == header.uncompressedSize)
            #Debug.Assert(header.offsetInFile + header.uncompressedSize <= Header.fileSize)

def ReadSectionReferenceUnchecked(import_file):
    reference = SectionReference()
    reference.Section = int.from_bytes(import_file.read(4), "little")
    reference.Offset = int.from_bytes(import_file.read(4), "little")

    return reference

def FormatFromSignature(sig):
    if sig == LittleEndian32Magic or sig == LittleEndian32Magic2 or sig == LittleEndian32MagicV6:
        return Format.LittleEndian32

    if sig == BigEndian32Magic or sig == BigEndian32Magic2:
        return Format.BigEndian32

    if sig == LittleEndian64Magic or sig == LittleEndian64Magic2:
        return Format.LittleEndian64

    if sig == BigEndian64Magic or sig == BigEndian64Magic2:
        return Format.BigEndian64

def Size(version, is_int):
    headerSize = 0
    if version == 6:
        headerSize = HeaderSize_V6

    elif version == 7:
        headerSize = HeaderSize_V7

    header_size = headerSize
    if is_int:
        header_size = int.from_bytes(headerSize, "little")

    return header_size

def CalculateCRC(stream, filepath, version):
    originalPos = stream.tell()
    totalHeaderSize = Size(version, False) + MagicSize
    stream.seek(0)
    fileSize = os.stat(filepath).st_size
    body = fileSize - int.from_bytes(totalHeaderSize, "little")
    crc = zlib.crc32(body)
    stream.seek(originalPos)
    return crc

def UncompressStream(import_file):
    totalSize = 0
    for section in Sections:
        totalSize += section.Header.uncompressedSize

    # Copy the whole file, as we'll update its contents because of relocations and marshalling fixups
    uncompressedStream = totalSize
    Stream = uncompressedStream
    Reader = Stream

    for i in range(Sections.Count):
        section = Sections[i]
        hdr = section.Header
        sectionContents = hdr.compressedSize
        import_file.seek(hdr.offsetInFile)
        #import_file.Read(sectionContents, 0, (int)hdr.compressedSize)

        #var originalOffset = hdr.offsetInFile;
        #hdr.offsetInFile = (uint)Stream.Position;
        #if (section.Header.compression == 0)
            #Stream.Write(sectionContents, 0, sectionContents.Length);

        #else if (section.Header.uncompressedSize > 0)
            #if (hdr.compression == 4)
                #var uncompressed = LSLib.Utils.GrannyWrapper.Decompress4(
                    #sectionContents, (int)hdr.uncompressedSize);
                #Stream.Write(uncompressed, 0, uncompressed.Length);

            #else
                #var uncompressed = LSLib.Utils.GrannyWrapper.Decompress(
                    #(int)hdr.compression,
                    #sectionContents, (int)hdr.uncompressedSize,
                    #(int)hdr.first16bit, (int)hdr.first8bit, (int)hdr.uncompressedSize);
                #Stream.Write(uncompressed, 0, uncompressed.Length);

def load_file(context, filepath, report):
    import_file = open(filepath, "rb")
    Magic = ReadMagic(import_file, report)
    if Magic.format != Format.LittleEndian32 and Magic.format != Format.LittleEndian64:
        report({'ERROR'}, "Only little-endian GR2 files are supported")
        return {'CANCELLED'}

    Header = ReadHeader(import_file, filepath, report)
    for i in range(Header.numSections):
        section = Section()
        section.Header = ReadSectionHeader(import_file)
        Sections.append(section)

    #Debug.Assert(InputStream.Position == Magic.headersSize);

    #UncompressStream()

    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.gr2()
