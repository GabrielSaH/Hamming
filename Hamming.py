
from functools import reduce
import operator as op


def onzeParaHammingSa(onze):
    bitEm16 = ["*"] * 16  #cria uma lista vazia com 16bits
    potencias2 = 4
    posicao_Onze = 0
    grupo1, grupo2, grupo3, grupo4 = [], [], [], []   # criando 4 listas vazias para cada grupo
    pariedadeg, pariedadeg1, pariedadeg2, pariedadeg3, pariedadeg4 = 0, 0, 0, 0, 0  # criando 5 variaveis numericas todas = 0
    for posicao, i in enumerate(bitEm16):
            if posicao == potencias2: # vai pular o 4
                potencias2 *= 2  # tranforma o 4 na proxima potencia de 2 e assim sucessivamente
            elif posicao > 2:    # pula a posiçao 0,1,2 (as primeiras potencias de dois)
                bitEm16[posicao] = onze[posicao_Onze]   # caso nao seja potencia de dois copia o numero mais a direita do numero original
                posicao_Onze += 1    
    
    
    for posicaoMatrix, resultado in enumerate(bitEm16):
        posicaoMatrixBin = [int(i) for i in bin(posicaoMatrix) if i != "b"] # quando usamos a funcao bin o python add um b a mais, isso remove ele
        while len(posicaoMatrixBin) < 4: # enquanto o binario tiver menos de 4 digitos
            posicaoMatrixBin.insert(0, 0) # adicionar 0 no digito mais a esquerda
        if len(posicaoMatrixBin) > 4: # caso ele tenha mias de 4 digitos retira o digito mais a esquerda
            posicaoMatrixBin.pop(0)
        if posicaoMatrixBin[0]: # caso o primeiro digito seja 1 adicione no grupo 4
            grupo4.append(posicaoMatrix)
        if posicaoMatrixBin[1]:  # caso o segundo digito seja 1 adicione no grupo 3
            grupo3.append(posicaoMatrix)
        if posicaoMatrixBin[2]:  # caso o terceiro digito seja 1 adicione no grupo 2
            grupo2.append(posicaoMatrix)
        if posicaoMatrixBin[3]:  # caso o quarto digito seja 1 adicione no grupo 1
            grupo1.append(posicaoMatrix)
        # isso de adicionar em cada grupo é um padrao especial do codigo de hamming, tem q checar o video la para entender pq funciona 

    liderG1 = grupo1.pop(0)  # o lider vai ser sempre o primeiro digito do grupo
    for posicaoP in grupo1:
        pariedadeg1 = pariedadeg1 ^ int(bitEm16[posicaoP]) # ^ é o comando para checar pariedade de bits no python
    bitEm16[liderG1] = pariedadeg1  # bitEm16 na posiçao do primeiro digito de cada grupo é igual a pariedade do grupo

    liderG2 = grupo2.pop(0)
    for posicaoP in grupo2:
        pariedadeg2 = pariedadeg2 ^ int(bitEm16[posicaoP])
    bitEm16[liderG2] = pariedadeg2

    liderG3 = grupo3.pop(0)
    for posicaoP in grupo3:
        pariedadeg3 = pariedadeg3 ^ int(bitEm16[posicaoP])  
    bitEm16[liderG3] = pariedadeg3
    
    liderG4 = grupo4.pop(0)
    for posicaoP in grupo4:
        pariedadeg4 = pariedadeg4 ^ int(bitEm16[posicaoP])
    bitEm16[liderG4] = pariedadeg4


    for im, posicaom in enumerate(bitEm16): # checando a pariedade do grupo todo para adicionar isso na posiçao 0
        if im == 0: 
            continue
        pariedadeg = pariedadeg ^ int(posicaom)
    bitEm16[0] = pariedadeg
    return(bitEm16)
            



