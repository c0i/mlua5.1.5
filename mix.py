#!/usr/bin/env python
#

import os
import sys
import numpy as np
from argparse import ArgumentParser

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run(cmd, quiet=False):
    from subprocess import call
    if quiet:
        ret = call(cmd, shell=True, stdout=subprocess.PIPE)
    else:
        ret = call(cmd, shell=True)
    if ret != 0:
        print bcolors.FAIL
        print "==> Command failed: " + cmd
        print "==> Stopping build."
        print bcolors.ENDC
        sys.exit(1)



def main(mix=True,dryrun=True):
    op_header = '''
/*
** grep "ORDER OP" if you change these enums
*/

typedef enum {
/*----------------------------------------------------------------------
name        args    description
------------------------------------------------------------------------*/
%s
OP_VARARG/* A B R(A), R(A+1), ..., R(A+B-1) = vararg        */
} OpCode;
    '''

    enum = '''
OP_MOVE,/*  A B R(A) := R(B)                    */
OP_LOADK,/* A Bx    R(A) := Kst(Bx)                 */
OP_LOADBOOL,/*  A B C   R(A) := (Bool)B; if (C) pc++            */
OP_LOADNIL,/*   A B R(A) := ... := R(B) := nil          */
OP_GETUPVAL,/*  A B R(A) := UpValue[B]              */
OP_GETGLOBAL,/* A Bx    R(A) := Gbl[Kst(Bx)]                */
OP_GETTABLE,/*  A B C   R(A) := R(B)[RK(C)]             */
OP_SETGLOBAL,/* A Bx    Gbl[Kst(Bx)] := R(A)                */
OP_SETUPVAL,/*  A B UpValue[B] := R(A)              */
OP_SETTABLE,/*  A B C   R(A)[RK(B)] := RK(C)                */
OP_NEWTABLE,/*  A B C   R(A) := {} (size = B,C)             */
OP_SELF,/*  A B C   R(A+1) := R(B); R(A) := R(B)[RK(C)]     */
OP_ADD,/* A B C   R(A) := RK(B) + RK(C)                 */
OP_SUB,/*   A B C   R(A) := RK(B) - RK(C)               */
OP_MUL,/*   A B C   R(A) := RK(B) * RK(C)               */
OP_DIV,/*   A B C   R(A) := RK(B) / RK(C)               */
OP_MOD,/*   A B C   R(A) := RK(B) % RK(C)               */
OP_POW,/*   A B C   R(A) := RK(B) ^ RK(C)               */
OP_UNM,/*   A B R(A) := -R(B)                   */
OP_NOT,/*   A B R(A) := not R(B)                */
OP_LEN,/*   A B R(A) := length of R(B)              */
OP_CONCAT,/*    A B C   R(A) := R(B).. ... ..R(C)           */
OP_JMP,/*   sBx pc+=sBx                 */
OP_EQ,/*    A B C   if ((RK(B) == RK(C)) ~= A) then pc++        */
OP_LT,/*    A B C   if ((RK(B) <  RK(C)) ~= A) then pc++        */
OP_LE,/*    A B C   if ((RK(B) <= RK(C)) ~= A) then pc++        */
OP_TEST,/*  A C if not (R(A) <=> C) then pc++           */
OP_TESTSET,/*   A B C   if (R(B) <=> C) then R(A) := R(B) else pc++ */
OP_CALL,/*    A B C   R(A), ... ,R(A+C-2) := R(A)(R(A+1), ... ,R(A+B-1)) */
OP_TAILCALL,/*  A B C   return R(A)(R(A+1), ... ,R(A+B-1))      */
OP_RETURN,/*    A B return R(A), ... ,R(A+B-2)  (see note)  */
OP_FORLOOP,/*   A sBx   R(A)+=R(A+2); if R(A) <?= R(A+1) then { pc+=sBx; R(A+3)=R(A) }*/
OP_FORPREP,/*   A sBx   R(A)-=R(A+2); pc+=sBx               */
OP_TFORLOOP,/*  A C R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2)); if R(A+3) ~= nil then R(A+2)=R(A+3) else pc++   */
OP_SETLIST,/*   A B C   R(A)[(C-1)*FPF+i] := R(A+i), 1 <= i <= B    */
OP_CLOSE,/* A   close all variables in the stack up to (>=) R(A)*/
OP_CLOSURE,/*   A Bx    R(A) := closure(KPROTO[Bx], R(A), ... ,R(A+n))  */
    '''

    op_source = '''
/*
** $Id: lopcodes.c,v 1.37.1.1 2007/12/27 13:02:25 roberto Exp $
** See Copyright Notice in lua.h
*/


#define lopcodes_c
#define LUA_CORE


#include "lopcodes.h"


/* ORDER OP */

const char *const luaP_opnames[NUM_OPCODES+1] = {
%s
  "VARARG",
  NULL
};


#define opmode(t,a,b,c,m) (((t)<<7) | ((a)<<6) | ((b)<<4) | ((c)<<2) | (m))

const lu_byte luaP_opmodes[NUM_OPCODES] = {
/*       T  A    B       C     mode        opcode   */
%s
 opmode(0, 1, OpArgU, OpArgN, iABC)        /* OP_VARARG */
};

    '''

    opnames = '''
  "MOVE",
  "LOADK",
  "LOADBOOL",
  "LOADNIL",
  "GETUPVAL",
  "GETGLOBAL",
  "GETTABLE",
  "SETGLOBAL",
  "SETUPVAL",
  "SETTABLE",
  "NEWTABLE",
  "SELF",
  "ADD",
  "SUB",
  "MUL",
  "DIV",
  "MOD",
  "POW",
  "UNM",
  "NOT",
  "LEN",
  "CONCAT",
  "JMP",
  "EQ",
  "LT",
  "LE",
  "TEST",
  "TESTSET",
  "CALL",
  "TAILCALL",
  "RETURN",
  "FORLOOP",
  "FORPREP",
  "TFORLOOP",
  "SETLIST",
  "CLOSE",
  "CLOSURE",
    '''

    opmodes = '''
 opmode(0, 1, OpArgR, OpArgN, iABC),        /* OP_MOVE */
 opmode(0, 1, OpArgK, OpArgN, iABx),        /* OP_LOADK */
 opmode(0, 1, OpArgU, OpArgU, iABC),        /* OP_LOADBOOL */
 opmode(0, 1, OpArgR, OpArgN, iABC),        /* OP_LOADNIL */
 opmode(0, 1, OpArgU, OpArgN, iABC),        /* OP_GETUPVAL */
 opmode(0, 1, OpArgK, OpArgN, iABx),        /* OP_GETGLOBAL */
 opmode(0, 1, OpArgR, OpArgK, iABC),        /* OP_GETTABLE */
 opmode(0, 0, OpArgK, OpArgN, iABx),        /* OP_SETGLOBAL */
 opmode(0, 0, OpArgU, OpArgN, iABC),        /* OP_SETUPVAL */
 opmode(0, 0, OpArgK, OpArgK, iABC),        /* OP_SETTABLE */
 opmode(0, 1, OpArgU, OpArgU, iABC),        /* OP_NEWTABLE */
 opmode(0, 1, OpArgR, OpArgK, iABC),        /* OP_SELF */
 opmode(0, 1, OpArgK, OpArgK, iABC),        /* OP_ADD */
 opmode(0, 1, OpArgK, OpArgK, iABC),        /* OP_SUB */
 opmode(0, 1, OpArgK, OpArgK, iABC),        /* OP_MUL */
 opmode(0, 1, OpArgK, OpArgK, iABC),        /* OP_DIV */
 opmode(0, 1, OpArgK, OpArgK, iABC),        /* OP_MOD */
 opmode(0, 1, OpArgK, OpArgK, iABC),        /* OP_POW */
 opmode(0, 1, OpArgR, OpArgN, iABC),        /* OP_UNM */
 opmode(0, 1, OpArgR, OpArgN, iABC),        /* OP_NOT */
 opmode(0, 1, OpArgR, OpArgN, iABC),        /* OP_LEN */
 opmode(0, 1, OpArgR, OpArgR, iABC),        /* OP_CONCAT */
 opmode(0, 0, OpArgR, OpArgN, iAsBx),       /* OP_JMP */
 opmode(1, 0, OpArgK, OpArgK, iABC),        /* OP_EQ */
 opmode(1, 0, OpArgK, OpArgK, iABC),        /* OP_LT */
 opmode(1, 0, OpArgK, OpArgK, iABC),        /* OP_LE */
 opmode(1, 1, OpArgR, OpArgU, iABC),        /* OP_TEST */
 opmode(1, 1, OpArgR, OpArgU, iABC),        /* OP_TESTSET */
 opmode(0, 1, OpArgU, OpArgU, iABC),        /* OP_CALL */
 opmode(0, 1, OpArgU, OpArgU, iABC),        /* OP_TAILCALL */
 opmode(0, 0, OpArgU, OpArgN, iABC),        /* OP_RETURN */
 opmode(0, 1, OpArgR, OpArgN, iAsBx),       /* OP_FORLOOP */
 opmode(0, 1, OpArgR, OpArgN, iAsBx),       /* OP_FORPREP */
 opmode(1, 0, OpArgN, OpArgU, iABC),        /* OP_TFORLOOP */
 opmode(0, 0, OpArgU, OpArgU, iABC),        /* OP_SETLIST */
 opmode(0, 0, OpArgN, OpArgN, iABC),        /* OP_CLOSE */
 opmode(0, 1, OpArgU, OpArgN, iABx),        /* OP_CLOSURE */
    '''

    opmodes = opmodes.split('\n')
    opmodes.pop(len(opmodes)-1)
    opmodes.pop(0)


    enum = enum.split('\n')
    enum.pop(len(enum)-1)
    enum.pop(0)

    opnames = opnames.split('\n')
    opnames.pop(len(opnames)-1)
    opnames.pop(0)

    opmodes_mix = list(opmodes)
    enum_mix    = list(enum)
    opnames_mix = list(opnames)
    if mix:
        arr = np.random.permutation(len(opmodes))
        k = 0
        for i in arr:
            opmodes_mix[k] = opmodes[i]
            enum_mix[k]    = enum[i]
            opnames_mix[k] = opnames[i]
            k = k + 1

    header = op_header % ('\n'.join(enum_mix))
    source = op_source % ('\n'.join(opnames_mix), '\n'.join(opmodes_mix))

    print(header)
    print(source)

    if not dryrun:
        dir = os.path.dirname(os.path.abspath(__file__))
        sourcefile = os.path.join(dir, 'src/lopcodes.c')
        headerfile = os.path.join(dir, 'src/lopcodes2.h')
        with open(headerfile, 'wb') as f:
            f.write(header)
        with open(sourcefile, 'wb') as f:
            f.write(source)


if __name__ == '__main__':
    parser = ArgumentParser(description="Mix Lua op table.")
    parser.add_argument('--revert', dest='revert', action='store_true', default=False, help='Use Lua default op')
    parser.add_argument('--dryrun', dest='dryrun', action='store_true', default=False, help='Dont modify lua files')
    (args, unknown) = parser.parse_known_args()
    if len(unknown) > 0:
        print("unknown arguments: %s" % unknown)
        parser.print_help()

    main(not args.revert, args.dryrun)

    dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dir)
    print(bcolors.HEADER + 'compile lua' + bcolors.ENDC)
    run('make clean')
    run('make macosx')

    print(bcolors.HEADER + 'test luac' + bcolors.ENDC)
    print(bcolors.HEADER + '>generate love.luac' + bcolors.ENDC)
    run('./src/luac -o love.luac love.lua')

    print(bcolors.HEADER + '>load luac' + bcolors.ENDC)
    run('./src/lua love.luac')
