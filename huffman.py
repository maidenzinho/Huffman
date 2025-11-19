"""
Implementação do algoritmo de Huffman para compressão e descompressão de arquivos.

Trabalho de Resolução de Problemas Estruturados em Computação / Huffman.
"""

import sys
import os
import heapq
from typing import Dict, Optional, Tuple, List

# =========================
# Estruturas de dados
# =========================

class NoHuffman:
    """Nó da árvore de Huffman."""
    def __init__(self, freq: int, simbolo: Optional[int] = None,
                 esquerdo: Optional['NoHuffman'] = None,
                 direito: Optional['NoHuffman'] = None):
        self.freq = freq
        self.simbolo = simbolo  # byte (0-255) quando for folha
        self.esquerdo = esquerdo
        self.direito = direito

    def __lt__(self, other: 'NoHuffman') -> bool:
        # Necessário para a fila de prioridade (heapq)
        return self.freq < other.freq

    def eh_folha(self) -> bool:
        return self.simbolo is not None


# =========================
# Classe principal
# =========================

class Huffman:
    """Classe que encapsula a lógica de Huffman e o estado atual."""

    def __init__(self) -> None:
        self.texto: Optional[str] = None
        self.bytes_dados: Optional[bytes] = None
        self.tabela_freq: Optional[Dict[int, int]] = None
        self.raiz: Optional[NoHuffman] = None
        self.codigos: Optional[Dict[int, str]] = None

    # -------------------------
    # Utilitários
    # -------------------------

    @staticmethod
    def _repr_simbolo(b: int) -> str:
        """Representação amigável de um byte para impressão."""
        ch = chr(b)
        if ch == ' ':
            return "' ' (ESPAÇO)"
        if ch == '\n':
            return "'\\n' (QUEBRA LINHA)"
        if ch == '\t':
            return "'\\t' (TAB)"
        if ch.isprintable():
            return f"'{ch}'"
        return f"(byte {b})"

    # -------------------------
    # 1) Ler arquivo
    # -------------------------

    def ler_arquivo(self, caminho: str) -> None:
        if not os.path.isfile(caminho):
            raise FileNotFoundError(f"Arquivo '{caminho}' não encontrado.")

        with open(caminho, "r", encoding="utf-8") as f:
            self.texto = f.read()

        # Armazenamos também em bytes (para suportar qualquer caractere UTF-8)
        self.bytes_dados = self.texto.encode("utf-8")

        # Resetar estruturas relacionadas
        self.tabela_freq = None
        self.raiz = None
        self.codigos = None

        # Exibindo o conteúdo do arquivo no terminal
        print(f"Conteúdo do arquivo '{caminho}':")
        print(self.texto)
        print("\n===================================================\n")

    # -------------------------
    # 2) Tabela de frequências
    # -------------------------

    def gerar_tabela_frequencia(self) -> Dict[int, int]:
        if self.bytes_dados is None:
            raise ValueError("Nenhum arquivo carregado. Use a opção 'Ler arquivo' primeiro.")

        freq: Dict[int, int] = {}
        for b in self.bytes_dados:
            freq[b] = freq.get(b, 0) + 1

        self.tabela_freq = freq
        return freq

    def imprimir_tabela_frequencia(self) -> None:
        if self.tabela_freq is None:
            self.gerar_tabela_frequencia()

        print("=== Tabela de Frequências (ordenada por frequência decrescente) ===")
        print(f"{'Símbolo':30} | {'Frequência':10}")
        print("-" * 45)
        itens_ordenados = sorted(self.tabela_freq.items(), key=lambda kv: (-kv[1], kv[0]))
        for b, fr in itens_ordenados:
            print(f"{self._repr_simbolo(b):30} | {fr:10d}")
        print()

    # -------------------------
    # 3) Construção da árvore
    # -------------------------

    def construir_arvore(self) -> NoHuffman:
        if self.tabela_freq is None:
            self.gerar_tabela_frequencia()

        if not self.tabela_freq:
            raise ValueError("Arquivo vazio: não há dados para construir a árvore.")

        heap: List[Tuple[int, int, NoHuffman]] = []
        contador = 0

        # Criar um nó para cada símbolo
        for b, fr in self.tabela_freq.items():
            no = NoHuffman(freq=fr, simbolo=b)
            heapq.heappush(heap, (fr, contador, no))
            contador += 1

        # Caso especial: apenas 1 símbolo no arquivo
        if len(heap) == 1:
            _, _, unico_no = heap[0]
            # Cria um nó "pai" fictício para manter a lógica uniforme
            raiz = NoHuffman(freq=unico_no.freq, esquerdo=unico_no, direito=None)
            self.raiz = raiz
            return raiz

        # Combina os nós até restar apenas a raiz
        while len(heap) > 1:
            freq1, _, no1 = heapq.heappop(heap)
            freq2, _, no2 = heapq.heappop(heap)
            pai = NoHuffman(freq=freq1 + freq2, esquerdo=no1, direito=no2)
            heapq.heappush(heap, (pai.freq, contador, pai))
            contador += 1

        self.raiz = heap[0][2]
        return self.raiz

    def _imprimir_arvore_rec(self, no: Optional[NoHuffman], prefixo: str = "") -> None:
        if no is None:
            return
        if no.eh_folha():
            print(f"{prefixo}* {self._repr_simbolo(no.simbolo)} ({no.freq})")
        else:
            print(f"{prefixo}* ({no.freq})")
            self._imprimir_arvore_rec(no.esquerdo, prefixo + "  0-")
            self._imprimir_arvore_rec(no.direito, prefixo + "  1-")

    def imprimir_arvore(self) -> None:
        if self.raiz is None:
            self.construir_arvore()

        print("=== Árvore de Huffman ===")
        self._imprimir_arvore_rec(self.raiz)
        print()

    # -------------------------
    # 4) Geração da tabela de códigos
    # -------------------------

    def gerar_codigos(self) -> Dict[int, str]:
        if self.raiz is None:
            self.construir_arvore()

        codigos: Dict[int, str] = {}

        def _gerar_rec(no: NoHuffman, caminho: str) -> None:
            if no.eh_folha():
                # Caso de apenas 1 símbolo na árvore, podemos ter caminho vazio
                codigos[no.simbolo] = caminho if caminho != "" else "0"
                return
            if no.esquerdo is not None:
                _gerar_rec(no.esquerdo, caminho + "0")
            if no.direito is not None:
                _gerar_rec(no.direito, caminho + "1")

        _gerar_rec(self.raiz, "")
        self.codigos = codigos
        return codigos

    def imprimir_codigos(self) -> None:
        if self.codigos is None:
            self.gerar_codigos()

        print("=== Tabela de Códigos de Huffman ===")
        print(f"{'Símbolo':30} | {'Código':20}")
        print("-" * 55)
        for b, codigo in sorted(self.codigos.items(), key=lambda kv: (kv[0])):
            print(f"{self._repr_simbolo(b):30} | {codigo:20}")
        print()

    # -------------------------
    # 5) Compactação
    # -------------------------

    @staticmethod
    def _bits_para_bytes(bits: str) -> Tuple[bytes, int]:
        """Converte uma string de bits em bytes. Retorna (dados, padding)."""
        if len(bits) == 0:
            return b"", 0

        padding = (8 - (len(bits) % 8)) % 8
        bits += "0" * padding

        dados = bytearray()
        for i in range(0, len(bits), 8):
            byte_str = bits[i:i+8]
            dados.append(int(byte_str, 2))

        return bytes(dados), padding

    @staticmethod
    def _bytes_para_bits(dados: bytes) -> str:
        """Converte bytes em uma string de bits."""
        return "".join(f"{b:08b}" for b in dados)

    def compactar(self, caminho_saida: str) -> None:
        if self.bytes_dados is None:
            raise ValueError("Nenhum arquivo carregado. Use a opção 'Ler arquivo' primeiro.")

        if self.tabela_freq is None:
            self.gerar_tabela_frequencia()
        if self.raiz is None:
            self.construir_arvore()
        if self.codigos is None:
            self.gerar_codigos()

        # Gerar string de bits para todo o arquivo
        bits = "".join(self.codigos[b] for b in self.bytes_dados)
        dados_codificados, padding = self._bits_para_bytes(bits)

        # Formato do arquivo .huff:
        # [4 bytes]  "HUF1" (assinatura / magic)
        # [4 bytes]  N = quantidade de símbolos distintos (uint32 big-endian)
        # N vezes:
        #   [1 byte] símbolo (0-255)
        #   [4 bytes] frequência (uint32 big-endian)
        # [1 byte] padding (0-7)
        # [resto] dados codificados

        freq = self.tabela_freq
        n = len(freq)

        with open(caminho_saida, "wb") as f:
            # Assinatura
            f.write(b"HUF1")
            # Quantidade de símbolos
            f.write(n.to_bytes(4, byteorder="big"))
            # Tabela de frequências
            for b, fr in freq.items():
                f.write(b.to_bytes(1, byteorder="big"))
                f.write(fr.to_bytes(4, byteorder="big"))
            # Padding
            f.write(padding.to_bytes(1, byteorder="big"))
            # Dados comprimidos
            f.write(dados_codificados)

    # -------------------------
    # 6) Descompactação
    # -------------------------

    @classmethod
    def descompactar_arquivo(cls, caminho_huff: str, caminho_saida: str) -> None:
        """Descompacta um arquivo .huff gerado por este programa."""
        if not os.path.isfile(caminho_huff):
            raise FileNotFoundError(f"Arquivo '{caminho_huff}' não encontrado.")

        with open(caminho_huff, "rb") as f:
            magic = f.read(4)
            if magic != b"HUF1":
                raise ValueError("Arquivo .huff inválido ou em formato desconhecido.")

            n_bytes = f.read(4)
            if len(n_bytes) < 4:
                raise ValueError("Arquivo .huff corrompido (tamanho da tabela).")

            n = int.from_bytes(n_bytes, byteorder="big")

            tabela_freq: Dict[int, int] = {}
            for _ in range(n):
                s = f.read(1)
                fr_bytes = f.read(4)
                if len(s) < 1 or len(fr_bytes) < 4:
                    raise ValueError("Arquivo .huff corrompido (entrada de tabela).")
                simbolo = s[0]
                fr = int.from_bytes(fr_bytes, byteorder="big")
                tabela_freq[simbolo] = fr

            padding_byte = f.read(1)
            if len(padding_byte) < 1:
                raise ValueError("Arquivo .huff corrompido (padding).")
            padding = padding_byte[0]

            dados_codificados = f.read()
            if len(dados_codificados) == 0 and sum(tabela_freq.values()) > 0:
                raise ValueError("Arquivo .huff corrompido (sem dados).")

        # Reconstruir a árvore de Huffman a partir da tabela de frequências
        h = cls()
        h.tabela_freq = tabela_freq
        raiz = h.construir_arvore()

        total_bytes_orig = sum(tabela_freq.values())

        # Converter os dados codificados em bits
        bits = cls._bytes_para_bits(dados_codificados)
        if padding > 0:
            bits = bits[:-padding]

        # Decodificar percorrendo a árvore
        resultado = bytearray()
        no_atual = raiz
        for bit in bits:
            if bit == "0":
                no_atual = no_atual.esquerdo
            else:
                no_atual = no_atual.direito

            if no_atual is None:
                raise ValueError("Erro na descompactação: navegação inválida na árvore.")

            if no_atual.eh_folha():
                simbolo = no_atual.simbolo
                resultado.append(simbolo)
                no_atual = raiz
                if len(resultado) == total_bytes_orig:
                    break

        dados_reconst = bytes(resultado)

        # Decodificar de volta para texto (UTF-8)
        try:
            texto_recuperado = dados_reconst.decode("utf-8")
        except UnicodeDecodeError:
            texto_recuperado = dados_reconst.decode("latin-1")

        with open(caminho_saida, "w", encoding="utf-8") as f_out:
            f_out.write(texto_recuperado)

