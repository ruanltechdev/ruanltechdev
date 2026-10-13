# Calculadora com Interface Gráfica — Python + Tkinter

Projeto pessoal de estudo para praticar Python e a criação de interfaces gráficas para desktop. A aplicação permite realizar cálculos em uma janela própria, usando botões ou o teclado.

> **Status:** versão inicial para portfólio. Quero continuar melhorando o código e acrescentar testes conforme evoluo nos estudos.

## Funcionalidades

- Operações básicas: adição, subtração, multiplicação e divisão
- Expressões com parênteses e números decimais
- Porcentagem, potência, quadrado e raiz quadrada
- Botões para limpar, apagar o último caractere e trocar o sinal
- Histórico das últimas 100 operações durante a execução
- Atalhos de teclado: `Enter` para calcular, `Esc` para limpar e `Backspace` para apagar
- Mensagens de erro para expressões inválidas, divisão por zero e raiz quadrada de número negativo

## Tecnologias e conceitos

- **Python 3**
- **Tkinter** para a interface gráfica
- Funções, classes e métodos
- Tratamento de erros e validação de expressões
- Módulos da biblioteca padrão, como `math`, `operator` e `ast`

A avaliação das expressões é feita por meio de uma lista de operações matemáticas permitidas, em vez de executar o texto digitado diretamente com `eval()`.

## Como executar

**Requisitos:** Python 3.10 ou superior, com Tkinter disponível.

1. Baixe ou clone o repositório.
2. Abra o terminal na pasta `projetos/calculadora-python`.
3. Execute:

```bash
python calculadora.py
```

Se o comando `python` não funcionar no Windows, tente `py calculadora.py`.

## Estrutura do projeto

```text
calculadora-python/
├── calculadora.py
├── README.md
├── .gitignore
└── screenshots/
```

## Limitações conhecidas

- O histórico fica apenas na memória e é apagado quando a aplicação é fechada.
- O projeto ainda não possui uma suíte de testes automatizados.
- A interface foi pensada inicialmente para uso em desktop.

## Próximos passos

- Criar testes automatizados para as operações matemáticas e os casos de erro
- Executar e verificar o comportamento em diferentes situações
- Adicionar capturas de tela da aplicação em funcionamento
- Melhorar a organização do código à medida que eu aprender novos conceitos

---

Este projeto faz parte da minha prática em Desenvolvimento de Sistemas. A ideia é aprender construindo, testar o que funciona, corrigir os problemas e registrar minha evolução.
