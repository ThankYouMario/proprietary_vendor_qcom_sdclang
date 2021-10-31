#!/usr/bin/env python2.7

import os
import argparse
import struct
from collections import namedtuple

ELF_CLASS_32 = 1
ELF_CLASS_64 = 2

PT_NULL = 0
PT_LOAD = 1
PT_DYNAMIC = 2
PT_INTERP = 3
PT_NOTE = 4
PT_SHLIB = 5
PT_PHDR = 6
PT_TLS = 7
PT_LOOS = 0x60000000
PT_HIOS = 0x6fffffff
PT_LOPROC = 0x70000000
PT_HIPROC = 0x7FFFFFFF

SHT_NULL = 0
SHT_PROGBITS = 1
SHT_SYMTAB = 2
SHT_STRTAB = 3
SHT_RELA = 4
SHT_HASH = 5
SHT_DYNAMIC = 6
SHT_NOTE = 7
SHT_NOBITS = 8
SHT_REL = 9
SHT_SHLIB = 10
SHT_DYNSYM = 11

SHF_WRITE = (1 << 0)
SHF_ALLOC = (1 << 1)
SHF_EXECINSTR = (1 << 2)
SHF_MERGE = (1 << 4)
SHF_STRINGS = (1 << 5)
SHF_INFO_LINK = (1 << 6)
SHF_LINK_ORDER = (1 << 7)
SHF_OS_NONCONFORMING = (1 << 8)
SHF_GROUP = (1 << 9)
SHF_TLS = (1 << 10)
SHF_COMPRESSED = (1 << 11)

fmt_endian = '<'  # Little Endian by default


def get_ehdr(data, verbose=False):
  global fmt_endian
  e_ident_fmt = '4sBBBBB7s'

  EI_LEN = 16
  if len(data) < EI_LEN:
    raise RuntimeError('Invalid ELF file')
  ehdr_ident = namedtuple('ehdr_ident', 'ei_mag, ei_class, ei_data,'
                          'ei_ver, ei_osabi, ei_abiver, ei_pad')
  ei = ehdr_ident._make(struct.unpack(e_ident_fmt, data[0:EI_LEN]))
  if ei.ei_mag != b'\x7fELF':
    raise RuntimeError('Invalid ELF file')
  if ei.ei_data == 2:
    fmt_endian = '>'
    if verbose:
      print('Big Endian')

  ehdr_fmt = fmt_endian + e_ident_fmt + 'HHIIIIIHHHHHH'
  if ei.ei_class == ELF_CLASS_64:
    ehdr_fmt = fmt_endian + e_ident_fmt + 'HHIQQQIHHHHHH'
  ehdr_fields = ('e_type', 'e_machine', 'e_version', 'e_entry',
                 'e_phoff', 'e_shoff', 'e_flags', 'e_ehsize',
                 'e_phentsize', 'e_phnum', 'e_shentsize',
                 'e_shnum', 'e_shstrndx')
  ehdr_t = namedtuple('ehdr_t', ehdr_ident._fields + ehdr_fields)
  ehdr_len = struct.calcsize(ehdr_fmt)
  ehdr = ehdr_t._make(struct.unpack(ehdr_fmt, data[0:ehdr_len]))
  if verbose:
    print('EHDR:', ehdr)
  return ehdr


def get_phdrs(data, ehdr, verbose=False):
  phdrs = []
  phdr_fmt = fmt_endian
  if ehdr.ei_class == ELF_CLASS_64:
    phdr_fmt += 'II' + 'Q' * 6
    phdr_t = namedtuple('phdr_t', 'p_type, p_flags, p_offset, p_vaddr,'
                        'p_paddr, p_filesz, p_memsz, p_align')
  else:
    phdr_fmt += 'I' * 8
    phdr_t = namedtuple('phdr_t', 'p_type, p_offset, p_vaddr, p_paddr,'
                      'p_filesz, p_memsz, p_flags, p_align')

  if struct.calcsize(phdr_fmt) != ehdr.e_phentsize:
    raise RuntimeError('Phdr size mismatch')
  offset = ehdr.e_phoff
  for idx in range(ehdr.e_phnum):
    phdr = phdr_t._make(struct.unpack(phdr_fmt,
                                      data[offset:offset + ehdr.e_phentsize]))
    phdrs.append(phdr)
    offset += ehdr.e_phentsize
    if verbose:
      print('PHDR', phdr)
  return phdrs


