from classes import Tabuleiro
from funcoes import manhattan, hamming, bfs, dfs, gulosa, a_estrela
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Solucionando 15-Puzzle')
    parser.add_argument('--dfs', type=int, help='Execute a pesquisa em profundidade (forneça um número inteiro para a profundidade máxima)')
    parser.add_argument('--bfs', action='store_true', help='Execute a busca em largura')
    parser.add_argument('--gulosa', type=int, choices=[1, 2], help='Execute a busca gulosa (1 -hamming; 2 -manhattan)')
    parser.add_argument('--a_estrela', type=int, choices=[1, 2], help='Execute a busca A* (1 -hamming; 2 -manhattan)')

    parser.add_argument('--input', '-i', help='Informe uma entrada para os testes')
    args = parser.parse_args()

    if args.input is None:
        estado_inicial = input("Ponto de partida:\n").split()
        estado_objetivo = input("Tabuleiro pronto:\n").split()
    else:
        try:
            numeros = []
            with open(args.input, "r") as f:
                linhas = f.lerlinhas()
                for linha in linhas:
                    numeros = numeros + linha.split()
            estado_inicial = numeros[:16]
            numeros = numeros[16:]
            estado_objetivo = numeros[:16]
        except FileNotFoundError:
            sys.stderr.write("Entrada inválida")
            sys.exit(1)

    estado_inicial = Tabuleiro(estado_inicial)
    estado_objetivo = Tabuleiro(estado_objetivo)
    print(estado_inicial)
    print(estado_objetivo)

    if estado_inicial == estado_objetivo:
        print("Tabuleiro já resolvido! :)")
        sys.exit(0)

    if estado_inicial.cap_soluc() ^ estado_objetivo.cap_soluc():
        print('Tabuleiro inválido.')
        sys.exit(1)

    if args.a_estrela is None and not args.bfs and args.dfs is None and not args.greedy is None:
        sys.stderr.write("Por favor, insira uma entrada válida! '-'")
        sys.stderr.write("Escolha um tipo de busca para a solução. ")
        sys.exit(1)

    if estado_inicial == estado_objetivo:
        print("O tabuleiro já está resolvido :) ")
        sys.exit(0)

    if args.bfs:
        print("BUSCA EM LARGURA:")
        jogadas, nos = bfs(estado_inicial, estado_objetivo)
        print(nos, "Indisponível.")
        if jogadas: print(" -> ".join(jogadas))
        else: print("Nenhuma solução encontrada :( ")

    if args.dfs is not None:
        if args.dfs < 0:
            parser.print_help(sys.stderr)
            sys.exit(1)
        print("BUSCA EM PROFUNDIDADE:")
        jogadas, nos = dfs(estado_inicial, estado_objetivo, args.dfs)
        print(nos, "Indisponível.")
        if jogadas: print(" -> ".join(jogadas))
        else: print("Nenhuma solução encontrada. :( ")
        
    if args.gulosa:
        print("BUSCA GULOSA:")
        comp = manhattan
        if args.a_estrela == 1: comp = hamming
        jogadas, nos = gulosa(estado_inicial, estado_objetivo, comp)
        print(nos, "Indisponível.")
        if jogadas: print(" -> ".join(jogadas))
        else: print("Nenhuma solução encontrada :(")

    if args.a_estrela:
        print("BUSCA A*:")
        comp = manhattan
        if args.a_estrela == 1: comp = hamming
        jogadas, nos = a_estrela(estado_inicial, estado_objetivo, comp)
        print(nos, "Indisponível.")
        if jogadas: print(" -> ".join(jogadas))
        else: print("Nenhuma solução encontrada :(.")

if __name__ == '__main__':
    main()