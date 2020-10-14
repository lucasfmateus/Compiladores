# Compiladores
Trabalhos desenvolvidos para a disciplina de Compiladores do curso
de Bacharelado em Ciência da Computação da Universidade Tuiuti do Paraná.

## Autor

- Lucas Ferreira Mateus e Felipe Dias Pereira

## Descrição

Implementação da Analise Léxica e Sintática, de uma linguagem desenvolvida exclusivamente para a matéria.

## ANALISADOR LEXO 

### INT/REAL - ID - STRING - CARACTER
https://imgur.com/rbIUURh

- IDs aceitam qualquer caracter, é validado após identificacao de um separador válido ou algum caracter não pertencente ao UTF-16, antes da sua validação é checado se pertence a uma lista de palavras reservadas; 

### OPERADORES
https://imgur.com/oOCWFgA

- No código o número de estados foi otimizado devido a possibilidade de trabalhar com o lexema atual em cada estado;