def BinarioParaHamming(binarioCompleto):
    binarioCompletoTemp = [i for i in binarioCompleto] # tranforma o binario original para uma lista
    binarioFinal = ""    # string vazia q usaremos mais tarde
    while len(binarioCompletoTemp) >= 11: # 11 é o numero de bits de data q vai em um hamming de 16 bits
        strSemAntErro = binarioCompletoTemp[0:11] # tem que fazer de 11 em 11
        strComAntErro = onzeParaHammingSa(strSemAntErro)  # joga na funcao de fazer anti erro
        strTemp = "".join(str(e) for e in strComAntErro) # joga o resultado em uma string
        binarioFinal = binarioFinal + strTemp # adiciona tudo numa string final
        del(binarioCompletoTemp[0:11]) # deleta a parte do binario q ja foi feita
    if 11 > len(binarioCompletoTemp) > 0: # caso o binario tenha menos de 11 bits de data para armazenar
        strTemp = "".join(str(e) for e in binarioCompletoTemp)
        binarioFinal = binarioFinal + strTemp # so adiciona os ultimos bits sem ter ant erro
    return binarioFinal


def HammingParaBinario(bits):
    erros = [] # string com a posiçao dos erros
    grupo = 0 
    bitsTemp = "0000000000000000000000"  # string com qlqr coisa so para substituir depois
    bitsLista = [int(i) for i in bits] # transformando o bits para uma lista de bits
    mensagemFinal = ""
    while len(bitsLista) >= 16:  # enquanto a lista for maior ou igual a 16
        temp = ""
        grupo += 1  # o grupo se refere a conjunto de digitos de 16 bits
        bitsTemp = bitsLista[0:16] # os primeiros 16 bits da lista
        posicao = (reduce(op.xor, [i for i, bit in enumerate(bitsTemp) if bit])) # isso usa a funcao reduca para fazer o xor dos bits, esse xor deveria dar qual posicao tem erro
        if int(posicao): # caso a posiçao nao seja zero, ou seja, caso tenha erros
            bitsTemp[posicao] = int(not bitsTemp[posicao]) # troca o bit na posicao com erro pelo inverso (0 vira 1 e 1 vira 0)
            erros.append([grupo, posicao]) # guarda a posicao onde o erro estava
        del(bitsTemp[8]) #remove os bits de pariedade
        del(bitsTemp[4]) #remove os bits de pariedade
        del(bitsTemp[2]) #remove os bits de pariedade
        del(bitsTemp[1]) #remove os bits de pariedade
        del(bitsTemp[0]) #remove os bits de pariedade
        temp = "".join(str(i) for i in bitsTemp) # string temp para guardar o resultado
        mensagemFinal = mensagemFinal + temp  # adiciona o resultado na mensagem final
        del(bitsLista[0:16]) # remove os bits ja trabalhados
    if len(bitsLista) > 0: # caso a lista de bits seja menor que 16 mas ainda maior que 0
        mensagemFinal = mensagemFinal + "".join([str(i) for i in bitsLista]) # so coloca oq restou no final da mensagem


    return (mensagemFinal, erros) # retorna a mensagem e a posiçao dos erros



def main():
    interface = int(input("hamming para binario [1]   |   binario para hamming [2]   : "))
    if interface == 1:
        variavel = input('qual o hamming?  ')
        mensagemFinal, erros = HammingParaBinario(variavel)
        if len(erros) > 0:
            print(f'Mensagem final: \n {mensagemFinal}')
            print(f'posica dos erros encontrados: \n {erros}')
        elif len(erros) == 0:
            print(f'Mensagem final: \n {mensagemFinal}')
            print(f'Nao foram encontrados erros')

    if interface == 2:
        variavel = input('qual a mensagem em binario a ser aplicado o hamming?  ')
        mensagemFinal = BinarioParaHamming(variavel)
        print(f'\n \n A mensagem com o hamming ficou: \n {mensagemFinal}')
if __name__ == '__main__':
    main()
