#!/usr/bin/python

import sys
import subprocess
import os
import math
import re
import argparse


class ELFFile:
    def __init__(self, elffile, objdump_tool=None):
    # init an ELFFile object
        self.elffile = elffile
        self.devnull = self.get_devnull()
        self.arch = self.get_arch(self.elffile)
        self.objdump = objdump_tool or self.get_objdump(self.arch)
        self.ofile = self.run_objdump()

    def get_arch(self, elffile):
    # get the arch based on the ELF file
        filetype = self.get_filetype(elffile)
        if '32-bit' in filetype:
            return '32'
        elif '64-bit' in filetype:
            return '64'
        else:
            do_error('Unknown ELF file architecture')

    def get_filetype(self, elffile):
    # get the filetype for the ELF file
        return Util.get_output('file ' + elffile, self.devnull)

    def get_devnull(self):
    # open a devnull file
        return open(os.devnull, 'r+b')

    def get_objdump(self, arch):
    # get the correct objdump to be used based on ELF file arch
        objdump = 'aarch64-linux-gnu-objdump'
        if arch == '32':
            objdump = 'arm-linux-gnueabi-objdump'
        return objdump

    def run_objdump(self):
    # run objdump on the ELF file
        try:
            return Util.get_output(
                    self.objdump + ' -d ' + self.elffile, self.devnull)
        except:
            Util.do_error(self.objdump + ' not found in PATH. See help.')


class ProgFunctionCode:
    def __init__(self, opcode=[], params=[]):
    # init a FunctioCode object
        self.opcode = opcode or []
        self.params = params or []

    def add_opcode(self, op):
    # add a next opcode to the function code
        self.opcode.append(op)

    def add_params(self, p):
    # add the params of the opcode to the function code
        self.params.append(p)