def get_shdrs(data, ehdr, verbose=False):
  shdrs = []
  shdr_t = namedtuple('shdr_t', 'sh_name, sh_type, sh_flags, sh_addr,'
                                'sh_offset, sh_size, sh_link, sh_info,'
                                'sh_addralign, sh_entsize')
  shdr_fmt = fmt_endian
  if ehdr.ei_class == ELF_CLASS_64:
    shdr_fmt += 'IIQQQQIIQQ'
  else:
    shdr_fmt += 'I' * 10
  if struct.calcsize(shdr_fmt) != ehdr.e_shentsize:
    raise RuntimeError('Shdr size mismatch')
  offset = ehdr.e_shoff
  for idx in range(ehdr.e_shnum):
    shdr = shdr_t._make(struct.unpack(shdr_fmt,
                                      data[offset:offset + ehdr.e_shentsize]))
    offset += ehdr.e_shentsize
    shdrs.append(shdr)
  return shdrs


def get_sh_names(data, ehdr, shdrs, verbose=False):
  # shdrs could be empty as section header could be stripped.
  if not shdrs:
    return None
  data = data.decode('ISO-8859-1')
  st = shdrs[ehdr.e_shstrndx]
  sh_names = {}
  if st.sh_type != SHT_STRTAB:
    raise RuntimeError('Invalid STRTAB')
  for sh in shdrs:
    offset = sh.sh_name + st.sh_offset
    name = ''
    while data[offset] != '\0':
      name += data[offset]
      offset += 1
    sh_names[sh] = name
  return sh_names


def get_first_section_for_segment(phdr, shdrs):
  for sh in shdrs:
    if sh.sh_flags & SHF_ALLOC == 0:
      continue
    if sh.sh_offset == phdr.p_offset and sh.sh_addr == phdr.p_vaddr:
      return sh
  return None


def is_emittable_phdr(phdr):
  return phdr.p_filesz and phdr.p_type == PT_LOAD


def byte2hex(x):
  ''' convert char to fixed hex string of length of 2 '''
  return '{0:X}'.format(x).rjust(2, '0')


def vals2hex(vals):
  ''' convert list of char to hex string '''
  return ''.join(map(byte2hex, vals))


def short2bytes(v):
  return [v >> 8, v & 0xFF]


def int2bytes(v):
  return short2bytes(v >> 16) + short2bytes(v & 0xFFFF)


def emit_bin(data, offset, size, width_byte, bank, of):
  print(('Output Binary Format: %s Bit Width: %d, Bank: %d') % (of.name, width_byte * 8, bank))
  of.write(data[offset:offset+size])


def emit_verilog(data, offset, size, width_byte, bank, of):
  print(('Output Verilog Format: %s Bit Width: %d, Bank: %d') % (of.name, width_byte * 8, bank))
  width_elem = {8: 'Q', 4: 'I', 2: 'H', 1: 'B'}
  fmt_elem = width_elem[width_byte]
  if width_byte != struct.calcsize(fmt_elem):
    raise RuntimeError('Element size not match')
  count = size // width_byte
  fmt = fmt_endian + str(count) + fmt_elem
  int2str = lambda v: '{0:X}'.format(v).rjust(width_byte * 2, '0') + '\n'
  vals = struct.unpack_from(fmt, data, offset)
  for v in vals:
    of.write(int2str(v))
  left_over = size - count * width_byte
  if left_over:
    buf = data[offset + count * width_byte:size]
    buf = buf.ljust(width_byte, '\0')
    v = struct.unpack(fmt_endian + fmt_elem, buf)[0]
    of.write(int2str(v))

