/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

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

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "3.0.4"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1


/* Substitute the variable and function names.  */
#define yyparse         pmatchparse
#define yylex           pmatchlex
#define yyerror         pmatcherror
#define yydebug         pmatchdebug
#define yynerrs         pmatchnerrs

#define yylval          pmatchlval
#define yychar          pmatchchar

/* Copy the first part of user declarations.  */
#line 1 "pmatch_parse.yy" /* yacc.c:339  */

// Copyright (c) 2016 University of Helsinki
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 3 of the License, or (at your option) any later version.
// See the file COPYING included with this distribution for more
// information.

#define YYDEBUG 0

#include <stdio.h>
#include <assert.h>
#include <iostream>
#include <sstream>
    
#include "HfstTransducer.h"
#include "HfstInputStream.h"
#include "HfstXeroxRules.h"
    
#include "pmatch_utils.h"
    using namespace hfst;
    using namespace hfst::pmatch;
    using namespace hfst::xeroxRules;

    extern int pmatcherror(const char * text);
    extern int pmatchlex();
    extern int pmatchlineno;

    

#line 107 "pmatch_parse.cc" /* yacc.c:339  */

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 1
#endif

/* In a future release of Bison, this section will be replaced
   by #include "y.tab.h".  */
#ifndef YY_PMATCH_PMATCH_PARSE_HH_INCLUDED
# define YY_PMATCH_PMATCH_PARSE_HH_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int pmatchdebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    END_OF_WEIGHTED_EXPRESSION = 258,
    WEIGHT = 259,
    CHARACTER_RANGE = 260,
    CROSS_PRODUCT = 261,
    COMPOSITION = 262,
    LENIENT_COMPOSITION = 263,
    INTERSECTION = 264,
    MERGE_RIGHT_ARROW = 265,
    MERGE_LEFT_ARROW = 266,
    CENTER_MARKER = 267,
    MARKUP_MARKER = 268,
    SHUFFLE = 269,
    BEFORE = 270,
    AFTER = 271,
    LEFT_ARROW = 272,
    RIGHT_ARROW = 273,
    LEFT_RIGHT_ARROW = 274,
    LEFT_RESTRICTION = 275,
    REPLACE_RIGHT = 276,
    REPLACE_LEFT = 277,
    OPTIONAL_REPLACE_RIGHT = 278,
    OPTIONAL_REPLACE_LEFT = 279,
    REPLACE_LEFT_RIGHT = 280,
    OPTIONAL_REPLACE_LEFT_RIGHT = 281,
    RTL_LONGEST_MATCH = 282,
    RTL_SHORTEST_MATCH = 283,
    LTR_LONGEST_MATCH = 284,
    LTR_SHORTEST_MATCH = 285,
    REPLACE_CONTEXT_UU = 286,
    REPLACE_CONTEXT_LU = 287,
    REPLACE_CONTEXT_UL = 288,
    REPLACE_CONTEXT_LL = 289,
    UNION = 290,
    MINUS = 291,
    UPPER_MINUS = 292,
    LOWER_MINUS = 293,
    UPPER_PRIORITY_UNION = 294,
    LOWER_PRIORITY_UNION = 295,
    IGNORING = 296,
    IGNORE_INTERNALLY = 297,
    LEFT_QUOTIENT = 298,
    COMMA = 299,
    COMMACOMMA = 300,
    SUBSTITUTE_LEFT = 301,
    TERM_COMPLEMENT = 302,
    COMPLEMENT = 303,
    CONTAINMENT = 304,
    CONTAINMENT_ONCE = 305,
    CONTAINMENT_OPT = 306,
    STAR = 307,
    PLUS = 308,
    REVERSE = 309,
    INVERT = 310,
    UPPER_PROJECT = 311,
    LOWER_PROJECT = 312,
    READ_BIN = 313,
    READ_TEXT = 314,
    READ_SPACED = 315,
    READ_PROLOG = 316,
    READ_RE = 317,
    READ_VEC = 318,
    READ_LEXC = 319,
    CATENATE_N_TO_K = 320,
    CATENATE_N = 321,
    CATENATE_N_PLUS = 322,
    CATENATE_N_MINUS = 323,
    LEFT_BRACKET = 324,
    RIGHT_BRACKET = 325,
    LEFT_PARENTHESIS = 326,
    RIGHT_PARENTHESIS = 327,
    LEFT_BRACKET_DOTTED = 328,
    RIGHT_BRACKET_DOTTED = 329,
    PAIR_SEPARATOR = 330,
    PAIR_SEPARATOR_SOLE = 331,
    PAIR_SEPARATOR_WO_RIGHT = 332,
    PAIR_SEPARATOR_WO_LEFT = 333,
    EPSILON_TOKEN = 334,
    ANY_TOKEN = 335,
    BOUNDARY_MARKER = 336,
    LEXER_ERROR = 337,
    SYMBOL = 338,
    SYMBOL_WITH_LEFT_PAREN = 339,
    QUOTED_LITERAL = 340,
    CURLY_LITERAL = 341,
    ALPHA = 342,
    LOWERALPHA = 343,
    UPPERALPHA = 344,
    NUM = 345,
    PUNCT = 346,
    WHITESPACE = 347,
    VARIABLE_NAME = 348,
    DEFINE = 349,
    SET_VARIABLE = 350,
    LIT_LEFT = 351,
    INS_LEFT = 352,
    REGEX = 353,
    DEFINS = 354,
    DEFINED_LIST = 355,
    CAP_LEFT = 356,
    OPTCAP_LEFT = 357,
    OPT_TOLOWER_LEFT = 358,
    TOLOWER_LEFT = 359,
    OPT_TOUPPER_LEFT = 360,
    TOUPPER_LEFT = 361,
    ANY_CASE_LEFT = 362,
    IMPLODE_LEFT = 363,
    EXPLODE_LEFT = 364,
    DEFINE_LEFT = 365,
    ENDTAG_LEFT = 366,
    LIKE_LEFT = 367,
    UNLIKE_LEFT = 368,
    LC_LEFT = 369,
    RC_LEFT = 370,
    NLC_LEFT = 371,
    NRC_LEFT = 372,
    OR_LEFT = 373,
    AND_LEFT = 374,
    TAG_LEFT = 375,
    LST_LEFT = 376,
    EXC_LEFT = 377,
    INTERPOLATE_LEFT = 378,
    SIGMA_LEFT = 379,
    COUNTER_LEFT = 380
  };
#endif
/* Tokens.  */
#define END_OF_WEIGHTED_EXPRESSION 258
#define WEIGHT 259
#define CHARACTER_RANGE 260
#define CROSS_PRODUCT 261
#define COMPOSITION 262
#define LENIENT_COMPOSITION 263
#define INTERSECTION 264
#define MERGE_RIGHT_ARROW 265
#define MERGE_LEFT_ARROW 266
#define CENTER_MARKER 267
#define MARKUP_MARKER 268
#define SHUFFLE 269
#define BEFORE 270
#define AFTER 271
#define LEFT_ARROW 272
#define RIGHT_ARROW 273
#define LEFT_RIGHT_ARROW 274
#define LEFT_RESTRICTION 275
#define REPLACE_RIGHT 276
#define REPLACE_LEFT 277
#define OPTIONAL_REPLACE_RIGHT 278
#define OPTIONAL_REPLACE_LEFT 279
#define REPLACE_LEFT_RIGHT 280
#define OPTIONAL_REPLACE_LEFT_RIGHT 281
#define RTL_LONGEST_MATCH 282
#define RTL_SHORTEST_MATCH 283
#define LTR_LONGEST_MATCH 284
#define LTR_SHORTEST_MATCH 285
#define REPLACE_CONTEXT_UU 286
#define REPLACE_CONTEXT_LU 287
#define REPLACE_CONTEXT_UL 288
#define REPLACE_CONTEXT_LL 289
#define UNION 290
#define MINUS 291
#define UPPER_MINUS 292
#define LOWER_MINUS 293
#define UPPER_PRIORITY_UNION 294
#define LOWER_PRIORITY_UNION 295
#define IGNORING 296
#define IGNORE_INTERNALLY 297
#define LEFT_QUOTIENT 298
#define COMMA 299
#define COMMACOMMA 300
#define SUBSTITUTE_LEFT 301
#define TERM_COMPLEMENT 302
#define COMPLEMENT 303
#define CONTAINMENT 304
#define CONTAINMENT_ONCE 305
#define CONTAINMENT_OPT 306
#define STAR 307
#define PLUS 308
#define REVERSE 309
#define INVERT 310
#define UPPER_PROJECT 311
#define LOWER_PROJECT 312
#define READ_BIN 313
#define READ_TEXT 314
#define READ_SPACED 315
#define READ_PROLOG 316
#define READ_RE 317
#define READ_VEC 318
#define READ_LEXC 319
#define CATENATE_N_TO_K 320
#define CATENATE_N 321
#define CATENATE_N_PLUS 322
#define CATENATE_N_MINUS 323
#define LEFT_BRACKET 324
#define RIGHT_BRACKET 325
#define LEFT_PARENTHESIS 326
#define RIGHT_PARENTHESIS 327
#define LEFT_BRACKET_DOTTED 328
#define RIGHT_BRACKET_DOTTED 329
#define PAIR_SEPARATOR 330
#define PAIR_SEPARATOR_SOLE 331
#define PAIR_SEPARATOR_WO_RIGHT 332
#define PAIR_SEPARATOR_WO_LEFT 333
#define EPSILON_TOKEN 334
#define ANY_TOKEN 335
#define BOUNDARY_MARKER 336
#define LEXER_ERROR 337
#define SYMBOL 338
#define SYMBOL_WITH_LEFT_PAREN 339
#define QUOTED_LITERAL 340
#define CURLY_LITERAL 341
#define ALPHA 342
#define LOWERALPHA 343
#define UPPERALPHA 344
#define NUM 345
#define PUNCT 346
#define WHITESPACE 347
#define VARIABLE_NAME 348
#define DEFINE 349
#define SET_VARIABLE 350
#define LIT_LEFT 351
#define INS_LEFT 352
#define REGEX 353
#define DEFINS 354
#define DEFINED_LIST 355
#define CAP_LEFT 356
#define OPTCAP_LEFT 357
#define OPT_TOLOWER_LEFT 358
#define TOLOWER_LEFT 359
#define OPT_TOUPPER_LEFT 360
#define TOUPPER_LEFT 361
#define ANY_CASE_LEFT 362
#define IMPLODE_LEFT 363
#define EXPLODE_LEFT 364
#define DEFINE_LEFT 365
#define ENDTAG_LEFT 366
#define LIKE_LEFT 367
#define UNLIKE_LEFT 368
#define LC_LEFT 369
#define RC_LEFT 370
#define NLC_LEFT 371
#define NRC_LEFT 372
#define OR_LEFT 373
#define AND_LEFT 374
#define TAG_LEFT 375
#define LST_LEFT 376
#define EXC_LEFT 377
#define INTERPOLATE_LEFT 378
#define SIGMA_LEFT 379
#define COUNTER_LEFT 380

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 36 "pmatch_parse.yy" /* yacc.c:355  */

         int value;
         int* values;
         double weight;
         char* label;
         hfst::pmatch::PmatchObject* pmatchObject;
         std::pair<std::string, hfst::pmatch::PmatchObject*>* pmatchDefinition;
         std::vector<hfst::pmatch::PmatchObject *>* pmatchObject_vector;
         std::vector<std::string>* string_vector;

         hfst::pmatch::PmatchParallelRulesContainer * replaceRules;
         hfst::pmatch::PmatchReplaceRuleContainer * replaceRule;
         hfst::pmatch::PmatchMappingPairsContainer * mappings;
         hfst::pmatch::PmatchContextsContainer * parallelContexts;
         hfst::pmatch::PmatchObjectPair * restrictionContext;
         hfst::pmatch::MappingPairVector * restrictionContexts;
         hfst::xeroxRules::ReplaceType replType;
         hfst::xeroxRules::ReplaceArrow replaceArrow;
     

