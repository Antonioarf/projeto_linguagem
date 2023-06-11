%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "grammar.tab.h"

extern int yylex();
void yyerror(const char *s) { printf("ERROR: %s\n", s); }
%}


%token IDENTIFIER NUMBER EQUAL LESS_THAN GREATER_THAN LESS_THAN_EQUAL GREATER_THAN_EQUAL GREATER_THAN_OR_EQUAL_TO LESS_THAN_OR_EQUAL_TO 

%start program

%%

BLOCK:
    STATEMENTS { printf("\nParsing complete.\n\n"); }
    ;

STATEMENTS:
    STATEMENT
    | STATEMENTS STATEMENT
    ;

STATEMENT:
    PRINT
    | ASSIGNMENT
    | FUNCTION
    | IF
    | LOOP
    ;

PRINT:
    LOG EXPRESSION { printf("\nFound print statement.\n\n"); }
    ;
ASSIGNMENT:
    STA IDENTIFIER EXPRESSION { printf("\nFound assignment statement.\n\n"); }
    ;
FUNCTION:
    FUNCTION_DEF | FUNCTION_CALL { printf("\nFound function.\n\n"); }
    ;
FUNCTION_DEF:
    FUNC FUNCTION_ID BLOCK RET { printf("\nFound function definition.\n\n"); }
    ;
FUNCTION_ID:
    IDENTIFIER PAR_LIST { printf("\nFound function identifier.\n\n"); }
    ;
PAR_LIST:
    PAR | PAR_LIST COMMA PAR { printf("\nFound parameter list.\n\n"); }
    ;
EXPRESSION:
    TERM | EXPRESSION PLUS | MINUS  TERM { printf("\nFound expression.\n\n"); }
    ;
TERM:
    FACTOR | TERM TIMES | DIVIDE FACTOR { printf("\nFound term.\n\n"); }
    ;
FACTOR:
    NUMBER | IDENTIFIER | LPAREN EXPRESSION RPAREN { printf("\nFound factor.\n\n"); }
    ;
CONDITION:
    EXPRESSION COMPARE EXPRESSION { printf("\nFound condition.\n\n"); }
    ;
COMPARE:
    EQUAL | LESS_THAN | GREATER_THAN | LESS_THAN_EQUAL | GREATER_THAN_EQUAL | GREATER_THAN_OR_EQUAL_TO | LESS_THAN_OR_EQUAL_TO { printf("\nFound comparison.\n\n"); }
    ;

IF:
    CEQ CONDITION STATEMENT { printf("\nFound if statement.\n\n"); }
    | CEQ CONDITION STATEMENT ELSE STATEMENT { printf("\nFound if-else statement.\n\n"); }
    ;

LOOP:
    WHILE CONDITION STATEMENT { printf("\nFound while loop.\n\n"); }
    ;


%%

int main(void) {
    yyparse();
    return 0;
}