# -------------------------
# Funções auxiliares para menu
# -------------------------

def mostrar_menu() -> None:
    print("========================================")
    print("     COMPRESSÃO HUFFMAN - MENU")
    print("========================================")
    print("1 - Ler arquivo texto")
    print("2 - Gerar e imprimir tabela de frequências")
    print("3 - Gerar e imprimir árvore de Huffman")
    print("4 - Gerar e imprimir tabela de códigos")
    print("5 - Compactar arquivo (gerar .huff)")
    print("6 - Descompactar arquivo (.huff -> _recuperado.txt)")
    print("7 - Sair")
    print("========================================")

def main():
    huff = Huffman()
    arquivo_carregado = False

    # Possibilidade de passar o arquivo de texto via argumento
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
        try:
            huff.ler_arquivo(caminho)
            arquivo_carregado = True
            print(f"Arquivo '{caminho}' carregado com sucesso via argumento.")
        except Exception as e:
            print(f"Erro ao carregar arquivo via argumento: {e}")

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            caminho = input("Informe o caminho do arquivo de texto: ").strip()
            try:
                huff.ler_arquivo(caminho)
                arquivo_carregado = True
                print(f"Arquivo '{caminho}' carregado com sucesso.")
            except Exception as e:
                print(f"Erro ao ler arquivo: {e}")

        elif opcao == "2":
            if not arquivo_carregado:
                print("Erro: Nenhum arquivo carregado. Carregue um arquivo primeiro.")
                continue
            try:
                huff.imprimir_tabela_frequencia()
            except Exception as e:
                print(f"Erro ao gerar/imprimir tabela de frequências: {e}")

        elif opcao == "3":
            if not arquivo_carregado:
                print("Erro: Nenhum arquivo carregado. Carregue um arquivo primeiro.")
                continue
            try:
                huff.imprimir_arvore()
            except Exception as e:
                print(f"Erro ao gerar/imprimir árvore de Huffman: {e}")

        elif opcao == "4":
            if not arquivo_carregado:
                print("Erro: Nenhum arquivo carregado. Carregue um arquivo primeiro.")
                continue
            try:
                huff.imprimir_codigos()
            except Exception as e:
                print(f"Erro ao gerar/imprimir tabela de códigos: {e}")

        elif opcao == "5":
            if not arquivo_carregado:
                print("Erro: Nenhum arquivo carregado. Carregue um arquivo primeiro.")
                continue
            caminho_saida = input("Informe o nome do arquivo de saída (.huff): ").strip()
            if not caminho_saida.endswith(".huff"):
                caminho_saida += ".huff"
            try:
                huff.compactar(caminho_saida)
                print(f"Arquivo compactado gerado: {caminho_saida}")
            except Exception as e:
                print(f"Erro ao compactar arquivo: {e}")

        elif opcao == "6":
            caminho_huff = input("Informe o caminho do arquivo .huff: ").strip()
            if not os.path.isfile(caminho_huff):
                print(f"Erro: Arquivo .huff '{caminho_huff}' não encontrado.")
                continue
            base, ext = os.path.splitext(caminho_huff)
            caminho_saida = base + "_recuperado.txt"
            try:
                Huffman.descompactar_arquivo(caminho_huff, caminho_saida)
                print(f"Arquivo descompactado gerado: {caminho_saida}")
            except Exception as e:
                print(f"Erro ao descompactar arquivo: {e}")

        elif opcao == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
