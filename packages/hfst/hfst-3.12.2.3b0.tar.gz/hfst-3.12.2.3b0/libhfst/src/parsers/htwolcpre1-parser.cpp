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
#define yyparse         htwolcpre1parse
#define yylex           htwolcpre1lex
#define yyerror         htwolcpre1error
#define yydebug         htwolcpre1debug
#define yynerrs         htwolcpre1nerrs

#define yylval          htwolcpre1lval
#define yychar          htwolcpre1char

/* Copy the first part of user declarations.  */
#line 13 "htwolcpre1-parser.yy" /* yacc.c:339  */

#ifdef HAVE_CONFIG_H
#  include <config.h>
#endif

#ifdef WINDOWS
#include <io.h>
#endif

#include <iostream>
#include <fstream>
#include <cstdlib>
#include "string_src/string_manipulation.h"
#include "io_src/InputReader.h"
#include "grammar_defs.h"
#include "variable_src/RuleSymbolVector.h"
#include "variable_src/RuleVariables.h"
#include "../HfstExceptionDefs.h"

  extern int htwolcpre1lineno;
  extern char * htwolcpre1text;
  extern int htwolcpre1lineno;
  extern char * htwolcpre1text;
  extern bool htwolcpre1_rules_start;
  void htwolcpre1error(const char * text );
  void htwolcpre1warn(const char * warning );
  int htwolcpre1lex();
  int htwolcpre1parse();
  void reduce_queue(bool variable_symbol=false);
  void set_variable_values(void);
  void reduce_symbol_pair(bool no_definitions = false);
  void increase_line_counter(void);
  std::string &get_symbol_queue_front(void);
  void pop_symbol_queue(void);
  std::ostream * output = NULL;

#define YYERROR_VERBOSE 1

  // For displaying the line number in error messages and warnings.
  size_t htwolcpre1_line_number = 1;
 
  // For reading input one byte at a time.
  InputReader htwolcpre1_input_reader(htwolcpre1_line_number);

namespace hfst {
  namespace twolcpre1 {

    void set_input(std::istream & istr)
    {
      htwolcpre1_input_reader.set_input(istr);
    }
    int parse()
    {
      return htwolcpre1parse();
    }
    void set_output(std::ostream & ostr)
    {
      output = &ostr;
    }
    void set_warning_stream(std::ostream & ostr)
    {
      htwolcpre1_input_reader.set_warning_stream(ostr);
    }
    void set_error_stream(std::ostream & ostr)
    {
      htwolcpre1_input_reader.set_error_stream(ostr);
    }
  }
}

  // For keeping track of values of variables.
  VariableValueMap variable_value_map;
  
  // For storing variable constructions of rules.
  RuleVariables rule_variables;

  // For storing the string representation of rules and replacing
  // rule variables by their values.
  RuleSymbolVector rule_symbol_vector(variable_value_map);

  // The latest symbol that was read is always the last element of this queue.
  HandyDeque<std::string> htwolcpre1_symbol_queue;

  // Stores symbol set names.
  HandySet<std::string> sets;

  // Stores definition names.
  HandySet<std::string> definitions;

  // Stores set names in "__HFST_TWOLC_SET_NAME=X" format and the set symbols.
  HandyMap<std::string,std::vector<std::string> > set_symbols;

  // The name of the lates set which was defined.
  std::string set_name;
  
  // Pointer to the latest symbol set which is being defined.
  std::vector<std::string> latest_set;

  // Tells whether we are inside a ( .. ). For variable rules.
  bool htwolcpre1_inside_parenthesis = false;

  // For temporarily storing a rule variable and its values
  StringVector variable_vector;

  // Queue for rule-matchers.
  HandyDeque<Matcher> matcher_queue;

namespace hfst {
namespace twolcpre1 {
void reset_parser()
{
  output = NULL;
  htwolcpre1_line_number = 1;
  htwolcpre1_input_reader.reset();
  variable_value_map = VariableValueMap();
  rule_variables = RuleVariables();
  //rule_symbol_vector.reset();
  htwolcpre1_symbol_queue = HandyDeque<std::string>();
  sets = HandySet<std::string>();
  definitions = HandySet<std::string>();
  set_symbols = HandyMap<std::string,std::vector<std::string> >();
  set_name = std::string();
  latest_set.clear();
  htwolcpre1_inside_parenthesis = false;
  variable_vector.clear();
  matcher_queue = HandyDeque<Matcher>();
}
}
}