def emit_i32(data, va, offset, size, is_last_phdr, entry, of):
  ''' Intel 32-bit hex format: https://en.wikipedia.org/wiki/Intel_HEX
      ':' | byte_count_of_data | address | record_type | data | checksum '''
  print(('Output Intel 32-bit Format: ' + of.name))
  emitted = 0
  bytes_per_rec = 16
  va_upper = va >> 16

  checksum = lambda vals: (256 - (sum(vals) & 0xFF)) & 0xFF

  bytes = [2] + short2bytes(0) + [4] + short2bytes(va_upper)
  bytes.append(checksum(bytes))
  of.write(':' + vals2hex(bytes) + '\n')
  while emitted < size:
    bytes_to_emit = min(bytes_per_rec, size - emitted)
    fmt = str(bytes_to_emit) + 'B'
    vals = struct.unpack_from(fmt, data, offset + emitted)
    addr = (va + emitted) & 0xFFFF
    upper_addr = (va + emitted) >> 16
    # Emit another extended linear address record if the 16bit address wraps
    if upper_addr != va_upper:
      va_upper = upper_addr
      bytes = [2] + short2bytes(0) + [4] + short2bytes(va_upper)
      bytes.append(checksum(bytes))
      of.write(':' + vals2hex(bytes) + '\n')

    bytes = [bytes_to_emit] + short2bytes(addr) + [0] + list(vals)
    bytes.append(checksum(bytes))
    of.write(':' + vals2hex(bytes) + '\n')
    emitted += bytes_to_emit

  if is_last_phdr:
    bytes = [4] + short2bytes(0) + [5] + int2bytes(entry)
    bytes.append(checksum(bytes))
    of.write(':' + vals2hex(bytes) + '\n')
    of.write(':00000001FF\n')  # EOF


