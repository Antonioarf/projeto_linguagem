%{
#include <stdio.h>
#include <stdlib.h>
#include "grammar.tab.h"
%}


%%

"STA"                { printf("STA\n"); return STA_id; }
"LOG"                { printf("LOG\n"); return LOG_id; }
"FUNC"               { printf("FUNC\n"); return FUNC_id; }
"JMP"                { printf("JMP\n"); return JMP_id; }
"CEQ"                { printf("CEQ\n"); return CEQ_id; }
"ELSE"               { printf("ELSE\n"); return ELSE_id; }
"WHL"                { printf("WHL\n"); return WHL_id; }
"END"                { printf("END\n"); return END_id; }
"=="                 { printf("EQ\n"); return EQ_id; }
"<"                  { printf("LT\n"); return LT_id; }
">"                  { printf("GT\n"); return GT_id; }

"("                  { printf("LPAREN\n"); return LPAREN; }
")"                  { printf("RPAREN\n"); return RPAREN; }
"+"                  { printf("PLUS\n"); return PLUS; }
"-"                  { printf("MINUS\n"); return MINUS; }
"*"                  { printf("TIMES\n"); return TIMES; }
"/"                  { printf("DIVIDE\n"); return DIVIDE; }
"&&"                 { printf("AND\n"); return AND; }
"||"                 { printf("OR\n"); return OR; }
"!"                  { printf("NOT\n"); return NOT; }

","                  { printf("COMMA\n"); return COMMA; }

[0-9]+               { yylval = atoi(yytext); printf("NUM\n") ; return NUMBER; }
[a-zA-Z][a-zA-Z0-9_]* { yylval = strdup(yytext);printf("VAR\n") ;  return IDENTIFIER; }

[ \t\n]              ; /* Skip whitespace */

.                    { fprintf(stderr, "Invalid token: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}