#line 205 "htwolcpre1-parser.cc" /* yacc.c:339  */

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
# define YYERROR_VERBOSE 0
#endif

/* In a future release of Bison, this section will be replaced
   by #include "y.tab.h".  */
#ifndef YY_HTWOLCPRE1_HTWOLCPRE_PARSER_HH_INCLUDED
# define YY_HTWOLCPRE1_HTWOLCPRE_PARSER_HH_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int htwolcpre1debug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    FREELY_INSERT = 258,
    DIFFERENCE = 259,
    INTERSECTION = 260,
    UNION = 261,
    STAR = 262,
    PLUS = 263,
    CONTAINMENT = 264,
    CONTAINMENT_ONCE = 265,
    TERM_COMPLEMENT = 266,
    COMPLEMENT = 267,
    POWER = 268,
    RIGHT_SQUARE_BRACKET = 269,
    RIGHT_PARENTHESIS = 270,
    LEFT_SQUARE_BRACKET = 271,
    LEFT_PARENTHESIS = 272,
    RIGHT_CURLY_BRACKET = 273,
    LEFT_CURLY_BRACKET = 274,
    LEFT_RESTRICTION_ARROW = 275,
    LEFT_ARROW = 276,
    RIGHT_ARROW = 277,
    LEFT_RIGHT_ARROW = 278,
    RE_LEFT_RESTRICTION_ARROW = 279,
    RE_LEFT_ARROW = 280,
    RE_RIGHT_ARROW = 281,
    RE_LEFT_RIGHT_ARROW = 282,
    RE_RIGHT_SQUARE_BRACKET = 283,
    RE_LEFT_SQUARE_BRACKET = 284,
    ALPHABET_DECLARATION = 285,
    DIACRITICS_DECLARATION = 286,
    SETS_DECLARATION = 287,
    DEFINITION_DECLARATION = 288,
    RULES_DECLARATION = 289,
    VARIABLE_DECLARATION = 290,
    COLON = 291,
    WHERE = 292,
    MATCHED_MATCHER = 293,
    MIXED_MATCHER = 294,
    FREELY_MATCHER = 295,
    IN = 296,
    AND = 297,
    COLON_SPACE = 298,
    SYMBOL_SPACE = 299,
    SEMI_COLON = 300,
    EQUALS = 301,
    CENTER_MARKER = 302,
    RULE_NAME = 303,
    SYMBOL = 304,
    NUMBER = 305,
    NUMBER_SPACE = 306,
    QUESTION_MARK = 307,
    EXCEPT = 308
  };
#endif
/* Tokens.  */
#define FREELY_INSERT 258
#define DIFFERENCE 259
#define INTERSECTION 260
#define UNION 261
#define STAR 262
#define PLUS 263
#define CONTAINMENT 264
#define CONTAINMENT_ONCE 265
#define TERM_COMPLEMENT 266
#define COMPLEMENT 267
#define POWER 268
#define RIGHT_SQUARE_BRACKET 269
#define RIGHT_PARENTHESIS 270
#define LEFT_SQUARE_BRACKET 271
#define LEFT_PARENTHESIS 272
#define RIGHT_CURLY_BRACKET 273
#define LEFT_CURLY_BRACKET 274
#define LEFT_RESTRICTION_ARROW 275
#define LEFT_ARROW 276
#define RIGHT_ARROW 277
#define LEFT_RIGHT_ARROW 278
#define RE_LEFT_RESTRICTION_ARROW 279
#define RE_LEFT_ARROW 280
#define RE_RIGHT_ARROW 281
#define RE_LEFT_RIGHT_ARROW 282
#define RE_RIGHT_SQUARE_BRACKET 283
#define RE_LEFT_SQUARE_BRACKET 284
#define ALPHABET_DECLARATION 285
#define DIACRITICS_DECLARATION 286
#define SETS_DECLARATION 287
#define DEFINITION_DECLARATION 288
#define RULES_DECLARATION 289
#define VARIABLE_DECLARATION 290
#define COLON 291
#define WHERE 292
#define MATCHED_MATCHER 293
#define MIXED_MATCHER 294
#define FREELY_MATCHER 295
#define IN 296
#define AND 297
#define COLON_SPACE 298
#define SYMBOL_SPACE 299
#define SEMI_COLON 300
#define EQUALS 301
#define CENTER_MARKER 302
#define RULE_NAME 303
#define SYMBOL 304
#define NUMBER 305
#define NUMBER_SPACE 306
#define QUESTION_MARK 307
#define EXCEPT 308

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 148 "htwolcpre1-parser.yy" /* yacc.c:355  */
 int symbol_number; 