#line 418 "pmatch_parse.cc" /* yacc.c:355  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE pmatchlval;

int pmatchparse (void);

#endif /* !YY_PMATCH_PMATCH_PARSE_HH_INCLUDED  */

/* Copy the second part of user declarations.  */

#line 435 "pmatch_parse.cc" /* yacc.c:358  */

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif

#ifndef YY_ATTRIBUTE
# if (defined __GNUC__                                               \
      && (2 < __GNUC__ || (__GNUC__ == 2 && 96 <= __GNUC_MINOR__)))  \
     || defined __SUNPRO_C && 0x5110 <= __SUNPRO_C
#  define YY_ATTRIBUTE(Spec) __attribute__(Spec)
# else
#  define YY_ATTRIBUTE(Spec) /* empty */
# endif
#endif

#ifndef YY_ATTRIBUTE_PURE
# define YY_ATTRIBUTE_PURE   YY_ATTRIBUTE ((__pure__))
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# define YY_ATTRIBUTE_UNUSED YY_ATTRIBUTE ((__unused__))
#endif

#if !defined _Noreturn \
     && (!defined __STDC_VERSION__ || __STDC_VERSION__ < 201112)
# if defined _MSC_VER && 1200 <= _MSC_VER
#  define _Noreturn __declspec (noreturn)
# else
#  define _Noreturn YY_ATTRIBUTE ((__noreturn__))
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(E) ((void) (E))
#else
# define YYUSE(E) /* empty */
#endif

#if defined __GNUC__ && 407 <= __GNUC__ * 100 + __GNUC_MINOR__
/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN \
    _Pragma ("GCC diagnostic push") \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")\
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# define YY_IGNORE_MAYBE_UNINITIALIZED_END \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif


#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYSIZE_T yynewbytes;                                            \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / sizeof (*yyptr);                          \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, (Count) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYSIZE_T yyi;                         \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  2
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   1308

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  126
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  46
/* YYNRULES -- Number of rules.  */
#define YYNRULES  193
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  343

