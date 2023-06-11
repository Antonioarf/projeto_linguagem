%{
#include <stdio.h>
#include <stdlib.h>
#include "grammar.tab.h"
%}

%%

[ \t\n]                 ;

LOG           { prinf("LOG\n") ; return PRINT; }
STA           { prinf("STA\n") ; return ASSIGNMENT; }
FUNC          { prinf("FUNC\n") ; return FUNCTION; }
CEQ           { prinf("CEQ\n") ; return IF; }
ELSE          { prinf("ELSE\n") ; return ELSE; }
WHL           { prinf("WHL\n") ; return LOOP; }
RET           { prinf("RET\n") ; return FUNCTION_RETURN; }
JSR           { prinf("JMP\n") ; return FUNCTION_CALL }

[a-zA-Z_][a-zA-Z0-9_]*   { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+(\.[0-9]+)?        { yylval.num = atof(yytext); return NUMBER; }
"=="                     { return EQUAL; }
"<"                      { return LESS_THAN; }
">"                      { return GREATER_THAN; }
"<="                     { return LESS_THAN_OR_EQUAL_TO; }
">="                     { return GREATER_THAN_OR_EQUAL_TO; }
"+"                      { return PLUS; }
"-"                      { return MINUS; }
"*"                      { return TIMES; }
"/"                      { return DIVIDE; }
"("                      { return LEFT_PAREN; }
")"                      { return RIGHT_PAREN; }

[\+\-\*\/\(\)\{\}\n]     { return yytext[0]; }

.                        { return UNKNOWN; }

%%