#line 354 "htwolcpre1-parser.cc" /* yacc.c:355  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE htwolcpre1lval;

int htwolcpre1parse (void);

#endif /* !YY_HTWOLCPRE1_HTWOLCPRE_PARSER_HH_INCLUDED  */

/* Copy the second part of user declarations.  */

#line 371 "htwolcpre1-parser.cc" /* yacc.c:358  */

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
#define YYFINAL  26
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   198

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  54
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  53
/* YYNRULES -- Number of rules.  */
#define YYNRULES  109
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  165

/* YYTRANSLATE[YYX] -- Symbol number corresponding to YYX as returned
   by yylex, with out-of-bounds checking.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   308

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
      45,    46,    47,    48,    49,    50,    51,    52,    53
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   196,   196,   199,   200,   202,   203,   205,   206,   208,
     209,   211,   212,   214,   216,   218,   219,   221,   255,   266,
     272,   273,   274,   275,   277,   279,   280,   282,   283,   284,
     285,   287,   288,   289,   290,   292,   293,   295,   296,   298,
     300,   302,   305,   308,   311,   312,   314,   315,   317,   324,
     325,   328,   330,   333,   336,   337,   339,   341,   343,   345,
     347,   349,   350,   352,   354,   355,   356,   357,   358,   360,
     361,   363,   364,   370,   371,   372,   373,   374,   375,   376,
     377,   378,   380,   381,   383,   384,   386,   387,   389,   414,
     417,   424,   435,   445,   446,   449,   456,   465,   472,   481,
     496,   503,   515,   516,   519,   520,   523,   524,   527,   528
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 0
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "FREELY_INSERT", "DIFFERENCE",
  "INTERSECTION", "UNION", "STAR", "PLUS", "CONTAINMENT",
  "CONTAINMENT_ONCE", "TERM_COMPLEMENT", "COMPLEMENT", "POWER",
  "RIGHT_SQUARE_BRACKET", "RIGHT_PARENTHESIS", "LEFT_SQUARE_BRACKET",
  "LEFT_PARENTHESIS", "RIGHT_CURLY_BRACKET", "LEFT_CURLY_BRACKET",
  "LEFT_RESTRICTION_ARROW", "LEFT_ARROW", "RIGHT_ARROW",
  "LEFT_RIGHT_ARROW", "RE_LEFT_RESTRICTION_ARROW", "RE_LEFT_ARROW",
  "RE_RIGHT_ARROW", "RE_LEFT_RIGHT_ARROW", "RE_RIGHT_SQUARE_BRACKET",
  "RE_LEFT_SQUARE_BRACKET", "ALPHABET_DECLARATION",
  "DIACRITICS_DECLARATION", "SETS_DECLARATION", "DEFINITION_DECLARATION",
  "RULES_DECLARATION", "VARIABLE_DECLARATION", "COLON", "WHERE",
  "MATCHED_MATCHER", "MIXED_MATCHER", "FREELY_MATCHER", "IN", "AND",
  "COLON_SPACE", "SYMBOL_SPACE", "SEMI_COLON", "EQUALS", "CENTER_MARKER",
  "RULE_NAME", "SYMBOL", "NUMBER", "NUMBER_SPACE", "QUESTION_MARK",
  "EXCEPT", "$accept", "ALL", "GRAMMAR", "GRAMMAR1", "GRAMMAR2",
  "GRAMMAR3", "GRAMMAR4", "GRAMMAR5", "RULES", "RULE_LIST", "RULE",
  "RULE_NAME_DECL", "RULE_CENTER", "RE_RULE_CENTER", "CENTER_LIST",
  "RULE_OPERATOR", "RE_RULE_OPERATOR", "RULE_CONTEXTS",
  "NEGATIVE_RULE_CONTEXTS", "MATCHER", "RULE_CONTEXT", "RULE_VARIABLES",
  "RULE_VARIABLE_BLOCKS", "RULE_VARIABLE_BLOCK",
  "RULE_VARIABLE_INITIALIZATION_LIST", "RULE_VARIABLE_INITIALIZATION",
  "VAR_SYMBOL", "VAR_SYMBOL_LIST", "ALPHABET", "DIACRITICS", "VARIABLES",
  "SETS", "DEFINITIONS", "DEFINITION_LIST", "DEFINITION",
  "REGULAR_EXPRESSION", "RE_LIST", "RE", "SET_LIST", "SYMBOL_LIST",
  "DIACRITIC_LIST", "SET_SYMBOL", "DIACRITIC_SYMBOL", "SET_DEFINITION",
  "SET_NAME", "DEFINITION_NAME", "ALPHABET_PAIR_LIST", "PAIR",
  "ALPHABET_PAIR", "GRAMMAR_SYMBOL", "GRAMMAR_SYMBOL_SPACE",
  "VARIABLE_LIST", "SEMI_COLON_LIST", YY_NULLPTR
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
     305,   306,   307,   308
};
# endif

#define YYPACT_NINF -76

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-76)))

#define YYTABLE_NINF -39

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int16 yypact[] =
{
     139,   -76,   -76,   -76,   -76,   -76,   -76,    32,   -76,   -76,
     -76,   -76,   -76,   -76,   -76,   144,   148,   164,     3,    13,
     117,    31,   -27,    41,     0,    31,   -76,   -76,   -76,   -76,
     -76,   -76,   -76,   -76,   -76,   -76,   -76,   -76,    51,   -76,
      14,   -76,   -76,    14,   -76,   -76,    43,   -76,   -76,    50,
     -76,   -76,    65,   -76,    14,    35,   -76,   -76,   -76,    73,
      73,   -76,    35,   -76,     8,   160,   -76,    47,   -76,   -76,
      31,    21,    61,     4,   -76,    27,   115,   -76,    73,   -76,
     -76,   -76,   -76,   -76,   -76,   -76,   -76,   -76,   -76,    35,
     -76,   -76,   -76,    14,   -76,   -76,   -76,   -76,    14,    61,
      61,    61,    61,   -76,   -76,   -76,   151,   -76,    73,   -76,
     -76,   -76,   -76,    12,    15,   -76,    61,    61,    61,    61,
      86,    86,    86,    86,   149,   145,   126,   -76,   -76,    49,
     -76,   -76,    66,   -76,    17,   -76,   -76,   -76,   -76,   -76,
       9,   -76,   -76,   -76,   -26,   -76,    96,    21,   -76,    14,
     -76,   -76,   -76,   -76,   -76,    72,   -76,    14,   -76,   -10,
     -76,   -76,    23,   -76,   -76
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       0,    93,    86,    82,    61,    15,   106,     0,     2,     4,
       6,     8,    10,    12,    13,     0,     0,     0,     0,     0,
       0,     0,    59,    60,    14,     0,     1,     3,     5,     7,
       9,    11,   104,   108,   102,   103,   105,    94,     0,   101,
      56,    87,    89,    57,    91,    83,     0,    92,    62,     0,
      19,    16,     0,   107,    58,     0,   109,    84,    69,     0,
       0,    69,     0,    98,     0,     0,    20,     0,    99,   100,
       0,     0,    64,     0,    25,     0,     0,    96,     0,    29,
      27,    28,    30,    35,    33,    31,    32,    34,    35,     0,
      95,    85,    88,    90,    69,    69,    69,    69,    63,     0,
       0,     0,     0,    69,    69,    69,    70,    71,     0,    22,
      23,    24,    21,    69,    69,    97,    68,    67,    66,    65,
      75,    76,    78,    77,     0,     0,     0,    73,    74,     0,
      26,    35,    44,    36,     0,    18,    79,    81,    80,    72,
      69,    49,    17,    69,     0,    46,    42,     0,    49,    45,
      39,    40,    41,    48,    50,     0,    53,    43,    47,     0,
      54,    52,     0,    51,    55
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int8 yypgoto[] =
{
     -76,   -76,   -76,    87,    90,   110,    89,   114,   -76,   -76,
     -76,   -76,   -76,   -76,    77,   -76,   -76,   -75,    24,   -76,
     -76,   -76,   -76,    -7,   -76,   -76,   -64,   -76,   -76,   -76,
     -76,   -76,   -76,   -76,   -76,   -50,    94,    93,   -76,   -76,
     -76,   -76,   -76,   -76,   -76,   -76,   -76,   104,   -17,   -16,
     -20,   -76,   -19
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,     7,     8,     9,    10,    11,    12,    13,    14,    24,
      51,    52,    64,    65,    73,    83,    88,   113,   132,   153,
     133,   142,   144,   145,   146,   154,   155,   162,    15,    16,
      17,    18,    19,    23,    48,   134,    72,   106,    22,    70,
      21,    91,    41,    45,    46,    49,    20,   107,    74,    67,
      68,    25,    40
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
      39,    42,    43,    37,    38,    53,    54,   160,    71,   -38,
     108,    76,   -37,   114,    78,   -37,   148,    44,   109,    33,
      94,    95,    96,    97,    94,    95,    96,    97,    79,    80,
      81,    82,    26,   108,    32,    69,     4,     5,   163,    39,
      39,    36,    77,    38,    38,   110,   -38,     5,    50,   -37,
      92,    93,    98,   124,   125,   126,   140,   -38,    39,    56,
     -37,   112,    38,   -37,   143,   131,    33,    32,   131,   115,
      99,   100,   101,   102,    36,    32,    33,   103,   104,    32,
     105,    59,    36,    89,    60,    47,    36,    55,    39,    57,
      90,   130,    38,   147,    61,   161,    58,    62,   164,   129,
     139,    62,    27,   141,    63,    32,    28,    30,    63,    32,
      34,    35,    36,   159,    34,    35,    36,    32,    94,    95,
      96,    97,    34,    35,    36,   149,   156,    29,   157,    94,
      95,    96,    97,    31,   150,   151,   152,    75,   135,   156,
      32,   158,   156,   111,   138,     0,     0,    36,    94,    95,
      96,    97,    94,    95,    96,    97,    66,     0,   127,   128,
     137,    32,    33,   136,   129,     0,    34,    35,    36,     1,
       2,     3,     4,     5,     6,     2,     3,     4,     5,     6,
       3,     4,     5,     6,    84,    85,    86,    87,   116,   117,
     118,   119,   120,   121,   122,   123,     3,     4,     5
};

static const yytype_int16 yycheck[] =
{
      20,    21,    21,    20,    20,    25,    25,    17,    58,     0,
       6,    61,     0,    88,     6,     0,    42,    44,    14,    45,
       3,     4,     5,     6,     3,     4,     5,     6,    20,    21,
      22,    23,     0,     6,    44,    55,    33,    34,    15,    59,
      60,    51,    62,    59,    60,    18,    37,    34,    48,    37,
      70,    70,    71,   103,   104,   105,   131,    48,    78,    45,
      48,    78,    78,    48,    47,    53,    45,    44,    53,    89,
       9,    10,    11,    12,    51,    44,    45,    16,    17,    44,
      19,    16,    51,    36,    19,    44,    51,    36,   108,    46,
      43,   108,   108,   143,    29,   159,    46,    36,   162,    13,
      51,    36,    15,    37,    43,    44,    16,    18,    43,    44,
      49,    50,    51,    41,    49,    50,    51,    44,     3,     4,
       5,     6,    49,    50,    51,   144,   146,    17,   147,     3,
       4,     5,     6,    19,    38,    39,    40,    60,   114,   159,
      44,   148,   162,    28,    18,    -1,    -1,    51,     3,     4,
       5,     6,     3,     4,     5,     6,    52,    -1,     7,     8,
      15,    44,    45,    14,    13,    -1,    49,    50,    51,    30,
      31,    32,    33,    34,    35,    31,    32,    33,    34,    35,
      32,    33,    34,    35,    24,    25,    26,    27,    94,    95,
      96,    97,    99,   100,   101,   102,    32,    33,    34
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,    30,    31,    32,    33,    34,    35,    55,    56,    57,
      58,    59,    60,    61,    62,    82,    83,    84,    85,    86,
     100,    94,    92,    87,    63,   105,     0,    57,    58,    59,
      60,    61,    44,    45,    49,    50,    51,   102,   103,   104,
     106,    96,   104,   106,    44,    97,    98,    44,    88,    99,
      48,    64,    65,   104,   106,    36,    45,    46,    46,    16,
      19,    29,    36,    43,    66,    67,   101,   103,   104,   104,
      93,    89,    90,    68,   102,    68,    89,   104,     6,    20,
      21,    22,    23,    69,    24,    25,    26,    27,    70,    36,
      43,    95,   104,   106,     3,     4,     5,     6,   106,     9,
      10,    11,    12,    16,    17,    19,    91,   101,     6,    14,
      18,    28,   102,    71,    71,   104,    90,    90,    90,    90,
      91,    91,    91,    91,    89,    89,    89,     7,     8,    13,
     102,    53,    72,    74,    89,    72,    14,    15,    18,    51,
      71,    37,    75,    47,    76,    77,    78,    89,    42,   106,
      38,    39,    40,    73,    79,    80,   104,   106,    77,    41,
      17,    80,    81,    15,    80
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    54,    55,    56,    56,    57,    57,    58,    58,    59,
      59,    60,    60,    61,    62,    63,    63,    64,    64,    65,
      66,    66,    66,    66,    67,    68,    68,    69,    69,    69,
      69,    70,    70,    70,    70,    71,    71,    72,    72,    73,
      73,    73,    73,    74,    75,    75,    76,    76,    77,    78,
      78,    79,    79,    80,    81,    81,    82,    83,    84,    85,
      86,    87,    87,    88,    89,    89,    89,    89,    89,    90,
      90,    91,    91,    91,    91,    91,    91,    91,    91,    91,
      91,    91,    92,    92,    93,    93,    94,    94,    95,    96,
      97,    98,    99,   100,   100,   101,   101,   101,   101,   101,
     102,   102,   103,   103,   104,   104,   105,   105,   106,   106
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     2,     1,     2,     1,     2,     1,     2,
       1,     2,     1,     1,     2,     0,     2,     6,     5,     1,
       1,     3,     3,     3,     3,     1,     3,     1,     1,     1,
       1,     1,     1,     1,     1,     0,     2,     0,     2,     1,
       1,     1,     0,     4,     0,     3,     1,     3,     2,     0,
       2,     5,     3,     1,     0,     2,     3,     3,     3,     2,
       2,     0,     2,     4,     1,     3,     3,     3,     3,     0,
       2,     1,     3,     2,     2,     2,     2,     2,     2,     3,
       3,     3,     0,     2,     0,     2,     0,     2,     1,     1,
       4,     1,     1,     0,     2,     2,     2,     3,     1,     1,
       3,     1,     1,     1,     1,     1,     0,     2,     1,     2
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
        case 2:
#line 196 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {}
#line 1598 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 17:
#line 223 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // If this rule didn't have variables, display it. Otherwise iterate
  // through its variable value combinations and display the rule using the
  // different combinations.
  try
    {
      if (rule_variables.empty())
	{ *output << rule_symbol_vector.replace_variables(); }
      else
	{
	  for (RuleVariables::const_iterator it = rule_variables.begin();
	       it != rule_variables.end();
	       ++it)
	    {
	      it.set_values(variable_value_map);
	      *output << rule_symbol_vector.replace_variables();
	    }
	}
    }
  catch (const UnequalSetSize &)
    {
      std::string error
	("Variable rules with keyword matched have to have equal length "
	 "variable value lists.");
      htwolcpre1error(error.c_str());
      HFST_THROW(HfstException);
    }
  // Clear all containers, so that we'll be ready to handle the next rule.
  rule_symbol_vector.clear();
  variable_value_map.clear();
  rule_variables.clear();
}
#line 1635 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 18:
#line 257 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  *output << rule_symbol_vector.replace_variables();

  // Clear all containers, so that we'll be ready to handle the next rule.
  rule_symbol_vector.clear();
  variable_value_map.clear();
  rule_variables.clear();
}
#line 1648 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 19:
#line 267 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // Add the rule name to rule_symbol_vector.
  reduce_queue();
}
#line 1657 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 39:
#line 299 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    { matcher_queue.push_back(MATCHED); }
#line 1663 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 40:
#line 301 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    { matcher_queue.push_back(MIXED); }
#line 1669 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 41:
#line 303 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    { matcher_queue.push_back(FREELY); }
#line 1675 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 42:
#line 305 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    { matcher_queue.push_back(FREELY); }
#line 1681 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 48:
#line 318 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // Set variable block matcher.
  rule_variables.set_matcher
    (matcher_queue.empty() ? FREELY : matcher_queue.get_front_and_pop());
}
#line 1691 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 51:
#line 329 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    { set_variable_values(); }
#line 1697 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 52:
#line 331 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    { set_variable_values(); }
#line 1703 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 53:
#line 334 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    { reduce_queue(true); }
#line 1709 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 72:
#line 365 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  htwolcpre1_symbol_queue.front() =
    std::string("__HFST_TWOLC_NUMBER=") + htwolcpre1_symbol_queue.front();
  reduce_queue();
}
#line 1719 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 88:
#line 390 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // Push the set_symbol into latest_set, which contains symbols in the next
  // set which will be defined.
  if (sets.find(get_symbol_queue_front()) != sets.end())
    {
      for (std::vector<std::string>::iterator it =
	     set_symbols
	     ["__HFST_TWOLC_SET_NAME=" + get_symbol_queue_front()].begin();
	   it != set_symbols
	     ["__HFST_TWOLC_SET_NAME=" + get_symbol_queue_front()].end();
	   ++it)
	{
	  *output << *it << " ";
	  latest_set.push_back(*it);
	}
      pop_symbol_queue();
    }
  else
    {
      latest_set.push_back(unescape(get_symbol_queue_front()));
      reduce_queue();
    }
}
#line 1747 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 89:
#line 415 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    { reduce_queue(); }
#line 1753 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 90:
#line 418 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // Store the set symbols of the set whose name is set_name into set_symbols.
  set_symbols[set_name] = latest_set;
  latest_set.clear();
}
#line 1763 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 91:
#line 425 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // Store the set name in sets and push it at the back of
  // symbol_queue.
  sets.insert(get_symbol_queue_front());
  get_symbol_queue_front() =
    "__HFST_TWOLC_SET_NAME=" + get_symbol_queue_front();
  set_name = get_symbol_queue_front();
  reduce_queue();
}
#line 1777 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 92:
#line 436 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // Store the definition name in definitions and push it at the back of
  // symbol_queue.
  definitions.insert(get_symbol_queue_front());
  get_symbol_queue_front() =
    "__HFST_TWOLC_DEFINITION_NAME=" + get_symbol_queue_front();
  reduce_queue();
}
#line 1790 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 95:
#line 450 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // For pairs "X:" and "X:?".
  // Reduce the first three symbols "X", "__HFST_TWOLC_:" and "__HFST_TWOLC_?"
  // from symbol_queue.
  reduce_symbol_pair(true);
}
#line 1801 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 96:
#line 457 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // For pairs ":X".
  // Push a "__HFST_TWOLC_?" onto symbol_queue.
  // Reduce the three first symbols "__HFST_TWOLC_?", "__HFST_TWOLC_:" and "X"
  // from symbol_queue.
  htwolcpre1_symbol_queue.push_front("__HFST_TWOLC_?");
  reduce_symbol_pair(true);
}
#line 1814 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 97:
#line 466 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // For pairs "X:Y".
  // Reduce the first three symbols "X", "__HFST_TWOLC_:" and "Y" from
  // symbol_queue.
  reduce_symbol_pair(true);
}
#line 1825 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 98:
#line 473 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // For pairs ":" and ":?".
  // Push a "__HFST_TWOLC_?" onto symbol_queue.
  // Reduce the three first symbols "__HFST_TWOLC_?", "__HFST_TWOLC_:" and
  // "__HFST_TWOLC_?" from symbol_queue.
  htwolcpre1_symbol_queue.push_front("__HFST_TWOLC_?");
  reduce_symbol_pair();
}
#line 1838 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 99:
#line 482 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // For pairs "X".
  // Push "X" and "__HFST_TWOLC_:" on top of symbol_queue.
  // Reduce the first three symbols "X", "__HFST_TWOLC_:" and "X" from
  // symbol_queue.
  std::string symbol = get_symbol_queue_front();

  // Add the colon and output symbol.
  htwolcpre1_symbol_queue.push_front("__HFST_TWOLC_:");
  htwolcpre1_symbol_queue.push_front(symbol);
  reduce_symbol_pair();
}
#line 1855 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 100:
#line 497 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // For pairs "X:Y".
  // Reduce the first three symbols "X", "__HFST_TWOLC_:" and "Y" from
  // symbol_queue.
  reduce_symbol_pair();
}
#line 1866 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 101:
#line 504 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    {
  // For pairs "X".
  // Push "X" and "__HFST_TWOLC_:" on top of symbol_queue.
  // Reduce the first three symbols "X", "__HFST_TWOLC_:" and "X" from
  // symbol_queue.
  std::string symbol = get_symbol_queue_front();
  htwolcpre1_symbol_queue.push_back("__HFST_TWOLC_:");
  htwolcpre1_symbol_queue.push_back(symbol);
  reduce_symbol_pair();
}
#line 1881 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;

  case 107:
#line 525 "htwolcpre1-parser.yy" /* yacc.c:1646  */
    { pop_symbol_queue(); }