def emit_m32(data, phdrs, idx, entry, of):
  ''' Doc: https://en.wikipedia.org/wiki/SREC_(file_format) '''
  print(('Output Motorola SREC 32-bit (S3) Format: ' + of.name))
  offset = phdrs[idx].p_offset
  size = phdrs[idx].p_filesz
  addr_width = 32
  bytes_per_rec = 16
  emitted = 0
  checksum = lambda vals: 255 - (sum(vals) & 0xFF)
  while emitted < size:
    bytes_to_emit = min(bytes_per_rec, size - emitted)
    fmt = fmt_endian + str(bytes_to_emit) + 'B'
    vals = struct.unpack_from(fmt, data, offset + emitted)
    addr = phdrs[idx].p_vaddr + emitted
    vals = [addr_width // 8 + bytes_to_emit + 1] + int2bytes(addr) + list(vals)
    vals.append(checksum(vals))  # Checksum
    emitted += bytes_to_emit
    of.write('S3' + vals2hex(vals) + '\n')
  if idx == len(phdrs) - 1:  # emit termination record
    vals = [5] + int2bytes(entry)
    vals.append(checksum(vals))
    of.write('S7' + vals2hex(vals) + '\n')


def emit_hex(data, ehdr, phdrs, shdrs, sh_names, args):
  if args.verbose:
    print('PHDRS:', phdrs)
  emittable_phdrs = [ph for ph in phdrs if is_emittable_phdr(ph)]

  if not emittable_phdrs:
    print('No segment to convert')
    return

  bit_width = args.wb >> 8
  byte_width = bit_width // 8
  bank = args.wb & 0xFF

  output_filename = args.output
  is_combined = args.output_format.endswith('combined')
  is_output_dir = len(emittable_phdrs) > 1 and not is_combined

  if is_output_dir:
    if not os.path.exists(output_filename):
      print(('Creating dir:' + output_filename))
      os.mkdir(output_filename)
  for idx, phdr in enumerate(emittable_phdrs):
    fn = output_filename
    if is_output_dir:
      if shdrs:
        first_sh = get_first_section_for_segment(phdr, shdrs)
        if not first_sh:
          raise RuntimeError('Unable to find section')
        phdr_name = sh_names[first_sh]
      else:
        phdr_name = str(idx)
      fn = output_filename + os.sep + phdr_name
    mode = 'w'
    if idx > 0 and is_combined:
      mode = 'a'
    if args.output_format.startswith('bin'):
      mode += 'b'
    with open(fn, mode) as of:
      if args.output_format.startswith('vhx'):
        emit_verilog(data, phdr.p_offset, phdr.p_filesz, byte_width, bank, of)
      elif args.output_format.startswith('m32'):
        emit_m32(data, emittable_phdrs, idx, ehdr.e_entry, of)
      elif args.output_format.startswith('i32'):
        emit_i32(data, phdr.p_vaddr, phdr.p_offset, phdr.p_filesz,
                 idx == len(emittable_phdrs) - 1, ehdr.e_entry, of)
      elif args.output_format.startswith('bin'):
        emit_bin(data, phdr.p_offset, phdr.p_filesz, byte_width, bank, of)
      else:
        raise RuntimeError('Unknown output format')


def parse_args():
  parser = argparse.ArgumentParser(description='ELF to Hex Converter.')
  group_type = parser.add_mutually_exclusive_group(required=True)
  group_type.add_argument('--vhx', dest='output_format', const='vhx_split',
                          action='store_const', help='Verilog Hex')
  group_type.add_argument('--m32combined', dest='output_format',
                          const='m32_combined', action='store_const',
                          help='Morotola Combined 32-bit Hex')
  group_type.add_argument('--i32combined', dest='output_format',
                          const='i32_combined', action='store_const',
                          help='Intel 32-bit Hex')
  group_type.add_argument('--m32', dest='output_format',
                          const='m32', action='store_const',
                          help='Morotola 32-bit Hex')
  group_type.add_argument('--bin', dest='output_format', const='bin_split',
                          action='store_const', help='Binary')
  group_wb = parser.add_mutually_exclusive_group()
  group_wb.add_argument('--8x1', dest='wb', const=(8 << 8) + 1,
                        action='store_const', default=(8 << 8) + 1)
  group_wb.add_argument('--8x2', dest='wb', const=(8 << 8) + 2,
                        action='store_const')
  group_wb.add_argument('--8x4', dest='wb', const=(8 << 8) + 4,
                        action='store_const')
  group_wb.add_argument('--16x1', dest='wb', const=(16 << 8) + 1,
                        action='store_const')
  group_wb.add_argument('--16x2', dest='wb', const=(16 << 8) + 2,
                        action='store_const')
  group_wb.add_argument('--32x1', dest='wb', const=(32 << 8) + 1,
                        action='store_const')
  group_wb.add_argument('--32x2', dest='wb', const=(32 << 8) + 2,
                        action='store_const')
  group_wb.add_argument('--64x1', dest='wb', const=(64 << 8) + 1,
                        action='store_const')
  parser.add_argument('input_elf', type=argparse.FileType('rb'))
  parser.add_argument('--output', '-o', required=True, help='output file')
  parser.add_argument('--verbose', '-v', action='store_true', help='Verbose')
  args = parser.parse_args()
  if args.wb & 0xFF != 1:
    parser.error('Multiple bank is not supported now')
  return args


def main():
  args = parse_args()
  input_file_name = args.input_elf.name
  data = args.input_elf.read()
  args.input_elf.close()

  ehdr = get_ehdr(data, args.verbose)
  phdrs = get_phdrs(data, ehdr, args.verbose)
  shdrs = get_shdrs(data, ehdr, args.verbose)
  sh_names = get_sh_names(data, ehdr, shdrs, args.verbose)

  print(('Input File: %s [%d-bit size: %d (0x%x)]') % (input_file_name,
                                                       ehdr.ei_class * 32,
                                                       len(data), len(data)))
  emit_hex(data, ehdr, phdrs, shdrs, sh_names, args)

if __name__ == '__main__':
  main()