/* YYTRANSLATE[YYX] -- Symbol number corresponding to YYX as returned
   by yylex, with out-of-bounds checking.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   380

#define YYTRANSLATE(YYX)                                                \
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, without out-of-bounds checking.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,    99,   100,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,   120,   121,   122,   123,   124,
     125
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   109,   109,   110,   127,   131,   136,   142,   147,   154,
     158,   165,   172,   173,   174,   175,   176,   178,   188,   189,
     190,   191,   192,   193,   194,   197,   199,   201,   205,   206,
     208,   215,   219,   221,   225,   232,   234,   237,   240,   245,
     248,   250,   252,   254,   258,   262,   265,   271,   272,   273,
     274,   278,   279,   280,   281,   284,   285,   286,   287,   288,
     289,   290,   291,   294,   295,   296,   297,   299,   300,   301,
     302,   304,   309,   316,   317,   318,   319,   321,   322,   323,
     324,   325,   326,   327,   328,   330,   331,   333,   334,   335,
     336,   338,   339,   340,   341,   342,   344,   345,   346,   347,
     348,   349,   350,   351,   355,   359,   363,   370,   371,   373,
     374,   375,   376,   377,   378,   383,   390,   391,   392,   393,
     394,   399,   400,   401,   402,   404,   405,   406,   407,   408,
     409,   410,   411,   412,   413,   414,   415,   416,   417,   418,
     420,   431,   442,   453,   464,   475,   486,   497,   498,   499,
     500,   501,   502,   503,   504,   505,   506,   513,   524,   530,
     536,   538,   546,   563,   565,   566,   568,   587,   598,   609,
     620,   633,   636,   641,   659,   663,   667,   689,   693,   714,
     715,   716,   719,   720,   721,   722,   724,   742,   758,   761,
     766,   771,   776,   781
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 1
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "END_OF_WEIGHTED_EXPRESSION", "WEIGHT",
  "CHARACTER_RANGE", "CROSS_PRODUCT", "COMPOSITION", "LENIENT_COMPOSITION",
  "INTERSECTION", "MERGE_RIGHT_ARROW", "MERGE_LEFT_ARROW", "CENTER_MARKER",
  "MARKUP_MARKER", "SHUFFLE", "BEFORE", "AFTER", "LEFT_ARROW",
  "RIGHT_ARROW", "LEFT_RIGHT_ARROW", "LEFT_RESTRICTION", "REPLACE_RIGHT",
  "REPLACE_LEFT", "OPTIONAL_REPLACE_RIGHT", "OPTIONAL_REPLACE_LEFT",
  "REPLACE_LEFT_RIGHT", "OPTIONAL_REPLACE_LEFT_RIGHT", "RTL_LONGEST_MATCH",
  "RTL_SHORTEST_MATCH", "LTR_LONGEST_MATCH", "LTR_SHORTEST_MATCH",
  "REPLACE_CONTEXT_UU", "REPLACE_CONTEXT_LU", "REPLACE_CONTEXT_UL",
  "REPLACE_CONTEXT_LL", "UNION", "MINUS", "UPPER_MINUS", "LOWER_MINUS",
  "UPPER_PRIORITY_UNION", "LOWER_PRIORITY_UNION", "IGNORING",
  "IGNORE_INTERNALLY", "LEFT_QUOTIENT", "COMMA", "COMMACOMMA",
  "SUBSTITUTE_LEFT", "TERM_COMPLEMENT", "COMPLEMENT", "CONTAINMENT",
  "CONTAINMENT_ONCE", "CONTAINMENT_OPT", "STAR", "PLUS", "REVERSE",
  "INVERT", "UPPER_PROJECT", "LOWER_PROJECT", "READ_BIN", "READ_TEXT",
  "READ_SPACED", "READ_PROLOG", "READ_RE", "READ_VEC", "READ_LEXC",
  "CATENATE_N_TO_K", "CATENATE_N", "CATENATE_N_PLUS", "CATENATE_N_MINUS",
  "LEFT_BRACKET", "RIGHT_BRACKET", "LEFT_PARENTHESIS", "RIGHT_PARENTHESIS",
  "LEFT_BRACKET_DOTTED", "RIGHT_BRACKET_DOTTED", "PAIR_SEPARATOR",
  "PAIR_SEPARATOR_SOLE", "PAIR_SEPARATOR_WO_RIGHT",
  "PAIR_SEPARATOR_WO_LEFT", "EPSILON_TOKEN", "ANY_TOKEN",
  "BOUNDARY_MARKER", "LEXER_ERROR", "SYMBOL", "SYMBOL_WITH_LEFT_PAREN",
  "QUOTED_LITERAL", "CURLY_LITERAL", "ALPHA", "LOWERALPHA", "UPPERALPHA",
  "NUM", "PUNCT", "WHITESPACE", "VARIABLE_NAME", "DEFINE", "SET_VARIABLE",
  "LIT_LEFT", "INS_LEFT", "REGEX", "DEFINS", "DEFINED_LIST", "CAP_LEFT",
  "OPTCAP_LEFT", "OPT_TOLOWER_LEFT", "TOLOWER_LEFT", "OPT_TOUPPER_LEFT",
  "TOUPPER_LEFT", "ANY_CASE_LEFT", "IMPLODE_LEFT", "EXPLODE_LEFT",
  "DEFINE_LEFT", "ENDTAG_LEFT", "LIKE_LEFT", "UNLIKE_LEFT", "LC_LEFT",
  "RC_LEFT", "NLC_LEFT", "NRC_LEFT", "OR_LEFT", "AND_LEFT", "TAG_LEFT",
  "LST_LEFT", "EXC_LEFT", "INTERPOLATE_LEFT", "SIGMA_LEFT", "COUNTER_LEFT",
  "$accept", "PMATCH", "DEFINITION", "ARGLIST", "EXPRESSION1",
  "EXPRESSION2", "EXPRESSION3", "PARALLEL_RULES", "RULE",
  "MAPPINGPAIR_VECTOR", "MAPPINGPAIR", "CONTEXTS_WITH_MARK",
  "CONTEXTS_VECTOR", "CONTEXT", "CONTEXT_MARK", "REPLACE_ARROW",
  "EXPRESSION4", "EXPRESSION5", "RESTR_CONTEXTS", "RESTR_CONTEXT",
  "EXPRESSION6", "EXPRESSION7", "EXPRESSION8", "EXPRESSION9",
  "EXPRESSION10", "EXPRESSION11", "EXPRESSION12", "EXPRESSION13",
  "EXPLODE", "IMPLODE", "CONCATENATED_STRING_LIST", "FUNCALL",
  "FUNCALL_ARGLIST", "INSERTION", "LIKE", "ENDTAG", "READ_FROM",
  "CONTEXT_CONDITION", "PMATCH_CONTEXT", "PMATCH_OR_CONTEXT",
  "PMATCH_AND_CONTEXT", "PMATCH_CONTEXTS", "PMATCH_RIGHT_CONTEXT",
  "PMATCH_NEGATIVE_RIGHT_CONTEXT", "PMATCH_LEFT_CONTEXT",
  "PMATCH_NEGATIVE_LEFT_CONTEXT", YY_NULLPTR
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[NUM] -- (External) token number corresponding to the
   (internal) symbol number NUM (which must be that of a token).  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323,   324,
     325,   326,   327,   328,   329,   330,   331,   332,   333,   334,
     335,   336,   337,   338,   339,   340,   341,   342,   343,   344,
     345,   346,   347,   348,   349,   350,   351,   352,   353,   354,
     355,   356,   357,   358,   359,   360,   361,   362,   363,   364,
     365,   366,   367,   368,   369,   370,   371,   372,   373,   374,
     375,   376,   377,   378,   379,   380
};
# endif

#define YYPACT_NINF -162

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-162)))

#define YYTABLE_NINF -1

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int16 yypact[] =
{
    -162,    22,  -162,  -162,   -60,   -57,   210,   -46,   -41,  -162,
     210,   -35,   -66,  -162,   -36,   994,   926,   926,   926,   926,
    -162,  -162,  -162,  -162,  -162,  -162,   210,   210,   298,  -162,
     210,  -162,  -162,  -162,  -162,   210,  -162,  -162,  -162,  -162,
    -162,  -162,  -162,  -162,   -40,   -32,   210,   210,   210,   210,
     210,   210,   210,   -16,   -16,   210,    99,   -35,   -35,   210,
     210,   210,   210,    17,    17,   210,   210,   210,   210,   -13,
    -162,    46,   222,    33,  -162,    40,  -162,   122,  -162,   430,
     853,   101,  -162,  -162,   285,     8,  -162,  -162,  -162,  -162,
    -162,  -162,  -162,  -162,  -162,  -162,  -162,  -162,  -162,  -162,
    -162,  -162,   210,   210,  -162,    11,    37,    14,  -162,  -162,
     677,     8,  -162,  -162,  -162,  -162,    81,   157,   222,   406,
     831,  1126,    18,    26,    31,    58,    69,   163,   170,   435,
    1114,  1120,    60,    42,    43,   215,    47,    52,    80,    82,
     919,  1132,  1138,  1144,    74,    87,    90,  1155,  1161,   100,
    1167,   103,  -162,   677,   677,   677,   677,   677,  -162,  -162,
    -162,  -162,  -162,  -162,  -162,  -162,  -162,   413,   677,  -162,
    -162,  -162,  -162,   677,  -162,   501,   853,   853,   853,   853,
     853,   765,   853,   853,   853,   853,   853,   853,   853,   853,
     853,   853,   853,  -162,  -162,  -162,  -162,  -162,  -162,  -162,
    -162,  -162,  -162,  -162,   994,  -162,  -162,   -35,   -35,   210,
    1236,    59,  -162,   677,   222,   210,  -162,  -162,  -162,   107,
    -162,   112,  -162,   116,  -162,   125,  -162,   126,  -162,   127,
    -162,   128,  -162,   -16,  -162,  -162,  -162,  -162,  -162,   146,
     150,  -162,  -162,  -162,  -162,    17,  -162,  -162,  -162,  -162,
    -162,  -162,  -162,   222,   222,   222,   222,   222,   677,   589,
    1278,   222,  -162,  -162,   677,  1265,   173,  -162,  -162,  -162,
    -162,   853,    23,   853,   174,  -162,  1210,  1216,   853,   853,
     853,   853,   853,   853,  -162,  -162,  -162,     8,  -162,  -162,
    -162,   677,   113,   222,   677,  -162,   147,   148,   152,   155,
     156,   160,   161,  -162,  -162,  -162,  -162,   222,   222,  1160,
     677,   222,   677,   501,   853,   415,   765,   853,   853,  1246,
     165,   166,   222,  -162,  -162,  -162,  -162,  -162,  -162,  -162,
     222,   222,   222,  -162,   415,  -162,   415,   415,   677,  -162,
    -162,  1172,  -162
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       2,     0,     1,     6,     0,     0,     0,     0,     0,     3,
       0,    16,     0,   149,     0,     0,     0,     0,     0,     0,
     173,   174,   175,   176,   178,   177,     0,     0,     0,    27,
       0,   117,   121,   118,   157,   165,   116,   120,   127,   128,
     129,   130,   131,   132,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,    16,    16,     0,
       0,     0,     0,     0,     0,     0,     0,   165,     0,     0,
       9,     0,    18,    29,    31,    32,    35,    28,    63,    67,
      77,    85,    87,    91,    96,   107,   109,   122,   123,   124,
     125,   126,   155,   148,   156,   179,   180,   181,   182,   183,
     184,   185,     0,     0,     7,    14,    15,     0,     5,     4,
       0,   108,    92,    93,    94,    95,     0,     0,     0,     0,
      26,   164,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,   160,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,   188,     0,     0,     0,     0,     0,
       0,     0,    17,     0,     0,     0,     0,     0,    25,    55,
      61,    56,    62,    57,    58,    59,    60,     0,     0,    51,
      52,    53,    54,     0,    33,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,    86,
       0,     0,     0,    97,    98,    99,   100,   101,   102,   106,
     103,   104,   105,   113,     0,     8,    11,    16,    16,     0,
       0,   110,   112,     0,     0,   165,   162,   119,   166,     0,
     133,     0,   134,     0,   137,     0,   135,     0,   138,     0,
     136,     0,   139,     0,   159,   158,   147,   171,   172,   167,
     169,   192,   190,   193,   191,     0,   186,   187,   150,   151,
     152,   153,   154,    20,    19,    21,    22,    23,     0,     0,
      36,     0,    30,    34,    50,     0,    44,    45,    64,    65,
      66,    79,     0,    76,    68,    71,     0,     0,    78,    80,
      81,    82,    83,    84,    88,    89,    90,   111,    12,    13,
      10,     0,     0,    40,     0,   163,     0,     0,     0,     0,
       0,     0,     0,   161,   168,   170,   189,    39,    42,     0,
      38,    49,    48,     0,     0,    75,     0,    74,     0,     0,
       0,     0,    41,   140,   141,   144,   142,   145,   143,   146,
      43,    37,    47,    46,    69,    72,    73,    70,     0,   114,
     115,     0,    24
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -162,  -162,  -162,   -47,    -3,   -21,   -28,  -162,    71,  -162,
      68,  -162,  -162,   -65,  -162,  -117,  -162,    10,  -162,   -63,
    -161,   -78,  -162,   -42,    77,  -162,   -12,  -162,  -162,  -162,
     -50,  -162,   -49,  -162,  -162,  -162,  -162,  -162,   -48,  -162,
    -162,   -56,  -162,  -162,  -162,  -162
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,     1,     9,   107,    70,    71,    72,    73,    74,    75,
      76,   174,   266,   267,   175,   167,    77,    78,   274,   275,
      79,    80,    81,    82,    83,    84,    85,    86,    87,    88,
     133,    89,   122,    90,    91,    92,    93,    94,    95,    96,
      97,   145,    98,    99,   100,   101
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_uint16 yytable[] =
{
     119,   213,   189,   111,   134,   116,   117,   104,   146,   120,
     138,   139,   203,   108,   121,   144,   144,   109,   149,   272,
     276,   277,     2,    10,    11,   125,   126,   127,   128,   129,
     130,   131,   179,   110,   135,   314,    12,   102,   140,   141,
     142,   143,   103,   123,   147,   148,   121,   150,   105,   152,
     106,   124,   153,   154,   155,   207,   156,   157,   183,   184,
     185,   186,   187,   188,   153,   154,   155,   132,   156,   157,
     151,   169,   170,   171,   172,   153,   154,   155,   168,   156,
     157,   208,   210,   204,   173,     3,   209,   153,   154,   155,
     216,   156,   157,   112,   113,   114,   115,   294,   217,   205,
     206,   271,   219,   218,   233,   278,   279,   280,   281,   282,
     283,   189,   315,   221,   234,   235,     4,     5,   245,   237,
       6,     7,     8,   158,   238,   253,   254,   255,   256,   257,
     220,    59,    60,    61,    62,   158,   176,   177,   178,   260,
     261,   222,   190,   191,   192,   261,   158,   265,   284,   285,
     286,   211,   239,   334,   240,   276,   336,   337,   158,   246,
     288,   289,   247,   153,   154,   155,   295,   156,   157,   153,
     154,   155,   250,   156,   157,   252,   153,   154,   155,   292,
     156,   157,   136,   303,   137,   293,   268,   269,   270,   306,
     296,   213,   287,   189,   121,   297,   320,   144,   321,   298,
     189,   189,   189,   189,   189,   189,   290,   223,   299,   300,
     301,   302,   304,   294,   225,    13,   305,   313,   316,   323,
     324,   153,   154,   155,   325,   156,   157,   326,   327,   212,
     307,   309,   328,   329,   158,   224,   311,   339,   340,   262,
     158,   263,   226,   159,   160,   161,   162,   158,   333,   163,
     164,   165,   166,   335,     0,     0,    14,    15,    16,    17,
      18,    19,     0,   319,     0,     0,   322,     0,    20,    21,
      22,    23,    24,     0,    25,     0,     0,     0,     0,    26,
       0,    27,   331,    28,   332,   265,    29,   236,    30,    31,
      32,    33,   158,    34,    35,    36,    37,    38,    39,    40,
      41,    42,    43,    13,     0,     0,    44,    45,     0,     0,
     341,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
       0,    65,    66,    67,    68,    69,     0,   193,   194,   195,
     196,   197,   198,     0,     0,    15,    16,    17,    18,    19,
     199,   200,   201,   202,     0,     0,    20,    21,    22,    23,
      24,     0,    25,     0,     0,     0,     0,    26,     0,    27,
       0,    28,   118,     0,     0,     0,     0,    31,    32,    33,
       0,    34,    35,    36,    37,    38,    39,    40,    41,    42,
      43,     0,     0,     0,    44,    45,     0,     0,     0,    46,
      47,    48,    49,    50,    51,    52,    53,    54,    55,    56,
      57,    58,    59,    60,    61,    62,    63,    64,    13,    65,
      66,    67,    68,    69,   179,     0,   258,   159,   160,   161,
     162,     0,     0,   163,   164,   165,   166,     0,     0,   179,
       0,   153,   154,   155,     0,   156,   157,   180,   181,   182,
     183,   184,   185,   186,   187,   188,     0,     0,     0,     0,
      15,    16,    17,    18,    19,   183,   184,   185,   186,   187,
     188,    20,    21,    22,    23,    24,     0,    25,     0,   227,
     214,     0,    26,     0,    27,     0,   259,     0,     0,     0,
       0,     0,    31,    32,    33,     0,    34,    35,    36,    37,
      38,    39,    40,    41,    42,    43,    13,   228,     0,    44,
      45,     0,   158,   264,    46,    47,    48,    49,    50,    51,
      52,    53,    54,    55,    56,    57,    58,    59,    60,    61,
      62,    63,    64,     0,    65,    66,    67,    68,    69,     0,
       0,     0,     0,     0,     0,     0,     0,     0,    15,    16,
      17,    18,    19,     0,     0,     0,     0,     0,     0,    20,
      21,    22,    23,    24,     0,    25,     0,     0,     0,     0,
      26,     0,    27,     0,    28,     0,     0,     0,     0,     0,
      31,    32,    33,     0,    34,    35,    36,    37,    38,    39,
      40,    41,    42,    43,    13,     0,     0,    44,    45,     0,
       0,     0,    46,    47,    48,    49,    50,    51,    52,    53,
      54,    55,    56,    57,    58,    59,    60,    61,    62,    63,
      64,     0,    65,    66,    67,    68,    69,     0,     0,     0,
       0,     0,     0,     0,     0,     0,    15,    16,    17,    18,
      19,     0,     0,     0,     0,     0,     0,    20,    21,    22,
      23,    24,     0,    25,     0,     0,     0,     0,    26,     0,
      27,     0,    28,   308,     0,     0,     0,     0,    31,    32,
      33,     0,    34,    35,    36,    37,    38,    39,    40,    41,
      42,    43,    13,     0,     0,    44,    45,     0,     0,     0,
      46,    47,    48,    49,    50,    51,    52,    53,    54,    55,
      56,    57,    58,    59,    60,    61,    62,    63,    64,     0,
      65,    66,    67,    68,    69,     0,     0,     0,     0,     0,
       0,     0,     0,     0,    15,    16,    17,    18,    19,     0,
       0,     0,     0,     0,     0,    20,    21,    22,    23,    24,
       0,    25,     0,     0,     0,     0,    26,     0,    27,     0,
      28,     0,     0,     0,     0,     0,    31,    32,    33,     0,
      34,    35,    36,    37,    38,    39,    40,    41,    42,    43,
      13,     0,     0,    44,    45,     0,     0,   273,    46,    47,
      48,    49,    50,    51,    52,    53,    54,    55,    56,    57,
      58,    59,    60,    61,    62,    63,    64,     0,    65,    66,
      67,    68,    69,     0,     0,     0,     0,     0,     0,     0,
       0,     0,    15,    16,    17,    18,    19,     0,     0,     0,
       0,     0,     0,    20,    21,    22,    23,    24,     0,    25,
       0,     0,     0,     0,    26,     0,    27,   153,   154,   155,
       0,   156,   157,     0,    31,    32,    33,     0,    34,    35,
      36,    37,    38,    39,    40,    41,    42,    43,    13,     0,
       0,    44,    45,     0,     0,     0,    46,    47,    48,    49,
      50,    51,    52,    53,    54,    55,    56,    57,    58,    59,
      60,    61,    62,    63,    64,     0,    65,    66,    67,    68,
      69,     0,     0,     0,     0,     0,     0,     0,     0,     0,
      15,    16,    17,    18,    19,     0,     0,     0,   158,     0,
       0,    20,    21,    22,    23,    24,     0,    25,     0,     0,
       0,     0,    26,     0,    27,   153,   154,   155,     0,   156,
     157,    13,    31,    32,    33,     0,    34,    35,    36,    37,
      38,    39,    40,    41,    42,    43,     0,     0,     0,    44,
      45,     0,     0,     0,    46,    47,    48,    49,    50,    51,
      52,    53,    54,    55,    56,    57,    58,    59,    60,    61,
      62,    63,    64,    15,    65,    66,    67,    68,    69,     0,
       0,     0,     0,     0,    20,    21,    22,    23,    24,     0,
      25,   241,     0,     0,     0,    26,   158,    27,     0,    13,
       0,     0,     0,     0,     0,    31,    32,    33,     0,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,     0,
       0,     0,    44,    45,     0,     0,     0,    46,    47,    48,
      49,    50,    51,    52,    53,    54,    55,    56,    57,    58,
      59,    60,    61,    62,    63,    64,     0,    65,    66,    67,
      68,    69,    20,    21,    22,    23,    24,     0,    25,     0,
       0,     0,     0,    26,     0,    27,     0,     0,     0,     0,
       0,     0,     0,    31,    32,    33,     0,    34,    35,    36,
      37,    38,    39,    40,    41,    42,    43,     0,     0,     0,
      44,    45,     0,     0,     0,    46,    47,    48,    49,    50,
      51,    52,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,    63,    64,     0,    65,    66,    67,    68,    69,
     153,   154,   155,     0,   156,   157,   153,   154,   155,     0,
     156,   157,   153,   154,   155,     0,   156,   157,   153,   154,
     155,     0,   156,   157,   153,   154,   155,     0,   156,   157,
     153,   154,   155,     0,   156,   157,     0,     0,   229,     0,
       0,   153,   154,   155,   231,   156,   157,   153,   154,   155,
     215,   156,   157,   153,   154,   155,     0,   156,   157,     0,
       0,   159,   160,   161,   162,     0,   230,   163,   164,   165,
     166,   158,   232,   159,   160,   161,   162,   158,     0,   163,
     164,   165,   166,   158,   242,     0,     0,     0,     0,   158,
     243,     0,     0,     0,     0,   158,   244,     0,     0,   179,
       0,   158,   317,     0,     0,   179,     0,   248,   318,     0,
       0,     0,   158,   249,   330,     0,     0,     0,   158,   251,
       0,     0,   342,     0,   158,   183,   184,   185,   186,   187,
     188,   183,   184,   185,   186,   187,   188,   159,   160,   161,
     162,     0,     0,   163,   164,   165,   166,   159,   160,   161,
     162,     0,     0,   163,   164,   165,   166,   312,     0,     0,
     291,     0,     0,     0,     0,     0,   159,   160,   161,   162,
     338,   310,   163,   164,   165,   166,     0,     0,     0,   159,
     160,   161,   162,     0,     0,   163,   164,   165,   166
};

static const yytype_int16 yycheck[] =
{
      28,   118,    80,    15,    54,    26,    27,    10,    64,    30,
      57,    58,     4,    79,    35,    63,    64,    83,    67,   180,
     181,   182,     0,    83,    84,    46,    47,    48,    49,    50,
      51,    52,     9,    69,    55,    12,    93,    83,    59,    60,
      61,    62,    83,    83,    65,    66,    67,    68,    83,     3,
      85,    83,     6,     7,     8,    44,    10,    11,    35,    36,
      37,    38,    39,    40,     6,     7,     8,    83,    10,    11,
      83,    31,    32,    33,    34,     6,     7,     8,    45,    10,
      11,    44,   110,    75,    44,    63,    72,     6,     7,     8,
      72,    10,    11,    16,    17,    18,    19,   214,    72,   102,
     103,   179,    44,    72,    44,   183,   184,   185,   186,   187,
     188,   189,   273,    44,    72,    72,    94,    95,    44,    72,
      98,    99,   100,    77,    72,   153,   154,   155,   156,   157,
      72,   114,   115,   116,   117,    77,    14,    15,    16,   167,
     168,    72,    41,    42,    43,   173,    77,   175,   190,   191,
     192,    70,    72,   314,    72,   316,   317,   318,    77,    72,
     207,   208,    72,     6,     7,     8,   215,    10,    11,     6,
       7,     8,    72,    10,    11,    72,     6,     7,     8,   120,
      10,    11,    83,   233,    85,   213,   176,   177,   178,   245,
      83,   308,   204,   271,   215,    83,    83,   245,    85,    83,
     278,   279,   280,   281,   282,   283,   209,    44,    83,    83,
      83,    83,    66,   330,    44,     5,    66,    44,    44,    72,
      72,     6,     7,     8,    72,    10,    11,    72,    72,    72,
     258,   259,    72,    72,    77,    72,   264,    72,    72,   168,
      77,   173,    72,    21,    22,    23,    24,    77,   313,    27,
      28,    29,    30,   316,    -1,    -1,    46,    47,    48,    49,
      50,    51,    -1,   291,    -1,    -1,   294,    -1,    58,    59,
      60,    61,    62,    -1,    64,    -1,    -1,    -1,    -1,    69,
      -1,    71,   310,    73,   312,   313,    76,    72,    78,    79,
      80,    81,    77,    83,    84,    85,    86,    87,    88,    89,
      90,    91,    92,     5,    -1,    -1,    96,    97,    -1,    -1,
     338,   101,   102,   103,   104,   105,   106,   107,   108,   109,
     110,   111,   112,   113,   114,   115,   116,   117,   118,   119,
      -1,   121,   122,   123,   124,   125,    -1,    52,    53,    54,
      55,    56,    57,    -1,    -1,    47,    48,    49,    50,    51,
      65,    66,    67,    68,    -1,    -1,    58,    59,    60,    61,
      62,    -1,    64,    -1,    -1,    -1,    -1,    69,    -1,    71,
      -1,    73,    74,    -1,    -1,    -1,    -1,    79,    80,    81,
      -1,    83,    84,    85,    86,    87,    88,    89,    90,    91,
      92,    -1,    -1,    -1,    96,    97,    -1,    -1,    -1,   101,
     102,   103,   104,   105,   106,   107,   108,   109,   110,   111,
     112,   113,   114,   115,   116,   117,   118,   119,     5,   121,
     122,   123,   124,   125,     9,    -1,    13,    21,    22,    23,
      24,    -1,    -1,    27,    28,    29,    30,    -1,    -1,     9,
      -1,     6,     7,     8,    -1,    10,    11,    17,    18,    19,
      35,    36,    37,    38,    39,    40,    -1,    -1,    -1,    -1,
      47,    48,    49,    50,    51,    35,    36,    37,    38,    39,
      40,    58,    59,    60,    61,    62,    -1,    64,    -1,    44,
      74,    -1,    69,    -1,    71,    -1,    73,    -1,    -1,    -1,
      -1,    -1,    79,    80,    81,    -1,    83,    84,    85,    86,
      87,    88,    89,    90,    91,    92,     5,    72,    -1,    96,
      97,    -1,    77,    12,   101,   102,   103,   104,   105,   106,
     107,   108,   109,   110,   111,   112,   113,   114,   115,   116,
     117,   118,   119,    -1,   121,   122,   123,   124,   125,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    47,    48,
      49,    50,    51,    -1,    -1,    -1,    -1,    -1,    -1,    58,
      59,    60,    61,    62,    -1,    64,    -1,    -1,    -1,    -1,
      69,    -1,    71,    -1,    73,    -1,    -1,    -1,    -1,    -1,
      79,    80,    81,    -1,    83,    84,    85,    86,    87,    88,
      89,    90,    91,    92,     5,    -1,    -1,    96,    97,    -1,
      -1,    -1,   101,   102,   103,   104,   105,   106,   107,   108,
     109,   110,   111,   112,   113,   114,   115,   116,   117,   118,
     119,    -1,   121,   122,   123,   124,   125,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    47,    48,    49,    50,
      51,    -1,    -1,    -1,    -1,    -1,    -1,    58,    59,    60,
      61,    62,    -1,    64,    -1,    -1,    -1,    -1,    69,    -1,
      71,    -1,    73,    74,    -1,    -1,    -1,    -1,    79,    80,
      81,    -1,    83,    84,    85,    86,    87,    88,    89,    90,
      91,    92,     5,    -1,    -1,    96,    97,    -1,    -1,    -1,
     101,   102,   103,   104,   105,   106,   107,   108,   109,   110,
     111,   112,   113,   114,   115,   116,   117,   118,   119,    -1,
     121,   122,   123,   124,   125,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    47,    48,    49,    50,    51,    -1,
      -1,    -1,    -1,    -1,    -1,    58,    59,    60,    61,    62,
      -1,    64,    -1,    -1,    -1,    -1,    69,    -1,    71,    -1,
      73,    -1,    -1,    -1,    -1,    -1,    79,    80,    81,    -1,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
       5,    -1,    -1,    96,    97,    -1,    -1,    12,   101,   102,
     103,   104,   105,   106,   107,   108,   109,   110,   111,   112,
     113,   114,   115,   116,   117,   118,   119,    -1,   121,   122,
     123,   124,   125,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    47,    48,    49,    50,    51,    -1,    -1,    -1,
      -1,    -1,    -1,    58,    59,    60,    61,    62,    -1,    64,
      -1,    -1,    -1,    -1,    69,    -1,    71,     6,     7,     8,
      -1,    10,    11,    -1,    79,    80,    81,    -1,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,     5,    -1,
      -1,    96,    97,    -1,    -1,    -1,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,    -1,   121,   122,   123,   124,
     125,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      47,    48,    49,    50,    51,    -1,    -1,    -1,    77,    -1,
      -1,    58,    59,    60,    61,    62,    -1,    64,    -1,    -1,
      -1,    -1,    69,    -1,    71,     6,     7,     8,    -1,    10,
      11,     5,    79,    80,    81,    -1,    83,    84,    85,    86,
      87,    88,    89,    90,    91,    92,    -1,    -1,    -1,    96,
      97,    -1,    -1,    -1,   101,   102,   103,   104,   105,   106,
     107,   108,   109,   110,   111,   112,   113,   114,   115,   116,
     117,   118,   119,    47,   121,   122,   123,   124,   125,    -1,
      -1,    -1,    -1,    -1,    58,    59,    60,    61,    62,    -1,
      64,    72,    -1,    -1,    -1,    69,    77,    71,    -1,     5,
      -1,    -1,    -1,    -1,    -1,    79,    80,    81,    -1,    83,
      84,    85,    86,    87,    88,    89,    90,    91,    92,    -1,
      -1,    -1,    96,    97,    -1,    -1,    -1,   101,   102,   103,
     104,   105,   106,   107,   108,   109,   110,   111,   112,   113,
     114,   115,   116,   117,   118,   119,    -1,   121,   122,   123,
     124,   125,    58,    59,    60,    61,    62,    -1,    64,    -1,
      -1,    -1,    -1,    69,    -1,    71,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    79,    80,    81,    -1,    83,    84,    85,
      86,    87,    88,    89,    90,    91,    92,    -1,    -1,    -1,
      96,    97,    -1,    -1,    -1,   101,   102,   103,   104,   105,
     106,   107,   108,   109,   110,   111,   112,   113,   114,   115,
     116,   117,   118,   119,    -1,   121,   122,   123,   124,   125,
       6,     7,     8,    -1,    10,    11,     6,     7,     8,    -1,
      10,    11,     6,     7,     8,    -1,    10,    11,     6,     7,
       8,    -1,    10,    11,     6,     7,     8,    -1,    10,    11,
       6,     7,     8,    -1,    10,    11,    -1,    -1,    44,    -1,
      -1,     6,     7,     8,    44,    10,    11,     6,     7,     8,
      44,    10,    11,     6,     7,     8,    -1,    10,    11,    -1,
      -1,    21,    22,    23,    24,    -1,    72,    27,    28,    29,
      30,    77,    72,    21,    22,    23,    24,    77,    -1,    27,
      28,    29,    30,    77,    72,    -1,    -1,    -1,    -1,    77,
      72,    -1,    -1,    -1,    -1,    77,    72,    -1,    -1,     9,
      -1,    77,    12,    -1,    -1,     9,    -1,    72,    12,    -1,
      -1,    -1,    77,    72,    74,    -1,    -1,    -1,    77,    72,
      -1,    -1,    70,    -1,    77,    35,    36,    37,    38,    39,
      40,    35,    36,    37,    38,    39,    40,    21,    22,    23,
      24,    -1,    -1,    27,    28,    29,    30,    21,    22,    23,
      24,    -1,    -1,    27,    28,    29,    30,    12,    -1,    -1,
      44,    -1,    -1,    -1,    -1,    -1,    21,    22,    23,    24,
      44,    13,    27,    28,    29,    30,    -1,    -1,    -1,    21,
      22,    23,    24,    -1,    -1,    27,    28,    29,    30
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,   127,     0,    63,    94,    95,    98,    99,   100,   128,
      83,    84,    93,     5,    46,    47,    48,    49,    50,    51,
      58,    59,    60,    61,    62,    64,    69,    71,    73,    76,
      78,    79,    80,    81,    83,    84,    85,    86,    87,    88,
      89,    90,    91,    92,    96,    97,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,   121,   122,   123,   124,   125,
     130,   131,   132,   133,   134,   135,   136,   142,   143,   146,
     147,   148,   149,   150,   151,   152,   153,   154,   155,   157,
     159,   160,   161,   162,   163,   164,   165,   166,   168,   169,
     170,   171,    83,    83,   130,    83,    85,   129,    79,    83,
      69,   152,   150,   150,   150,   150,   131,   131,    74,   132,
     131,   131,   158,    83,    83,   131,   131,   131,   131,   131,
     131,   131,    83,   156,   156,   131,    83,    85,   129,   129,
     131,   131,   131,   131,   164,   167,   167,   131,   131,   158,
     131,    83,     3,     6,     7,     8,    10,    11,    77,    21,
      22,    23,    24,    27,    28,    29,    30,   141,    45,    31,
      32,    33,    34,    44,   137,   140,    14,    15,    16,     9,
      17,    18,    19,    35,    36,    37,    38,    39,    40,   147,
      41,    42,    43,    52,    53,    54,    55,    56,    57,    65,
      66,    67,    68,     4,    75,   130,   130,    44,    44,    72,
     132,    70,    72,   141,    74,    44,    72,    72,    72,    44,
      72,    44,    72,    44,    72,    44,    72,    44,    72,    44,
      72,    44,    72,    44,    72,    72,    72,    72,    72,    72,
      72,    72,    72,    72,    72,    44,    72,    72,    72,    72,
      72,    72,    72,   132,   132,   132,   132,   132,    13,    73,
     132,   132,   134,   136,    12,   132,   138,   139,   143,   143,
     143,   147,   146,    12,   144,   145,   146,   146,   147,   147,
     147,   147,   147,   147,   149,   149,   149,   152,   129,   129,
     130,    44,   120,   132,   141,   158,    83,    83,    83,    83,
      83,    83,    83,   156,    66,    66,   167,   132,    74,   132,
      13,   132,    12,    44,    12,   146,    44,    12,    12,   132,
      83,    85,   132,    72,    72,    72,    72,    72,    72,    72,
      74,   132,   132,   139,   146,   145,   146,   146,    44,    72,
      72,   132,    70
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,   126,   127,   127,   127,   127,   127,   128,   128,   128,
     128,   128,   129,   129,   129,   129,   129,   130,   131,   131,
     131,   131,   131,   131,   131,   131,   131,   131,   132,   132,
     133,   133,   134,   134,   135,   135,   136,   136,   136,   136,
     136,   136,   136,   136,   137,   138,   138,   139,   139,   139,
     139,   140,   140,   140,   140,   141,   141,   141,   141,   141,
     141,   141,   141,   142,   142,   142,   142,   143,   143,   143,
     143,   144,   144,   145,   145,   145,   145,   146,   146,   146,
     146,   146,   146,   146,   146,   147,   147,   148,   148,   148,
     148,   149,   149,   149,   149,   149,   150,   150,   150,   150,
     150,   150,   150,   150,   150,   150,   150,   151,   151,   152,
     152,   152,   152,   152,   152,   152,   153,   153,   153,   153,
     153,   153,   153,   153,   153,   153,   153,   153,   153,   153,
     153,   153,   153,   153,   153,   153,   153,   153,   153,   153,
     153,   153,   153,   153,   153,   153,   153,   153,   153,   153,
     153,   153,   153,   153,   153,   153,   153,   153,   154,   155,
     156,   156,   157,   158,   158,   158,   159,   160,   160,   160,
     160,   161,   161,   162,   162,   162,   162,   162,   162,   163,
     163,   163,   164,   164,   164,   164,   165,   166,   167,   167,
     168,   169,   170,   171
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     0,     2,     4,     4,     2,     3,     3,     2,
       5,     3,     3,     3,     1,     1,     0,     2,     1,     3,
       3,     3,     3,     3,     8,     2,     2,     1,     1,     1,
       3,     1,     1,     2,     3,     1,     3,     5,     4,     4,
       4,     5,     4,     5,     2,     1,     3,     3,     2,     2,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     3,     3,     3,     1,     3,     5,
       5,     1,     3,     3,     2,     2,     1,     1,     3,     3,
       3,     3,     3,     3,     3,     1,     2,     1,     3,     3,
       3,     1,     2,     2,     2,     2,     1,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     1,     2,     1,
       3,     3,     3,     2,     6,     6,     1,     1,     1,     3,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     3,     3,     3,     3,     3,     3,     3,
       5,     5,     5,     5,     5,     5,     5,     3,     1,     1,
       3,     3,     3,     3,     3,     1,     1,     1,     3,     3,
       1,     3,     3,     3,     1,     0,     3,     3,     4,     3,
       4,     3,     3,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     3,     3,     1,     3,
       3,     3,     3,     3
};


#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)
#define YYEMPTY         (-2)
#define YYEOF           0

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                  \
do                                                              \
  if (yychar == YYEMPTY)                                        \
    {                                                           \
      yychar = (Token);                                         \
      yylval = (Value);                                         \
      YYPOPSTACK (yylen);                                       \
      yystate = *yyssp;                                         \
      goto yybackup;                                            \
    }                                                           \
  else                                                          \
    {                                                           \
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;                                                  \
    }                                                           \
while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256



/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)

/* This macro is provided for backward compatibility. */
#ifndef YY_LOCATION_PRINT
# define YY_LOCATION_PRINT(File, Loc) ((void) 0)
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*----------------------------------------.
| Print this symbol's value on YYOUTPUT.  |
`----------------------------------------*/

static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  FILE *yyo = yyoutput;
  YYUSE (yyo);
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# endif
  YYUSE (yytype);
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyoutput, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yytype_int16 *yyssp, YYSTYPE *yyvsp, int yyrule)
{
  unsigned long int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       yystos[yyssp[yyi + 1 - yynrhs]],
                       &(yyvsp[(yyi + 1) - (yynrhs)])
                                              );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
static YYSIZE_T
yystrlen (const char *yystr)
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            /* Fall through.  */
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYSIZE_T *yymsg_alloc, char **yymsg,
                yytype_int16 *yyssp, int yytoken)
{
  YYSIZE_T yysize0 = yytnamerr (YY_NULLPTR, yytname[yytoken]);
  YYSIZE_T yysize = yysize0;
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat. */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Number of reported tokens (one for the "unexpected", one per
     "expected"). */
  int yycount = 0;

  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[*yyssp];
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                {
                  YYSIZE_T yysize1 = yysize + yytnamerr (YY_NULLPTR, yytname[yyx]);
                  if (! (yysize <= yysize1
                         && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
                    return 2;
                  yysize = yysize1;
                }
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  {
    YYSIZE_T yysize1 = yysize + yystrlen (yyformat);
    if (! (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
      return 2;
    yysize = yysize1;
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          yyp++;
          yyformat++;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
{
  YYUSE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}




/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;


/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.

       Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        YYSTYPE *yyvs1 = yyvs;
        yytype_int16 *yyss1 = yyss;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * sizeof (*yyssp),
                    &yyvs1, yysize * sizeof (*yyvsp),
                    &yystacksize);

        yyss = yyss1;
        yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yytype_int16 *yyss1 = yyss;
        union yyalloc *yyptr =
          (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
        if (! yyptr)
          goto yyexhaustedlab;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
                  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 3:
#line 110 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if (verbose) {
        std::cerr << std::setiosflags(std::ios::fixed) << std::setprecision(2);
        double duration = (clock() - timer) /
            (double) CLOCKS_PER_SEC;
        timer = clock();
        std::cerr << "defined " << (yyvsp[0].pmatchDefinition)->first << " in " << duration << " seconds\n";
    }
    if (definitions.count((yyvsp[0].pmatchDefinition)->first) != 0) {
        std::stringstream warning;
        warning << "definition of " << (yyvsp[0].pmatchDefinition)->first << " on line " << pmatchlineno
                << " shadows earlier definition\n";
        warn(warning.str());
        delete definitions[(yyvsp[0].pmatchDefinition)->first];
    }
    definitions.insert(*(yyvsp[0].pmatchDefinition));
 }
#line 2009 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 4:
#line 127 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    hfst::pmatch::variables[(yyvsp[-1].label)] = (yyvsp[0].label);
    free((yyvsp[-1].label)); free((yyvsp[0].label));
 }
#line 2018 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 5:
#line 131 "pmatch_parse.yy" /* yacc.c:1646  */
    {
     // the symbol can be 0, and that pretty much has to be reserved for
     // epsilon, so we detect that possibility here
     hfst::pmatch::variables[(yyvsp[-1].label)] = "0";
     free((yyvsp[-1].label));
 }
#line 2029 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 6:
#line 136 "pmatch_parse.yy" /* yacc.c:1646  */
    {
     std::string filepath = hfst::pmatch::path_from_filename((yyvsp[0].label));
     free((yyvsp[0].label));
     hfst::pmatch::read_vec(filepath);
   }
#line 2039 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 7:
#line 142 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject*>((yyvsp[-1].label), (yyvsp[0].pmatchObject));
    (yyvsp[0].pmatchObject)->name = (yyvsp[-1].label);
    free((yyvsp[-1].label));
 }
#line 2049 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 8:
#line 147 "pmatch_parse.yy" /* yacc.c:1646  */
    {
     (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject*>(
         (yyvsp[-1].label), new PmatchString(get_Ins_transition((yyvsp[-1].label))));
     def_insed_expressions[(yyvsp[-1].label)] = (yyvsp[0].pmatchObject);
     (yyvsp[0].pmatchObject)->name = (yyvsp[-1].label);
     free((yyvsp[-1].label));
 }
#line 2061 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 9:
#line 154 "pmatch_parse.yy" /* yacc.c:1646  */
    {
     (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject*>("TOP", (yyvsp[0].pmatchObject));
     (yyvsp[0].pmatchObject)->name = "TOP";
 }
#line 2070 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 10:
#line 158 "pmatch_parse.yy" /* yacc.c:1646  */
    {
     PmatchFunction * fun = new PmatchFunction(*(yyvsp[-2].string_vector), (yyvsp[0].pmatchObject));
     fun->name = (yyvsp[-3].label);
     (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject*>(std::string((yyvsp[-3].label)), fun);
     function_names.insert((yyvsp[-3].label));
     free((yyvsp[-3].label));
 }
#line 2082 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 11:
#line 165 "pmatch_parse.yy" /* yacc.c:1646  */
    {
     (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject *>(
         (yyvsp[-1].label), new PmatchUnaryOperation(MakeSigma, (yyvsp[0].pmatchObject)));
     (yyvsp[0].pmatchObject)->name = (yyvsp[-1].label);
 }
#line 2092 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 12:
#line 172 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.string_vector) = (yyvsp[0].string_vector); (yyval.string_vector)->push_back(std::string((yyvsp[-2].label))); free((yyvsp[-2].label)); }
#line 2098 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 13:
#line 173 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.string_vector) = (yyvsp[0].string_vector); (yyval.string_vector)->push_back(std::string((yyvsp[-2].label))); free((yyvsp[-2].label)); }
#line 2104 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 14:
#line 174 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.string_vector) = new std::vector<std::string>(1, std::string((yyvsp[0].label))); free((yyvsp[0].label)); }
#line 2110 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 15:
#line 175 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.string_vector) = new std::vector<std::string>(1, std::string((yyvsp[0].label))); free((yyvsp[0].label)); }
#line 2116 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 16:
#line 176 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.string_vector) = new std::vector<std::string>(); }
#line 2122 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 17:
#line 178 "pmatch_parse.yy" /* yacc.c:1646  */
    {
     (yyvsp[-1].pmatchObject)->weight += (yyvsp[0].weight);
     if (need_delimiters) {
         (yyval.pmatchObject) = new PmatchUnaryOperation(AddDelimiters, (yyvsp[-1].pmatchObject));
     } else {
         (yyval.pmatchObject) = (yyvsp[-1].pmatchObject);
     }
     need_delimiters = false;
}
#line 2136 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 18:
#line 188 "pmatch_parse.yy" /* yacc.c:1646  */
    {}
#line 2142 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 19:
#line 189 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Compose, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2148 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 20:
#line 190 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(CrossProduct, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2154 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 21:
#line 191 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(LenientCompose, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2160 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 22:
#line 192 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Merge, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject));}
#line 2166 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 23:
#line 193 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Merge, (yyvsp[0].pmatchObject), (yyvsp[-2].pmatchObject)); }
#line 2172 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 24:
#line 194 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchTernaryOperation(Substitute, (yyvsp[-5].pmatchObject), (yyvsp[-3].pmatchObject), (yyvsp[-1].pmatchObject));
}
#line 2180 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 25:
#line 197 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchBinaryOperation(CrossProduct, (yyvsp[-1].pmatchObject), new PmatchQuestionMark); }
#line 2187 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 26:
#line 199 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchBinaryOperation(CrossProduct, new PmatchQuestionMark, (yyvsp[0].pmatchObject)); }
#line 2194 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 27:
#line 201 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchQuestionMark;
}
#line 2202 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 28:
#line 205 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2208 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 29:
#line 206 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2214 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 30:
#line 209 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if ((yyvsp[0].replaceRule)->arrow != (yyvsp[-2].replaceRules)->arrow) {
        pmatcherror("Replace type mismatch in parallel rules");
    }
    (yyval.replaceRules) = dynamic_cast<PmatchParallelRulesContainer *>((yyval.replaceRules));
    (yyvsp[-2].replaceRules)->rules.push_back((yyvsp[0].replaceRule));
}
#line 2226 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 31:
#line 215 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.replaceRules) = new PmatchParallelRulesContainer((yyvsp[0].replaceRule));
}
#line 2234 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 32:
#line 220 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceRule) = new PmatchReplaceRuleContainer((yyvsp[0].mappings)); }
#line 2240 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 33:
#line 222 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceRule) = new PmatchReplaceRuleContainer((yyvsp[-1].mappings), (yyvsp[0].parallelContexts)); }
#line 2246 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 34:
#line 226 "pmatch_parse.yy" /* yacc.c:1646  */
    {
          if ((yyvsp[-2].mappings)->arrow != (yyvsp[0].mappings)->arrow) {
             pmatcherror("Replace type mismatch in parallel rules.");
          }
         (yyvsp[-2].mappings)->push_back((yyvsp[0].mappings));
      }
#line 2257 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 35:
#line 232 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.mappings) = (yyvsp[0].mappings); }
#line 2263 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 36:
#line 235 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[-1].replaceArrow), (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2270 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 37:
#line 237 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    PmatchMarkupContainer * markup = new PmatchMarkupContainer((yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject));
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[-3].replaceArrow), (yyvsp[-4].pmatchObject), markup); }
#line 2278 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 38:
#line 240 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    PmatchTransducerContainer * epsilon = new PmatchTransducerContainer(
        new HfstTransducer(hfst::internal_epsilon, format));
    PmatchMarkupContainer * markup = new PmatchMarkupContainer((yyvsp[-1].pmatchObject), epsilon);
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[-2].replaceArrow), (yyvsp[-3].pmatchObject), markup);
}
#line 2289 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 39:
#line 245 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    PmatchMarkupContainer * markup = new PmatchMarkupContainer(new PmatchEpsilonArc, (yyvsp[0].pmatchObject));
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[-2].replaceArrow), (yyvsp[-3].pmatchObject), markup);
}
#line 2298 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 40:
#line 248 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[-1].replaceArrow), new PmatchEpsilonArc, (yyvsp[0].pmatchObject));
}
#line 2306 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 41:
#line 250 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[-1].replaceArrow), (yyvsp[-3].pmatchObject), (yyvsp[0].pmatchObject));
}
#line 2314 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 42:
#line 252 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[-2].replaceArrow), (yyvsp[-3].pmatchObject), new PmatchEpsilonArc);
}
#line 2322 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 43:
#line 254 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[-3].replaceArrow), (yyvsp[-4].pmatchObject), (yyvsp[-1].pmatchObject)); }
#line 2329 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 44:
#line 259 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.parallelContexts) = new PmatchContextsContainer((yyvsp[-1].replType), (yyvsp[0].parallelContexts));
}
#line 2337 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 45:
#line 263 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.parallelContexts) = new PmatchContextsContainer((yyvsp[0].parallelContexts));
}
#line 2345 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 46:
#line 265 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyvsp[-2].parallelContexts)->push_back((yyvsp[0].parallelContexts));
    (yyval.parallelContexts) = (yyvsp[-2].parallelContexts);
}
#line 2354 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 47:
#line 271 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.parallelContexts) = new PmatchContextsContainer((yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2360 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 48:
#line 272 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.parallelContexts) = new PmatchContextsContainer((yyvsp[-1].pmatchObject), new PmatchEpsilonArc); }
#line 2366 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 49:
#line 273 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.parallelContexts) = new PmatchContextsContainer(new PmatchEpsilonArc, (yyvsp[0].pmatchObject)); }
#line 2372 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 50:
#line 274 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.parallelContexts) = new PmatchContextsContainer(new PmatchEpsilonArc, new PmatchEpsilonArc);
}
#line 2379 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 51:
#line 278 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replType) = REPL_UP; }
#line 2385 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 52:
#line 279 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replType) = REPL_RIGHT; }
#line 2391 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 53:
#line 280 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replType) = REPL_LEFT; }
#line 2397 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 54:
#line 281 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replType) = REPL_DOWN; }
#line 2403 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 55:
#line 284 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceArrow) = E_REPLACE_RIGHT; }
#line 2409 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 56:
#line 285 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceArrow) = E_OPTIONAL_REPLACE_RIGHT; }
#line 2415 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 57:
#line 286 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceArrow) = E_RTL_LONGEST_MATCH; }
#line 2421 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 58:
#line 287 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceArrow) = E_RTL_SHORTEST_MATCH; }
#line 2427 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 59:
#line 288 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceArrow) = E_LTR_LONGEST_MATCH; }
#line 2433 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 60:
#line 289 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceArrow) = E_LTR_SHORTEST_MATCH; }
#line 2439 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 61:
#line 290 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceArrow) =  E_REPLACE_LEFT; }
#line 2445 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 62:
#line 291 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.replaceArrow) = E_OPTIONAL_REPLACE_LEFT;
}
#line 2452 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 63:
#line 294 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2458 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 64:
#line 295 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Shuffle, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2464 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 65:
#line 296 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Before, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject));}
#line 2470 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 66:
#line 297 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(After, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2476 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 67:
#line 299 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2482 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 68:
#line 300 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchRestrictionContainer((yyvsp[-2].pmatchObject), (yyvsp[0].restrictionContexts)); }
#line 2488 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 69:
#line 301 "pmatch_parse.yy" /* yacc.c:1646  */
    { pmatcherror("Left arrow with contexts not implemented"); }
#line 2494 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 70:
#line 302 "pmatch_parse.yy" /* yacc.c:1646  */
    { pmatcherror("Left-right arrow with contexts not implemented"); }
#line 2500 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 71:
#line 304 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.restrictionContexts) = new MappingPairVector();
    (yyval.restrictionContexts)->push_back(*(yyvsp[0].restrictionContext));
    delete (yyvsp[0].restrictionContext);
}
#line 2510 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 72:
#line 309 "pmatch_parse.yy" /* yacc.c:1646  */
    {
     (yyvsp[-2].restrictionContexts)->push_back(*(yyvsp[0].restrictionContext));
     (yyval.restrictionContexts) = (yyvsp[-2].restrictionContexts);
     delete (yyvsp[0].restrictionContext);
}
#line 2520 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 73:
#line 316 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.restrictionContext) = new PmatchObjectPair((yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2526 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 74:
#line 317 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.restrictionContext) = new PmatchObjectPair((yyvsp[-1].pmatchObject), new PmatchEpsilonArc); }
#line 2532 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 75:
#line 318 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.restrictionContext) = new PmatchObjectPair(new PmatchEpsilonArc, (yyvsp[0].pmatchObject)); }
#line 2538 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 76:
#line 319 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.restrictionContext) = new PmatchObjectPair(new PmatchEmpty, new PmatchEmpty); }
#line 2544 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 77:
#line 321 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2550 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 78:
#line 322 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Disjunct, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2556 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 79:
#line 323 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Intersect, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2562 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 80:
#line 324 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Subtract, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2568 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 81:
#line 325 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(UpperSubtract, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2574 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 82:
#line 326 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(LowerSubtract, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2580 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 83:
#line 327 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(UpperPriorityUnion, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2586 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 84:
#line 328 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(LowerPriorityUnion, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2592 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 85:
#line 330 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2598 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 86:
#line 331 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Concatenate, (yyvsp[-1].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2604 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 87:
#line 333 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2610 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 88:
#line 334 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(InsertFreely, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2616 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 89:
#line 335 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(IgnoreInternally, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2622 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 90:
#line 336 "pmatch_parse.yy" /* yacc.c:1646  */
    { pmatcherror("Left quotient not implemented"); }
#line 2628 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 91:
#line 338 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2634 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 92:
#line 339 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Complement, (yyvsp[0].pmatchObject)); }
#line 2640 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 93:
#line 340 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Containment, (yyvsp[0].pmatchObject)); }
#line 2646 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 94:
#line 341 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(ContainmentOnce, (yyvsp[0].pmatchObject)); }
#line 2652 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 95:
#line 342 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(ContainmentOptional, (yyvsp[0].pmatchObject)); }
#line 2658 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 96:
#line 344 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2664 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 97:
#line 345 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(RepeatStar, (yyvsp[-1].pmatchObject)); }
#line 2670 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 98:
#line 346 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(RepeatPlus, (yyvsp[-1].pmatchObject)); }
#line 2676 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 99:
#line 347 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Reverse, (yyvsp[-1].pmatchObject)); }
#line 2682 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 100:
#line 348 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Invert, (yyvsp[-1].pmatchObject)); }
#line 2688 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 101:
#line 349 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(InputProject, (yyvsp[-1].pmatchObject)); }
#line 2694 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 102:
#line 350 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(OutputProject, (yyvsp[-1].pmatchObject)); }
#line 2700 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 103:
#line 351 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchNumericOperation(RepeatN, (yyvsp[-1].pmatchObject));
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[0].value));
}
#line 2709 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 104:
#line 355 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchNumericOperation(RepeatNPlus, (yyvsp[-1].pmatchObject));
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[0].value) + 1);
}
#line 2718 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 105:
#line 359 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchNumericOperation(RepeatNMinus, (yyvsp[-1].pmatchObject));
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[0].value) - 1);
}
#line 2727 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 106:
#line 363 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchNumericOperation(RepeatNToK, (yyvsp[-1].pmatchObject));
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[0].values)[0]);
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[0].values)[1]);
    free((yyvsp[0].values));
}
#line 2738 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 107:
#line 370 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2744 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 108:
#line 371 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(TermComplement, (yyvsp[0].pmatchObject)); }
#line 2750 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 109:
#line 373 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2756 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 110:
#line 374 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = (yyvsp[-1].pmatchObject); }
#line 2762 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 111:
#line 375 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBinaryOperation(CrossProduct, (yyvsp[-2].pmatchObject), (yyvsp[0].pmatchObject)); }
#line 2768 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 112:
#line 376 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Optionalize, (yyvsp[-1].pmatchObject)); }
#line 2774 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 113:
#line 377 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = (yyvsp[-1].pmatchObject); (yyval.pmatchObject)->weight += (yyvsp[0].weight); }
#line 2780 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 114:
#line 378 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchUnaryOperation(AddDelimiters,
                                  new PmatchBinaryOperation(Concatenate, (yyvsp[-4].pmatchObject),
                                                            new PmatchString((yyvsp[-1].label))));
    free((yyvsp[-1].label)); }
#line 2790 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 115:
#line 383 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchUnaryOperation(AddDelimiters,
                                  new PmatchBinaryOperation(Concatenate, (yyvsp[-4].pmatchObject),
                                                            new PmatchString((yyvsp[-1].label))));
    free((yyvsp[-1].label)); }
#line 2800 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 116:
#line 390 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchString(std::string((yyvsp[0].label))); free((yyvsp[0].label)); }
#line 2806 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 117:
#line 391 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchString(hfst::internal_epsilon); }
#line 2812 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 118:
#line 392 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchString("@BOUNDARY@"); }
#line 2818 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 119:
#line 393 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchString(std::string((yyvsp[-1].label))); free((yyvsp[-1].label)); }
#line 2824 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 120:
#line 394 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    PmatchString * retval = new PmatchString(std::string((yyvsp[0].label)));
    retval->multichar = true;
    (yyval.pmatchObject) = retval; free((yyvsp[0].label));
}
#line 2834 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 121:
#line 399 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchQuestionMark; }
#line 2840 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 122:
#line 400 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2846 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 123:
#line 401 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2852 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 124:
#line 402 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2858 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 125:
#line 404 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2864 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 126:
#line 405 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 2870 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 127:
#line 406 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchAcceptor(Alpha); }
#line 2876 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 128:
#line 407 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchAcceptor(LowercaseAlpha); }
#line 2882 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 129:
#line 408 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchAcceptor(UppercaseAlpha); }
#line 2888 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 130:
#line 409 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchAcceptor(Numeral); }
#line 2894 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 131:
#line 410 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchAcceptor(Punctuation); }
#line 2900 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 132:
#line 411 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchAcceptor(Whitespace); }
#line 2906 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 133:
#line 412 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Cap, (yyvsp[-1].pmatchObject)); }
#line 2912 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 134:
#line 413 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(OptCap, (yyvsp[-1].pmatchObject)); }
#line 2918 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 135:
#line 414 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(ToLower, (yyvsp[-1].pmatchObject)); }
#line 2924 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 136:
#line 415 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(ToUpper, (yyvsp[-1].pmatchObject)); }
#line 2930 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 137:
#line 416 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(OptToLower, (yyvsp[-1].pmatchObject)); }
#line 2936 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 138:
#line 417 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(OptToUpper, (yyvsp[-1].pmatchObject)); }
#line 2942 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 139:
#line 418 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(AnyCase, (yyvsp[-1].pmatchObject)); }
#line 2948 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 140:
#line 420 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if (strcmp((yyvsp[-1].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(CapUpper, (yyvsp[-3].pmatchObject));
    } else if (strcmp((yyvsp[-1].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(CapLower, (yyvsp[-3].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(Cap, (yyvsp[-3].pmatchObject));
    }
    free((yyvsp[-1].label));
}
#line 2964 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 141:
#line 431 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if (strcmp((yyvsp[-1].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptCapUpper, (yyvsp[-3].pmatchObject));
    } else if (strcmp((yyvsp[-1].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptCapLower, (yyvsp[-3].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptCap, (yyvsp[-3].pmatchObject));
    }
    free((yyvsp[-1].label));
}
#line 2980 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 142:
#line 442 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if (strcmp((yyvsp[-1].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToLowerUpper, (yyvsp[-3].pmatchObject));
    } else if (strcmp((yyvsp[-1].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToLowerLower, (yyvsp[-3].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToLower, (yyvsp[-3].pmatchObject));
    }
    free((yyvsp[-1].label));
}
#line 2996 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 143:
#line 453 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if (strcmp((yyvsp[-1].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToUpperUpper, (yyvsp[-3].pmatchObject));
    } else if (strcmp((yyvsp[-1].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToUpperLower, (yyvsp[-3].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToUpper, (yyvsp[-3].pmatchObject));
    }
    free((yyvsp[-1].label));
}
#line 3012 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 144:
#line 464 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if (strcmp((yyvsp[-1].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToLowerUpper, (yyvsp[-3].pmatchObject));
    } else if (strcmp((yyvsp[-1].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToLowerLower, (yyvsp[-3].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToLower, (yyvsp[-3].pmatchObject));
    }
    free((yyvsp[-1].label));
}
#line 3028 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 145:
#line 475 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if (strcmp((yyvsp[-1].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToUpperUpper, (yyvsp[-3].pmatchObject));
    } else if (strcmp((yyvsp[-1].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToUpperLower, (yyvsp[-3].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToUpper, (yyvsp[-3].pmatchObject));
    }
    free((yyvsp[-1].label));
}
#line 3044 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 146:
#line 486 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if (strcmp((yyvsp[-1].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(AnyCaseUpper, (yyvsp[-3].pmatchObject));
    } else if (strcmp((yyvsp[-1].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(AnyCaseLower, (yyvsp[-3].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(AnyCase, (yyvsp[-3].pmatchObject));
    }
    free((yyvsp[-1].label));
}
#line 3060 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 147:
#line 497 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(AddDelimiters, (yyvsp[-1].pmatchObject)); }
#line 3066 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 148:
#line 498 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 3072 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 149:
#line 499 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = (yyvsp[0].pmatchObject); }
#line 3078 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 150:
#line 500 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(MakeList, (yyvsp[-1].pmatchObject)); }
#line 3084 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 151:
#line 501 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(MakeExcList, (yyvsp[-1].pmatchObject)); }
#line 3090 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 152:
#line 502 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchBuiltinFunction(Interpolate, (yyvsp[-1].pmatchObject_vector)); }
#line 3096 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 153:
#line 503 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = new PmatchUnaryOperation(MakeSigma, (yyvsp[-1].pmatchObject)); }
#line 3102 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 154:
#line 504 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = hfst::pmatch::make_counter((yyvsp[-1].label)); free((yyvsp[-1].label)); }
#line 3108 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 155:
#line 505 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject) = (yyvsp[0].pmatchObject); hfst::pmatch::need_delimiters = true; }
#line 3114 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 156:
#line 506 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = (yyvsp[0].pmatchObject);
    // We will wrap the current definition with entry and exit guards
    hfst::pmatch::need_delimiters = true;
    // Switch off the automatic separator-seeking context condition
    hfst::pmatch::variables["need-separators"] = "off";
}
#line 3126 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 157:
#line 513 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    std::string sym((yyvsp[0].label));
    free((yyvsp[0].label));
    if (sym.size() == 0) {
        (yyval.pmatchObject) = new PmatchEmpty;
    } else {
        (yyval.pmatchObject) = new PmatchSymbol(sym);
        used_definitions.insert(sym);
    }
}
#line 3141 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 158:
#line 525 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchString((yyvsp[-1].label), true);
    free((yyvsp[-1].label));
}
#line 3150 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 159:
#line 531 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = new PmatchString((yyvsp[-1].label));
    free((yyvsp[-1].label));
}
#line 3159 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 160:
#line 537 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.label) = (yyvsp[0].label); }
#line 3165 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 161:
#line 539 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.label) = static_cast<char*>(malloc(sizeof(char)*(strlen((yyvsp[-2].label)) + strlen((yyvsp[0].label))+1)));
    strcpy((yyval.label), (yyvsp[-2].label));
    strcat((yyval.label), (yyvsp[0].label));
    free((yyvsp[-2].label)); free((yyvsp[0].label));
}
#line 3176 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 162:
#line 547 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    std::string sym((yyvsp[-2].label));
    if (function_names.count((yyvsp[-2].label)) == 0) {
        std::stringstream ss;
        ss << "Function " << sym << " hasn't been defined\n";
        pmatcherror(ss.str().c_str());
        (yyval.pmatchObject) = new PmatchString("");
    } else {
        (yyval.pmatchObject) = new PmatchFuncall(
            (yyvsp[-1].pmatchObject_vector),
            dynamic_cast<PmatchFunction *>(symbol_from_global_context(sym)));
    }
    used_definitions.insert(sym);
    free((yyvsp[-2].label));
}
#line 3196 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 163:
#line 563 "pmatch_parse.yy" /* yacc.c:1646  */
    {
(yyval.pmatchObject_vector) = (yyvsp[0].pmatchObject_vector); (yyval.pmatchObject_vector)->push_back((yyvsp[-2].pmatchObject)); }
#line 3203 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 164:
#line 565 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject_vector) = new std::vector<PmatchObject *>(1, (yyvsp[0].pmatchObject)); }
#line 3209 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 165:
#line 566 "pmatch_parse.yy" /* yacc.c:1646  */
    { (yyval.pmatchObject_vector) = new std::vector<PmatchObject *>; }
#line 3215 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 166:
#line 568 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if (!hfst::pmatch::flatten) {
        if(hfst::pmatch::definitions.count((yyvsp[-1].label)) == 0) {
            hfst::pmatch::unsatisfied_insertions.insert((yyvsp[-1].label));
        }
        (yyval.pmatchObject) = new PmatchString(hfst::pmatch::get_Ins_transition((yyvsp[-1].label)));
        hfst::pmatch::inserted_names.insert((yyvsp[-1].label));
        hfst::pmatch::used_definitions.insert((yyvsp[-1].label));
    } else if(hfst::pmatch::definitions.count((yyvsp[-1].label)) != 0) {
        (yyval.pmatchObject) = hfst::pmatch::definitions[(yyvsp[-1].label)];
    } else {
        (yyval.pmatchObject) = new PmatchEmpty;
        std::stringstream ss;
        ss << "Insertion of " << (yyvsp[-1].label) << " on line " << pmatchlineno << " is undefined and --flatten is in use\n";
        pmatcherror(ss.str().c_str());
    }
    free((yyvsp[-1].label));
}
#line 3238 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 167:
#line 587 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if ((yyvsp[-1].string_vector)->size() == 0) {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc("");
    } else if ((yyvsp[-1].string_vector)->size() == 1) {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[-1].string_vector)->operator[](0));
    } else {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[-1].string_vector)->operator[](0),
                                            (yyvsp[-1].string_vector)->operator[](1));
    }
    delete((yyvsp[-1].string_vector));
}
#line 3254 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 168:
#line 598 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if ((yyvsp[-2].string_vector)->size() == 0) {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc("");
    } else if ((yyvsp[-2].string_vector)->size() == 1) {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[-2].string_vector)->operator[](0), "", (yyvsp[0].value));
    } else {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[-2].string_vector)->operator[](0),
                                            (yyvsp[-2].string_vector)->operator[](1), (yyvsp[0].value));
    }
    delete((yyvsp[-2].string_vector));
}
#line 3270 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 169:
#line 609 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if ((yyvsp[-1].string_vector)->size() < 2) {
        std::stringstream err;
        err << "Unlike() operation takes exactly 2 arguments, got " << (yyvsp[-1].string_vector)->size();
        pmatcherror(err.str().c_str());
    } else {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[-1].string_vector)->operator[](1),
                                            (yyvsp[-1].string_vector)->operator[](0), 10, true);
    }
    delete((yyvsp[-1].string_vector));
}
#line 3286 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 170:
#line 620 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    if ((yyvsp[-2].string_vector)->size() < 2) {
        std::stringstream err;
        err << "Unlike() operation takes exactly 2 arguments, got " << (yyvsp[-2].string_vector)->size();
        pmatcherror(err.str().c_str());
    } else {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[-2].string_vector)->operator[](1),
                                            (yyvsp[-2].string_vector)->operator[](0), (yyvsp[0].value), true);
    }
    delete((yyvsp[-2].string_vector));
}
#line 3302 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 171:
#line 633 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = hfst::pmatch::make_end_tag((yyvsp[-1].label));
    free((yyvsp[-1].label));
}
#line 3311 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 172:
#line 636 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = hfst::pmatch::make_end_tag((yyvsp[-1].label));
    free((yyvsp[-1].label));
}
#line 3320 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 173:
#line 641 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[0].label));
    free((yyvsp[0].label));
    HfstTransducer * read = NULL;
    try {
        hfst::HfstInputStream instream(filepath);
        read = new HfstTransducer(instream);
        instream.close();
    } catch(HfstException) {
        std::string ermsg =
            std::string("Couldn't read transducer from ") +
            filepath;
        pmatcherror(ermsg.c_str());
    }
    if (read->get_type() != hfst::pmatch::format) {
        read->convert(hfst::pmatch::format);
    }
    (yyval.pmatchObject) = new PmatchTransducerContainer(read);
}
#line 3344 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 174:
#line 659 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[0].label));
    free((yyvsp[0].label));
    (yyval.pmatchObject) = new PmatchTransducerContainer(hfst::pmatch::read_text(filepath));
}
#line 3354 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 175:
#line 663 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[0].label));
    free((yyvsp[0].label));
    (yyval.pmatchObject) = new PmatchTransducerContainer(hfst::pmatch::read_spaced_text(filepath));
}
#line 3364 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 176:
#line 667 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[0].label));
    free((yyvsp[0].label));
    FILE * f = NULL;
    f = hfst::hfst_fopen(filepath.c_str(), "r");
    if (f == NULL) {
        pmatcherror("File cannot be opened.\n");
    } else {
        try {
            unsigned int linecount = 0;
            HfstBasicTransducer tmp = HfstBasicTransducer::read_in_prolog_format(f, linecount);
            fclose(f);
            HfstTransducer * t = new HfstTransducer(tmp, hfst::pmatch::format);
            t->minimize();
            (yyval.pmatchObject) = new PmatchTransducerContainer(t);
        }
        catch (const HfstException & e) {
            (void) e;
            fclose(f);
            pmatcherror("Error reading prolog file.\n");
        }
    }
}
#line 3392 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 177:
#line 689 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[0].label));
    free((yyvsp[0].label));
    (yyval.pmatchObject) = new PmatchTransducerContainer(hfst::HfstTransducer::read_lexc_ptr(filepath, format, hfst::pmatch::verbose));
}
#line 3402 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 178:
#line 693 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[0].label));
    free((yyvsp[0].label));
    std::string regex;
    std::string tmp;
    std::ifstream regexfile(filepath.c_str());
    if (regexfile.is_open()) {
        while (getline(regexfile, tmp)) {
            regex.append(tmp);
        }
    }
    if (regex.size() == 0) {
        std::stringstream err;
        err << "Failed to read regex from " << filepath << ".\n";
        pmatcherror(err.str().c_str());
    }
    hfst::xre::XreCompiler xre_compiler;
    (yyval.pmatchObject) = new PmatchTransducerContainer(xre_compiler.compile(regex));
    }
#line 3426 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 179:
#line 714 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 3432 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 180:
#line 715 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 3438 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 181:
#line 716 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 3444 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 182:
#line 719 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 3450 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 183:
#line 720 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 3456 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 184:
#line 721 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 3462 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 185:
#line 722 "pmatch_parse.yy" /* yacc.c:1646  */
    { }
#line 3468 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 186:
#line 725 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = NULL;
    for (std::vector<PmatchObject *>::reverse_iterator it = (yyvsp[-1].pmatchObject_vector)->rbegin();
         it != (yyvsp[-1].pmatchObject_vector)->rend(); ++it) {
        if ((yyval.pmatchObject) == NULL) {
            (yyval.pmatchObject) = *it;
        } else {
            PmatchObject * tmp = (yyval.pmatchObject);
            (yyval.pmatchObject) = new PmatchBinaryOperation(Disjunct, tmp, *it);
        }
    }
    delete (yyvsp[-1].pmatchObject_vector);
    // Zero the counter for making minimization
    // guards for disjuncted negative contexts
    hfst::pmatch::zero_minimization_guard();
}
#line 3489 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 187:
#line 743 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject) = NULL;
    for (std::vector<PmatchObject *>::reverse_iterator it = (yyvsp[-1].pmatchObject_vector)->rbegin();
         it != (yyvsp[-1].pmatchObject_vector)->rend(); ++it) {
        if ((yyval.pmatchObject) == NULL) {
            (yyval.pmatchObject) = *it;
        } else {
            PmatchObject * tmp = (yyval.pmatchObject);
            (yyval.pmatchObject) = new PmatchBinaryOperation(Concatenate, tmp, *it);
        }
    }
    delete (yyvsp[-1].pmatchObject_vector);
}
#line 3507 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 188:
#line 758 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyval.pmatchObject_vector) = new std::vector<PmatchObject *>(1, (yyvsp[0].pmatchObject));
}
#line 3515 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 189:
#line 761 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyvsp[0].pmatchObject_vector)->push_back((yyvsp[-2].pmatchObject));
    (yyval.pmatchObject_vector) = (yyvsp[0].pmatchObject_vector);
}
#line 3524 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 190:
#line 766 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyvsp[-1].pmatchObject)->mark_context_children();
    (yyval.pmatchObject) = new PmatchUnaryOperation(RC, (yyvsp[-1].pmatchObject));
}
#line 3533 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 191:
#line 771 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyvsp[-1].pmatchObject)->mark_context_children();
    (yyval.pmatchObject) = new PmatchUnaryOperation(NRC, (yyvsp[-1].pmatchObject));
}
#line 3542 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 192:
#line 776 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyvsp[-1].pmatchObject)->mark_context_children();
    (yyval.pmatchObject) = new PmatchUnaryOperation(LC, (yyvsp[-1].pmatchObject));
}
#line 3551 "pmatch_parse.cc" /* yacc.c:1646  */
    break;

  case 193:
#line 781 "pmatch_parse.yy" /* yacc.c:1646  */
    {
    (yyvsp[-1].pmatchObject)->mark_context_children();
    (yyval.pmatchObject) = new PmatchUnaryOperation(NLC, (yyvsp[-1].pmatchObject));
}
#line 3560 "pmatch_parse.cc" /* yacc.c:1646  */
    break;


#line 3564 "pmatch_parse.cc" /* yacc.c:1646  */
      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = (char *) YYSTACK_ALLOC (yymsg_alloc);
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYTERROR;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined yyoverflow || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  return yyresult;
}
#line 814 "pmatch_parse.yy" /* yacc.c:1906  */