#line 1887 "htwolcpre1-parser.cc" /* yacc.c:1646  */
    break;


#line 1891 "htwolcpre1-parser.cc" /* yacc.c:1646  */
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
#line 530 "htwolcpre1-parser.yy" /* yacc.c:1906  */


// Print warning.
void htwolcpre1warn(const char * warning)
{ htwolcpre1_input_reader.warn(warning); }

// Print error message and throw exception.
void htwolcpre1error(const char * text)
{
  htwolcpre1_input_reader.error(text);
  *output << "__HFST_TWOLC_DIE";
  HFST_THROW(HfstException);
}

// Set the variable of this variable initialization and set its values.
// If its value list contains set names, replace them by the set elements.
void set_variable_values(void)
{
  rule_variables.set_variable(variable_vector.front());
  for (StringVector::const_iterator it = variable_vector.begin()+1;
       it != variable_vector.end();
       ++it)
    {
      if (set_symbols.has_key(*it))
	{ rule_variables.add_values(set_symbols[*it]); }
      else
	{ rule_variables.add_value(*it); }
    }
  variable_vector.clear();
}

// Pop the queue three times: once for the input symbol, once for the pair
// separator and once for the output symbol.
void reduce_symbol_pair(bool no_definitions)
{
  if (no_definitions)
    {
      if (definitions.has_element(get_symbol_queue_front()))
	{
	  std::string def = get_symbol_queue_front();
	  std::string error =
	    "Definition name " + def + " can't be used in pair expressions " +
	    def + ":, :" + def + " and " + def + ":" + def + ".";
	  
	  htwolcpre1error(error.c_str());
	}
    }

  reduce_queue();
  reduce_queue();

  if (no_definitions)
    {
      if (definitions.has_element(get_symbol_queue_front()))
	{
	  std::string def = get_symbol_queue_front();
	  std::string error =
	    "Definition name " + def + " can't be used in pair expressions " +
	    def + ":, :" + def + " and " + def + ":" + def + ".";
	  
	  htwolcpre1error(error.c_str());
	}
    }

  reduce_queue();
}

