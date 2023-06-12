#include <stdio.h>

extern int yyparse(void);
extern FILE* yyin;
extern int yylineno;

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Please provide an input file.\n");
        return 1;
    }

    FILE* inputFile = fopen(argv[1], "r");
    if (!inputFile) {
        printf("Failed to open input file.\n");
        return 1;
    }

    yyin = inputFile;
    yyparse();

    fclose(inputFile);
    return 0;
}


// flex lexer.l
// gcc lex.yy.c -o lexer
// bison -d grammar.y
// gcc grammar.tab.c -o parser
// flex lexer.l && bison -d grammar.y && gcc main.c lex.yy.c grammar.tab.c -o main