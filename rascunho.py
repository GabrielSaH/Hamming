def ArqParaHamming():
    arqInicial = input("qual o local do arquivo?")
    binarioArq = open(r"C:\Users\Gabriel\PycharmProjects\guppe\Trabalho_hamming\Binario.txt", "w")      
    
    melhorTamanhoHamming, contadorPotenciasDois = 8, 4                                               
    
    listNome = arqInicial.split(".")                                                                    
    des = "Destino." + listNome[1]                                                                       
    
    with open(arqInicial, "rb") as main: #, open(des, "wb") as file:
        mainTexto = main.read()
        tamanhoTotal = len(mainTexto * 8)
        while (melhorTamanhoHamming - contadorPotenciasDois) * 100_000 < tamanhoTotal:
            melhorTamanhoHamming = (melhorTamanhoHamming * 2)
            contadorPotenciasDois += 1

        y = 0
        listaBinario = []
        listaSublistas = []
        for byte in mainTexto:
            binario = bin(byte)[2:]
            
            if len(binario) < 8:
                    qntZeros = 8 - len(binario)                                                             
                    binarioNovo = (f'{"0" * qntZeros}{binario}')
            else:
                binarioNovo = binario
            for i in binarioNovo:
                listaBinario.append(i)
                

            while len(listaBinario) >= ((melhorTamanhoHamming - contadorPotenciasDois)):
                mensagem = listaBinario[0:(melhorTamanhoHamming - contadorPotenciasDois)]
                mensagemLista,tamanhoHamming = dataParaLista(mensagem)
                adicionarHamming = list(binarioParaHamming(mensagemLista,tamanhoHamming))
                listaSublistas.append(adicionarHamming)
                del(listaBinario[0:(melhorTamanhoHamming - contadorPotenciasDois)])
        
            if len(listaSublistas) == 300:
                escreveNoHamming = embaralhar(listaSublistas)
                binarioArq.write(escreveNoHamming)
                listaSublistas = []

        if len(listaBinario) != 0:
            while len(listaBinario) < (melhorTamanhoHamming - contadorPotenciasDois):
                listaBinario.insert(0,"0")
            mensagem = listaBinario[0:(melhorTamanhoHamming - contadorPotenciasDois)]
            mensagemLista,tamanhoHamming = dataParaLista(mensagem)
            adicionarHamming = list(binarioParaHamming(mensagemLista,tamanhoHamming))
            listaSublistas.append(adicionarHamming)
        
        if len(listaSublistas):
            escreveNoHamming = embaralhar(listaSublistas)
            binarioArq.write(escreveNoHamming)
        
    binarioArq.close()

    print("\n"*3, f"Terminei :D \rFoi feito um Hamming com {melhorTamanhoHamming} bits totais sendo {melhorTamanhoHamming - contadorPotenciasDois} bits de data e {contadorPotenciasDois}\
 de pariedade")


def arquivoHammingParaBinario(localArquivo):
    binarioArq = open(localArquivo, "r")
    listaBits,semHammingList1 = [], []
    extensao = input("Qual era a extensão do arquivo?")
    des = "Destino." + extensao
    y = binarioArq.read()
    z = (len(y))
    errosLista,listaHammings = 0,[]
    tamanhoHammingVolta = 8
    hammina = 0
    
    while tamanhoHammingVolta * 100_000 < z:
            tamanhoHammingVolta = (tamanhoHammingVolta * 2)
    
    if z % tamanhoHammingVolta != 0:
        print("Foram adicionados ou removidos bits, a recuperação do arquivo não é possivel")
        return()

    with open(des, "wb") as file:
        for bit in y:
            listaHammings.append(bit)
            if len(listaHammings) == (300 * tamanhoHammingVolta):
                hammingOrdem = desembaralhar(listaHammings,tamanhoHammingVolta)
                listaHammings = []
                for chr in hammingOrdem:
                    listaBits.append(chr)
                    if len(listaBits) == tamanhoHammingVolta:
                        hammina += 1
                        semHammingStr,erros = HammingParaBinario(listaBits)
                        for i in semHammingStr:
                            semHammingList1.append(i)
                        while len(semHammingList1) >= 8:
                            semHammingint = int("".join([i for i in semHammingList1[0:8]]),2)
                            file.write(semHammingint.to_bytes(1,"little"))
                            del(semHammingList1[0:8])
                        if erros:
                            errosLista += 1
                        del(listaBits[0:tamanhoHammingVolta])
        if len(listaHammings) != 0:
            hammingOrdem = desembaralhar(listaHammings,tamanhoHammingVolta)
            listaHammings = []
            for chr in hammingOrdem:
                listaBits.append(chr)
                if len(listaBits) == tamanhoHammingVolta:
                    hammina += 1
                    semHammingStr,erros = HammingParaBinario(listaBits)
                    for i in semHammingStr:
                        semHammingList1.append(i)
                    while len(semHammingList1) >= 8:
                        semHammingint = int("".join([i for i in semHammingList1[0:8]]),2)
                        file.write(semHammingint.to_bytes(1,"little"))
                        del(semHammingList1[0:8])
                    if erros:
                        errosLista += 1
                    del(listaBits[0:tamanhoHammingVolta])
    if not errosLista:
        print("\n"*3,"Não foram encontrados erros, o arquivo foi convertido ao seu formato original :D")
    elif errosLista:
        print("\n"*3,f"Foram encontrados e corrigidos {errosLista} erros. O arquivo foi arrumado e exportado ao seu formato original :D")