class ProgFunction:
    # list of all functions contained in the objdump output for the ELF file
    fnlist = {}
    # list of all function already added in the call list of some function
    added_fns = {}
    # list of all functions already printed
    printed_fns = {}
    # list of functions to be filtered out from the final CFG display
    filter_fns = {}
    # list of functions displayed in CFG
    added_to_cfg_fns = {}
    start_fn = '_start'
    main_start_fn = 'main'
    libc_start_fn = '__libc_start_main'
    dummy_start_fn = 'dummy_start'

    def __init__(self, code=None, call_list={}, stack_size=0):
    # init a ProgFunction object
        self.code = code or None
        self.call_list = call_list or {}
        self.stack_size = stack_size or 0
        self.final_size = -1
        self.call_size = 0

    def get_call_list(self, fnname):
        if fnname in ProgFunction.fnlist:
            return ProgFunction.fnlist[fnname].call_list
        else:
            return {}

    def add_node_to_dot_cfg(self, node, func):
        # if the user has not specified any filter functions file
        if not ProgFunction.filter_fns:
            return True
        # if the function node has already been visited
        if node in ProgFunction.added_to_cfg_fns:
            return True
        # if the function is in the filter functions file
        if node in ProgFunction.filter_fns:
            return True
        for f in ProgFunction.filter_fns:
            # if there is a path from the current function to one of the
            # functions in the filter functions file
            if self.check_edges(f, node, False):
                ProgFunction.added_to_cfg_fns[node] = None
                return True
        return False

    def check_edges(self, target_node, start_node, flag=True, visited={}):
        for curr_node in self.get_call_list(start_node):
            if flag and curr_node in visited:
                return True
            if curr_node == target_node or \
              target_node in self.get_call_list(curr_node):
                return True
            visited[curr_node] = None
            self.check_edges(target_node, curr_node, flag, visited)
        return False

    def remove_edges(self, from_node, to_node):
        if from_node not in ProgFunction.fnlist or \
           to_node not in ProgFunction.fnlist:
            if Util.verbose:
                print 'FUNCTION NOT FOUND: ' + from_node + ' : ' + to_node
            return

        if Util.verbose:
            print '==========================================================='
            print 'FROM-->TO: ' + from_node + '-->' + to_node
            print 'CALL LIST FOR ' + to_node + ': ' + \
              str(self.get_call_list(to_node).keys())
            print 'ADDED_LIST: ' + str(ProgFunction.added_fns.keys())

        for curr_node in self.get_call_list(to_node).keys():
            # if the function is not present in the list of valid functions
            if curr_node not in ProgFunction.fnlist:
                if Util.verbose:
                    print 'FUNCTION NOT FOUND: ' + curr_node
                continue
            # if it is a leaf node then it cannot cause cycles
            if len(self.get_call_list(curr_node)) == 0:
                continue
            # if the child nodes of curr node are leaf nodes
            flag = True
            for n in self.get_call_list(curr_node):
                if len(self.get_call_list(n)) > 0:
                    flag = False
            if flag:
                continue
            key_node1 = from_node + '-->' + curr_node
            key_node2 = from_node + '-->' + to_node
            if Util.verbose:
                print 'CURR NODE: ' + curr_node
                print 'KEYNODES: ' + key_node1 + ', ' + key_node2
            if key_node1 in ProgFunction.added_fns and \
               key_node2 in ProgFunction.added_fns:
                if curr_node in self.get_call_list(to_node):
                    if self.check_edges(to_node, curr_node):
                        Util.dotted_op += to_node + '->' + \
                          curr_node + '[style=dotted arrowhead=empty]\n'
                        self.remove_node(to_node, curr_node)
                        if Util.verbose:
                            print 'DELETE EDGE: ' + to_node + '-->' + curr_node
                        continue
            ProgFunction.added_fns[key_node1] = None
            self.remove_edges(from_node, curr_node)

    def path_exists(self, a, b, node=None):
        # check if there exists a path from b to a
        # this is essentially a DFS traversal of the call graph rooted at b

        # for recursive functions
        if a == b:
            return True

        # if there is a direct edge from b to a (trivial case)
        if b and b in ProgFunction.fnlist:
            if a in self.get_call_list(b):
                return True

        # else search for 'node' in all functions reached through a
        if node and a:
            if a in ProgFunction.fnlist:
                for c in self.get_call_list(a):
                    if c and c == node:
                        return True
                    return self.path_exists(c, None, node)
            return False

        # check if this function has already been added
        # to the call list of some other function
        if b and b in ProgFunction.added_fns:
            return self.path_exists(b, None, a)
        return False

    def add_to_call_list(self, fn_from, fn_to, flag=False):
        if not flag:
            self.remove_edges(fn_from, fn_to)
        self.call_list[fn_to] = None

    def get_fnname(self, param):
    # get the formatted function name for the current function
        s = param[param.index('<') + 1:param.index('>')]
        ch = [':', '.', '@', '$', '-']
        for c in ch:
            # replace all special chars with '_'
            s = s.replace(c, '_')
        # replace all digits with 'x'
        # Note: this is due to a shortcoming in dot
        # which splits strings on chars and digits
        s = re.sub('\d', 'x', s)
        return s

    def get_fncode(self, ofile, arch):
    # get the code for each function
        inst = Inst()

        fn_start = False
        fnname = ''
        line_count = -1
        line_list = ofile.splitlines()
        for line in line_list:
            line_count += 1
            # convert multiple whitespaces into single space
            line = Util.beautify(line)
            l = line.split(' ')
            if not line or 'Disassembly' in line or \
            '.word' in line or \
            '...' in line:
                fn_start = False
                continue
            elif '+' in line:
                continue
            elif '>:' in line:
                fn_start = True
                fnname = self.get_fnname(l[1])
                ProgFunction.fnlist[fnname] = ProgFunction(ProgFunctionCode())
                continue
            elif line and fn_start == True:
                if fnname not in ProgFunction.fnlist:
                    continue
                op = l[2]
                p = l[3:]
                f = ProgFunction.fnlist[fnname]
                f.code.add_opcode(op)
                f.code.add_params(p)
                if inst.is_branch_inst(op) or \
                inst.is_tail_call(op, line_count, line_list):
                    called_fn = self.get_fnname(str(l[-1]))
                    f.add_to_call_list(fnname, called_fn, True)
                    ProgFunction.added_fns[called_fn] = None
                elif inst.inst_modifies_stack(op, p):
                    i = inst.get_inst_cost(op, p, arch)
                    f.stack_size += int(i)

    def remove_node(self, from_node, node_to_be_removed):
        if from_node and node_to_be_removed:
            call_list = self.get_call_list(from_node)
            if node_to_be_removed in call_list:
                del call_list[node_to_be_removed]

    def add_user_edges(self, edge_file):
        f = Util.do_read_file(edge_file)
        for line in f:
            line = line.strip()
            if not line:
                continue
            [fn_from, fn_to] = line.split(':')
            if fn_from and fn_to:
                if fn_from not in ProgFunction.fnlist:
                    Util.do_error('Function ' + fn_from + ' not found in \
program')
                if fn_to not in ProgFunction.fnlist:
                    Util.do_error('Function ' + fn_to + ' not found in \
program')
                self.add_fake_edge(fn_from, fn_to, flag=False)

    def add_fake_edge(self, fn_from, fn_to, flag=True):
        f = ProgFunction.fnlist[fn_from]
        f.add_to_call_list(fn_from, fn_to, flag)

    def remove_cycles(self, from_fn):
        if from_fn not in ProgFunction.fnlist:
            return
        for curr_fn in self.get_call_list(from_fn).keys():
            self.add_to_call_list(from_fn, curr_fn)

    def prune_call_graph(self):
        s = ProgFunction.start_fn
        m = ProgFunction.main_start_fn
        l = ProgFunction.libc_start_fn
        d = ProgFunction.dummy_start_fn

        if m in ProgFunction.fnlist:
            if l in ProgFunction.fnlist:
                self.add_fake_edge(l, m)
            elif s in ProgFunction.fnlist:
                self.add_fake_edge(s, m)
        if s not in ProgFunction.fnlist:
            root_nodes = set(ProgFunction.fnlist.keys()) - \
            set(ProgFunction.added_fns.keys())
            if root_nodes:
                ProgFunction.start_fn = ProgFunction.dummy_start_fn
                ProgFunction.fnlist[d] = ProgFunction(ProgFunctionCode())
                for root in root_nodes:
                    self.add_fake_edge(d, root)
        # now remove all cycles from the graph
        ProgFunction.added_fns = {}
        self.remove_cycles(ProgFunction.start_fn)

    def print_node(self, node, fn):
        if not node:
            return
        print '### NODE: ' + node + ':' + str(fn.final_size) + ' B'

    def print_nodes(self, root):
        if root in ProgFunction.printed_fns:
            return
        ProgFunction.printed_fns[root] = None

        if root not in ProgFunction.fnlist:
            return
        fn = ProgFunction.fnlist[root]
        print "-------------------------"
        self.print_node(root, fn)
        print "### CALL_LIST:"

        node = ''
        label = ''
        if root == ProgFunction.start_fn:
            label = root + '[label="' + root + '\\n' + \
            ' (' + str(fn.final_size) + ' B)' + '"];\n'

        print_closing_brace = False
        if root == ProgFunction.start_fn or \
            self.add_node_to_dot_cfg(root, fn):
            Util.dot_op += root + '->{'
            print_closing_brace = True

        for func in fn.call_list:
            if func not in ProgFunction.fnlist:
                continue
            fl = ProgFunction.fnlist[func]
            size = str(fl.final_size)
            print  func + ':' + size
            if self.add_node_to_dot_cfg(func, fl):
                node += func + ' '
                label += func + '[label="' + func + '\\n' + \
                '(' + size + ' B)' + '"];\n'

        if node:
            Util.dot_op += node
        if print_closing_brace:
            Util.dot_op += '}\n'
        if label:
            Util.dot_op += label
        if node:
            Util.dot_op += '{rank=same; ' + node + '}\n'

        for c in fn.call_list:
            self.print_nodes(c)

    def print_call_graph(self):
        self.print_nodes(ProgFunction.start_fn)

    def calc_func_size(self, fn):
        if fn not in ProgFunction.fnlist:
            return 0
        f = ProgFunction.fnlist[fn]
        if f.final_size != -1:
            return f.final_size
        else:
            f.final_size = f.stack_size
        for c in f.call_list:
            m = self.calc_func_size(c)
            # only consider the max stack size among all called functions
            if m > f.call_size:
                f.call_size = m
            #f.final_size += self.calc_func_size(c)
        f.final_size += f.call_size
        return f.final_size


