import random
from random import randint

# 
# Função para Criar peças do jogo e 
# embaralhar as peças do dominó
#
def embaralhar_pecas():
    pecas = []
    for i in range(7):
        for j in range(i, 7):
            pecas.append((i, j))
    random.shuffle(pecas)
    return pecas

# Função para distribuir as peças entre os jogadores
def distribuir_pecas(pecas):
    jg1 = []
    jg2 = []
    for i in range(7):
        jg1.append(pecas.pop())
        jg2.append(pecas.pop())
    return jg1, jg2, pecas

# Função para imprimir a mão de um jogador
def imprimir_mao(jogador):
    print("Suas Peças:")
    for i, peca in enumerate(jogador):
        print(f"{i+1}: {peca}")

# Execução do código
'''
def jogar_peca(jogador):
    while True:
        if len(jogador) == 0:
            print(f"o jogador: {jogador} venceu!")
            break
        else:
            peca_valida = False
            for i in range(len(jogador)):
                if jogador[i]['lado1'] == pecasM[-1]['lado2'] or jogador[i]['lado2'] == pecasM[-1]['lado2']:
                    pecasM.append(jogador[i])
                    jogador.remove(jogador[i])
                    peca_valida = True
                    break
            if peca_valida:
                print("Uma peça foi jogada na mesa.")
                mostra_peca(pecasM)
            else:
                print("Nenhuma peça pode ser jogada.")
                break
'''
def verifica_mao(jogador_atual, mesa, peca_escolhida):
    #ver o começo da trilha
    if mesa[0][0] in list(map(lambda i: i[0], jogador_atual)) or \
        mesa[0][0] in list(map(lambda i: i[1], jogador_atual)):
        print("Para o começo da trilha há peças")
        #if mesa[0][0] == peca_escolhida
        mesa.insert(0, peca_escolhida)
        jogador_atual.remove(peca_escolhida)

    #ver o final da trilha
    elif mesa[len(trilha)-1][0] in list(map(lambda i: i[0], jogador_atual)) or \
        mesa[len(trilha)-1][0] in list(map(lambda i: i[1], jogador_atual)):
        print("Para o final da trilha há peças")
        mesa.append(peca_escolhida)
        jogador_atual.remove(peca_escolhida)
    else:
        print("precisa comprar peças!")


#jogar_peca(jg1)

def iniciar_jogo():
    mesa = []
    pecas = embaralhar_pecas()
    jg1, jg2, pecas_mesa = distribuir_pecas(pecas)

    print(f"peças do jogador 1: {jg1}")
    print(f"peças do jogador 1: {jg2}")
    
    mesa.append(pecas_mesa.pop())
    print(f"peças restantes: {pecas_mesa}")

    
    

    jogadores = [jg1, jg2]
    turno = random.randint(0, 1) # alterar
    pulou_vez = False

    while True:
        jogador_atual = jogadores[turno]
        print("=== Jogador", turno + 1, "===\n")
        imprimir_mao(jogador_atual)
        print(f"Peças na mesa: {mesa}")

        opcao = input("Digite o número da peça que deseja jogar (ou '0' para pular): ")
        if opcao == '0':
            pulou_vez = True
            print("Jogador", turno + 1, "pulou a vez.\n")
            turno = (turno + 1) % 2 
        else:
            opcao = int(opcao)
            if opcao < 1 or opcao > len(jogador_atual):
                print("Opção inválida.\n")
            else:
                peca_escolhida = jogador_atual[opcao - 1]
                print("Peça escolhida", peca_escolhida,"\n")
                verifica_mao(jogador_atual, mesa, peca_escolhida)
                pulou_vez = False
                if len(jogador_atual) == 0:
                    #vitoria se acabar as peças
                    print("Jogador", turno + 1, "venceu!")
                    break
            

            
iniciar_jogo()