def embaralhar(listaHamming):
    tamanhoHamming = len(listaHamming[0])
    listaRetorno = ""
    for posicao in range(tamanhoHamming):
        for hamming, _ in enumerate(listaHamming):
            listaRetorno = listaRetorno + str(listaHamming[hamming][posicao])
    return(listaRetorno)


def desembaralhar(listaHamming,tamanhoHamming):
    numeroHammings = len(listaHamming) // tamanhoHamming
    strRetorno = ""
    for hamming in range(numeroHammings):
        for posicao in range(tamanhoHamming):
            strRetorno = strRetorno + listaHamming[hamming + (posicao * numeroHammings)]
    return(strRetorno)





def dataParaLista(mensagem):
    potenciaDeDois = 8                                                                  
    marcadorDois = 2                                                            
    while potenciaDeDois < len(mensagem):
        potenciaDeDois = potenciaDeDois * 2
    mensagemLista = [i for i in mensagem]
    bitsem8 = ["*"] * potenciaDeDois
    posicao8 = 0
    for posicao, _ in enumerate(bitsem8):
        if posicao == marcadorDois:
            marcadorDois = marcadorDois * 2           
            continue
        if posicao > 2:
            bitsem8[posicao] = int(mensagemLista[posicao8])
            posicao8 += 1

    return(bitsem8,marcadorDois)


def binarioParaHamming(bitsemHamming,tamanhoHamming):
    grupos = []
    bitsDeParidade,potenciasDois = 3,8
        
    for contadorNeutro in range(1, tamanhoHamming + 1):  
        if contadorNeutro > potenciasDois:
            potenciasDois = potenciasDois * 2
            bitsDeParidade += 1
        
    for _ in range(bitsDeParidade):
        grupos.append([]) 

    for posicaoHamming, _ in enumerate(bitsemHamming):
        contadorGrupo = -1
        posicaoHammingBin = [int(i) for i in bin(posicaoHamming) if i != "b"]
        while len(posicaoHammingBin) < bitsDeParidade:
            posicaoHammingBin.insert(0, 0)
        if len(posicaoHammingBin) > bitsDeParidade:
            posicaoHammingBin.pop(0)
        for posicaoBinario, bitBinario in enumerate(posicaoHammingBin):
            if bitBinario:
                grupos[contadorGrupo].append(posicaoHamming)
            contadorGrupo -= 1

    for subGrupo in grupos:
        pariedade = 0
        for bit in subGrupo:
            pariedade = pariedade ^ int(bitsemHamming[bit]) if bitsemHamming[bit] != "*" else pariedade
        bitsemHamming[subGrupo[0]] = pariedade

    pariedade = 0
    for posicaoGeral in bitsemHamming:
        if posicaoGeral != "*":
            pariedade = pariedade ^ posicaoGeral
    bitsemHamming[0] = pariedade

    return("".join([str(i) for i in bitsemHamming]))

def HammingParaBinario(bitsComHamming):
    listaBits = [int(i) for i in bitsComHamming]
    erros = []
    pariedade = 0
    potenciaDois = 4
    listaBitsPariedade = []

    for posicao,bite in enumerate(listaBits):
        pariedade = pariedade ^ posicao if bite else pariedade
    if pariedade:
        erros.append(pariedade)
        listaBits[pariedade] = int(not listaBits[pariedade])
    
    for posicao, _ in enumerate(listaBits):
        if posicao > 2:
            if posicao == potenciaDois:
                listaBitsPariedade.insert(0,posicao)
                potenciaDois = potenciaDois * 2
                continue
        elif posicao <= 2:
            listaBitsPariedade.insert(0,posicao)

    for posicaoPariedade in listaBitsPariedade:
        del(listaBits[posicaoPariedade])
    
    bitsComHamming = "".join([str(i) for i in listaBits])
    return(bitsComHamming, erros)


def main():
    print("Escolha uma opção: \n [1] Binario para hamming \t \t [2] Hamming para binario \t \t [3] Arquvio para hamming \t \t [4] Arquivo com Hamming para arquivo original")
    opcao = input("")
    
    if opcao == "1":
        mensagem = input("qual os bits de data?")
        mensagemLista,tamanhoHamming = dataParaLista(mensagem)
        print (binarioParaHamming(mensagemLista,tamanhoHamming))
    elif opcao == "2":
        mensagem = input("qual os bits com Hamming? ")
        binario, erros = HammingParaBinario(mensagem)
        if erros:
            print(f'\nTeve um erro na posição {erros[0]} \nA mensagem corrigida ficou {binario}')
        else:
            print(f'Nao teve erros, sua mensagem é {binario}')
    elif opcao == "3":
        ArqParaHamming()
    elif opcao == "4":
        localArquivo = input("qual o local do arquivo com o hamming? ")
        arquivoHammingParaBinario(localArquivo)

if __name__ == '__main__':
    main()