class Inst:
    def get_opcode_params(self, p):
    # get the params of the opcode as a list
        if ';' in p:
            i = p.index(';')
            p = p[:i]
        return p

    def is_branch_inst(self, inst):
    # check if the given inst is a 'bl'
        return inst == 'bl'

    def is_unconditional_branch(self, inst):
    # check if the given inst is an unconditional branch
        return inst == 'b'

    def is_nop(self, inst):
        return not inst or 'nop' in inst or '; undefined' in inst

    def is_tail_call(self, op, i, lines):
    # check if the given inst is a tail call
        if not self.is_unconditional_branch(op):
            return False
        line_plus_one = lines[i + 1]
        line_plus_two = lines[i + 2]
        return self.is_nop(line_plus_one) or self.is_nop(line_plus_two)

    def inst_modifies_stack(self, op, p):
        sp = str(p)
        stack_ops = ['add', 'sub']
        return op == 'push' \
            or (op in stack_ops and 'sp' in sp and '#' in sp) \
            or re.search('\[sp,#-.*]!', sp)

    def get_register_size(self, arch):
        return 4 if arch == '32' else 8

    def get_inst_cost(self, op, p, arch):
        inst_cost = 0
        sp = str(p)
        if op == 'push':
            if 'sp' in sp and '#' in sp:
                i = sp.index('#')
                sp = sp[i + 1:]
                j = sp.index(']')
                inst_cost = int(math.fabs(int(sp[:j])))
            else:
                inst_cost = len(p)
            inst_cost *= self.get_register_size(arch)
        elif re.search('\[sp,#-.*]!', sp):
            i = sp.index('#-')
            j = sp.index(']!')
            inst_cost = int(sp[i + 2:j])
        elif 'sp' in sp:
            for param in p:
                if '#' in param:
                    tpar = param.replace(',', '')
                    inst_cost = int(tpar[1:], 0)
                    break
            # we do not consider add of a +ve val to sp
            # also we do not consider sub of a -ve val to sp
            # b'coz those are similar to pop
            if op == 'add' and inst_cost > 0:
                inst_cost = 0
            elif op == 'sub' and inst_cost < 0:
                inst_cost = 0
        return inst_cost