// Increase line counter for every symbol "__HFST_TWOLC_\\n", which is
// encountered.
void increase_line_counter(void)
{
  while (! htwolcpre1_symbol_queue.empty() &&
	 htwolcpre1_symbol_queue.front() == "__HFST_TWOLC_\\n")
    {
      ++htwolcpre1_line_number;
      htwolcpre1_symbol_queue.pop_front();
    }
}

// First pop all "__HFST_TWOLC_\\n" in symbol_queue, while incrementing
// line_counter. Then pop the first element != "__HFST_TWOLC_\\n" in
// symbol_queue.
void pop_symbol_queue(void)
{
  increase_line_counter();
  htwolcpre1_symbol_queue.pop_front();
}

// First pop all "__HFST_TWOLC_\\n" in symbol_queue, while incrementing
// line_counter. Then return a reference to the first element
// != "__HFST_TWOLC_\\n" in symbol_queue.
std::string &get_symbol_queue_front(void)
{
  increase_line_counter();
  return htwolcpre1_symbol_queue.front();
}

// Decide what to do with the next symbol in symbol_queue.
void reduce_queue(bool variable_symbol)
{
  increase_line_counter();
  // Test whether the next symbol is a set name and label it a set if it is.
  if (sets.has_element(get_symbol_queue_front()))
    {  get_symbol_queue_front() =
	std::string("__HFST_TWOLC_SET_NAME=") + get_symbol_queue_front(); }

  // Test whether the next symbol is a definition name and label it a
  // definition if it is.
  if (definitions.has_element(get_symbol_queue_front()))
    { get_symbol_queue_front() =
      std::string("__HFST_TWOLC_DEFINITION_NAME=") + get_symbol_queue_front();}

  // Unescape the escaped characters in the symbol.
  get_symbol_queue_front() = unescape(get_symbol_queue_front());
  
  // We treat different symbols differently:
  //
  // 1. We display symbols, which aren't part of a rule.
  // 2. We push back rule symbols into rule_symbol_vector, which stores
  //    string representations of rules.
  // 3. We push back variable symbols into rule_symbol_vector, which stores
  //    rule-variable names and values.
  if (! variable_symbol)
    {
      if (! htwolcpre1_rules_start)
	{
	  *output << get_symbol_queue_front() << " ";
	  pop_symbol_queue();
	}
      else
	{
	  rule_symbol_vector.push_back
	    (StringVector(get_symbol_queue_front()));
	  pop_symbol_queue();
	}
    }
  else
    {
      variable_vector.push_back(get_symbol_queue_front());
      pop_symbol_queue();
    }
}

