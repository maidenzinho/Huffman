# Huffman

Trabalho Final – Algoritmo de Huffman (Python)

Arquivos:
- huffman.py      -> Código-fonte completo do programa
- exemplo.txt     -> Arquivo de texto simples para teste
- README.md      -> Este arquivo com instruções de uso
- README.txt      -> Caso não consigo abrir o ".md"

Requisitos:
- Python 3 instalado (recomendado 3.9 ou superior)

Como executar:
1) Pelo terminal, entre na pasta onde estão os arquivos.
2) Execute:
   python huffman.py
   (ou: python3 huffman.py)

   Opcionalmente você pode já passar um arquivo texto:
   python huffman.py exemplo.txt

Menu do programa:
1 - Ler arquivo texto
    - Solicita o caminho de um arquivo .txt e carrega todo o conteúdo
      na memória.

2 - Gerar e imprimir tabela de frequências
    - Calcula quantas vezes cada caractere (byte) aparece no arquivo.
    - Imprime a tabela ordenada por frequência decrescente.

3 - Gerar e imprimir árvore de Huffman
    - Constrói a árvore de Huffman a partir da tabela de frequências.
    - Imprime a árvore de forma textual (pré-ordem com indentação).

4 - Gerar e imprimir tabela de códigos
    - Gera os códigos binários (0/1) para cada caractere.
    - Imprime a tabela: símbolo -> código Huffman.

5 - Compactar arquivo (gerar .huff)
    - Usa o arquivo carregado e gera um arquivo comprimido
      no formato:
      - assinatura "HUF1"
      - tabela de frequências
      - quantidade de bits de padding
      - dados comprimidos
    - O nome de saída deve terminar com .huff (se não terminar, o
      programa adiciona automaticamente).

6 - Descompactar arquivo (.huff -> _recuperado.txt)
    - Solicita o caminho de um arquivo .huff gerado por este programa.
    - Reconstrói a árvore a partir da tabela de frequências contida
      no próprio .huff.
    - Decodifica todos os dados e grava um novo arquivo texto com
      o sufixo "_recuperado.txt".
    - O texto recuperado deve ser idêntico ao original (UTF-8).

7 - Sair
    - Encerra o programa.

Observações importantes:
- O programa trata o arquivo de entrada como texto UTF-8.
- A tabela de frequências e a árvore são sempre recalculadas a partir
  do conteúdo carregado.
- A descompactação NÃO depende de o arquivo original estar carregado:
  todas as informações necessárias estão dentro do .huff.

Sugestão para apresentação:
- Usar o exemplo.txt ou um arquivo próprio com várias repetições de
  caracteres para demonstrar maior compressão.
- Mostrar ao professor:
  1) Leitura do arquivo.
  2) Impressão da tabela de frequências.
  3) Impressão da árvore.
  4) Impressão dos códigos.
  5) Compactação do arquivo.
  6) Descompactação e comparação do arquivo recuperado com o original.
