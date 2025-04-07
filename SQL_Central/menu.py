import sys
from pathlib import Path
import os
import time
sys.path.append(str(Path(__file__).resolve().parent / "central_atendimento"))
from central_atendimento.app.routes.ConsultarLimite import consultar_limite
from central_atendimento.app.routes.ConsultarStatusCartao import consultar_status_cartao
from central_atendimento.app.routes.AlterarStatusCartao import alterar_status_cartao


def limpar_tela():
    os.system('cls')

def main():
    while True:
        #limpar_tela()
        print("=== Central de Atendimento ===")
        print("1 - Consultar limite")
        print("2 - Verificar Status do Cartão")
        print("3 - Bloquear Cartão")
        print("4 - Desbloquear Cartão")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cliente_id = input("Digite o ID do cliente: ")
            consultar_limite(cliente_id)
            resp = input('Deseja voltar ao menu? [s]im ou [N]ão: ')
            if resp.upper() == 'N':
                break
            elif resp.upper() == 'S':
                print('Voltando...')
        elif opcao == "0":
            print("Encerrando...")
            break
        elif opcao == "2":
            cliente_id = input("Digite o ID do cliente: ")
            consultar_status_cartao(cliente_id)
            resp = input('Deseja voltar ao menu? [s]im ou [N]ão: ')
            if resp.upper() == 'N':
                break
            elif resp.upper() == 'S':
                print('Voltando...')

        elif opcao == "3":
            cliente_id = input("Digite o ID do cliente: ")
            alterar_status_cartao(cliente_id, "Bloqueado")
            resp = input('Deseja voltar ao menu? [s]im ou [N]ão: ')
            if resp.upper() == 'N':
                break
            elif resp.upper() == 'S':
                print('Voltando...')
        elif opcao == "4":
            cliente_id = input("Digite o ID do cliente: ")
            alterar_status_cartao(cliente_id, "Ativo")
            resp = input('Deseja voltar ao menu? [s]im ou [N]ão: ')
            if resp.upper() == 'N':
                break
            elif resp.upper() == 'S':
                print('Voltando...')
        else:
            print("Opção inválida.")
            time.sleep(2)
            limpar_tela()
    return print('Obrigado por entrar em contato com a Central !')

if __name__ == "__main__":
    main()
