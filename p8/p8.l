%{
/* Declarations section */
int lines = 0, words = 0, chars = 0;
%}

%%
\n          { lines++; chars++; }              /* newline increases line and char count */
[ \t]+      { chars += yyleng; }              /* spaces/tabs are counted as characters */
[^ \t\n]+   { words++; chars += yyleng; }     /* words (any non-space sequence) */
.           { chars++; }                      /* count every other character */
%%

int main()
{
    yylex();   /* call the lexer */
    printf("\nLines: %d\nWords: %d\nCharacters: %d\n", lines, words, chars);
    return 0;
}

int yywrap()
{
    return 1;
}


/* 
lex file.l
cc lex.yy.c -o a.out
a.out < input.txt
*/