class Util:
    dot_op = ''
    dotted_op = ''
    user_wants_filter = False
    verbose = False

    @staticmethod
    def __init__(dot_op=''):
        Util.dot_op = dot_op or ''

    @staticmethod
    def print_dot_header():
        Util.dot_op += 'digraph cfg { \n'

    @staticmethod
    def print_dot_footer():
        if not Util.user_wants_filter:
            Util.dot_op += Util.dotted_op
        Util.dot_op += '}'

    @staticmethod
    def do_error(msg):
    # print error message
        sys.exit('ERROR: ' + msg)

    @staticmethod
    def do_warn(msg):
    # print warning message
        print 'WARNING: ' + msg

    @staticmethod
    def do_read_file(filename):
    # read a file and return the contents
        f = open(filename, 'r')
        return f

    @staticmethod
    def do_write_file(filename, content):
    # write the content to a file called <filename>
        f = open(filename, 'w+')
        f.write(content)
        f.close()

    @staticmethod
    def get_retval(self, command, err_stream):
    # run the given command and return the return code
        return subprocess.call(command, shell=True, stderr=err_stream)

    @staticmethod
    def get_output(command, err_stream):
    # run the given command and return the output
        return subprocess.check_output(command, shell=True, stderr=err_stream)

    @staticmethod
    def beautify(line):
    # convert multiple whitespaces into single space
    # remove leading and trailing spaces
        line = re.sub('[:]\t\w+\s\w+\s', ' 0000 ', line)
        return (' '.join(line.split())).strip()


parser = argparse.ArgumentParser(description='Snapdragon LLVM ARM Resource \
Analyzer 1.0')

parser.add_argument('elf_file', help='The input ELF file')

parser.add_argument('-c', '--cfg_file', help='File into which the control \
flow graph should be written (in dot format)')

parser.add_argument('-d', '--objdump_tool', help='Path to the objdump tool to \
be used to generate objdump data')

parser.add_argument('-e', '--edge_file', help='File containing a list of \
function-name pairs in the format f:n. The result would be an edge f-->n in \
the CFG.')

parser.add_argument('-f', '--function_file', help='Functions listed in this \
file would be filtered out from the CFG display')

parser.add_argument('-o', '--objdump_file', help='File into which the objdump \
data should be written')

parser.add_argument('-v', '--verbose', help='Verbose Debug Output', \
action="store_true")

args = parser.parse_args()

elffile = ELFFile(args.elf_file, args.objdump_tool)
if args.objdump_file:
    Util.do_write_file(args.objdump_file, elffile.ofile)
Util.print_dot_header()

if args.verbose:
    Util.verbose = True

func = ProgFunction()
func.get_fncode(elffile.ofile, elffile.arch)
func.prune_call_graph()
if args.edge_file:
    func.add_user_edges(args.edge_file)
func.calc_func_size(ProgFunction.start_fn)

if args.function_file:
    f = Util.do_read_file(args.function_file)
    for line in f:
        line = line.strip()
        if line:
            ProgFunction.filter_fns[line] = None
            Util.user_wants_filter = True

func.print_nodes(ProgFunction.start_fn)

Util.print_dot_footer()
if args.cfg_file:
    Util.do_write_file(args.cfg_file, Util.dot_op)
