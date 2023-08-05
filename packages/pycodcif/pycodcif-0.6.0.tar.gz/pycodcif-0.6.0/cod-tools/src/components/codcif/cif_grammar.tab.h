/* A Bison parser, made by GNU Bison 2.5.  */

/* Bison interface for Yacc-like parsers in C
   
      Copyright (C) 1984, 1989-1990, 2000-2011 Free Software Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* "%code requires" blocks.  */

/* Line 2068 of yacc.c  */
#line 35 "cif_grammar.y"

    #include <cif_compiler.h>



/* Line 2068 of yacc.c  */
#line 44 "y.tab.h"

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     _DATA_ = 258,
     _SAVE_HEAD = 259,
     _SAVE_FOOT = 260,
     _TAG = 261,
     _LOOP_ = 262,
     _DQSTRING = 263,
     _SQSTRING = 264,
     _UQSTRING = 265,
     _TEXT_FIELD = 266,
     _INTEGER_CONST = 267,
     _REAL_CONST = 268
   };
#endif
/* Tokens.  */
#define _DATA_ 258
#define _SAVE_HEAD 259
#define _SAVE_FOOT 260
#define _TAG 261
#define _LOOP_ 262
#define _DQSTRING 263
#define _SQSTRING 264
#define _UQSTRING 265
#define _TEXT_FIELD 266
#define _INTEGER_CONST 267
#define _REAL_CONST 268




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 2068 of yacc.c  */
#line 39 "cif_grammar.y"

    char *s;
    typed_value *typed_value;



/* Line 2068 of yacc.c  */
#line 94 "y.tab.h"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE ciflval;


