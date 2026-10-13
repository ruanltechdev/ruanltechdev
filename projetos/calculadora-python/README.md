# Calculadora Pro — Python + Tkinter

Aplicação desktop de calculadora desenvolvida em Python com interface gráfica Tkinter.

## Funcionalidades

- Operações de adição, subtração, multiplicação e divisão
- Números decimais, parênteses e porcentagem
- Potência, quadrado e raiz quadrada
- Botão de troca de sinal, limpar e apagar último caractere
- Histórico das últimas 100 operações, com opção de limpar
- Atalhos de teclado: `Enter` calcula, `Esc` limpa e `Backspace` apaga
- Tratamento de expressões inválidas, divisão por zero e raiz de número negativo
- Avaliação matemática segura com análise de AST, sem usar `eval()`

## Requisitos

- Python 3.10 ou superior
- Tkinter (normalmente incluído na instalação do Python para Windows)

## Como executar

1. Instale o Python e confirme que a opção Tcl/Tk foi instalada.
2. Baixe ou clone este repositório.
3. Abra o terminal na pasta do projeto.
4. Execute:

```bash
python calculadora.py
```

## Estrutura

```text
calculadora-python/
├── calculadora.py
├── README.md
├── .gitignore
└── screenshots/
```

## Observações

- O histórico fica na memória enquanto a aplicação está aberta; ele não é salvo após fechar o programa.
- A avaliação de expressões permite somente números e operadores matemáticos previstos no código.
- O projeto foi feito com a biblioteca padrão do Python, sem dependências externas.

## Próximas melhorias

- Testes automatizados para a lógica matemática
- Persistência do histórico em arquivo
- Empacotamento para distribuição como executável
