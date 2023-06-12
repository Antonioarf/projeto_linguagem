%{
#include <stdio.h>
#include <stdlib.h>

extern int yylex();
extern int yylineno;
extern char* yytext;
extern FILE* yyin;

void yyerror(const char* s) {
    fprintf(stderr, "Syntax error at line %d: %s\n", yylineno, s);
    exit(1);
}

%}

%token STA_id LOG_id FUNC_id JMP_id CEQ_id WHL_id END_id EQ_id LT_id GT_id ELSE_id COMMA AND OR NOT PLUS MINUS TIMES DIVIDE LPAREN RPAREN NEWLINE
token_type NUMBER IDENTIFIER

%%

program : BLOCK { printf("Valid program\n"); }
        ;

BLOCK :  statement_list 
      ;

statement_list : statement
               | statement_list statement
               ;


statement:  ASSIGNMENT
    | PRINT
    | FUNCTION_DEF
    | FUNCTION_CALL
    | IF
    | LOOP
    | NEWLINE
    ;

ASSIGNMENT : STA_id IDENTIFIER COMMA expression

           ;

PRINT : LOG_id expression
      ;

FUNCTION_DEF : FUNC_id FUNCTION_ID NEWLINE BLOCK END_id
             ;

FUNCTION_CALL : JMP_id FUNCTION_ID
              ;

FUNCTION_ID : IDENTIFIER COMMA par_list
            | IDENTIFIER
            ;

par_list : IDENTIFIER
         | par_list COMMA IDENTIFIER
         ;

IF : CEQ_id rel_expression NEWLINE BLOCK ELSE END_id
   | CEQ_id rel_expression NEWLINE BLOCK END_id
   ;

ELSE : ELSE_id NEWLINE BLOCK
     ;

LOOP : WHL_id rel_expression NEWLINE BLOCK END_id
     ;

rel_expression : expression
               | expression EQ_id expression
               | expression LT_id expression
               | expression GT_id expression
               ;

expression : term
           | expression PLUS term
           | expression MINUS term
           | expression OR term
           ;

term : factor
     | term TIMES factor
     | term DIVIDE factor
     | term AND factor
     ;

factor : PLUS factor
       | MINUS factor
       | NOT factor
       | NUMBER
       | LPAREN expression RPAREN
       | IDENTIFIER
       ;




%%

