# -*- coding: utf-8 -*-
"""
@date: 07/06/2017
@author: Jaine Budke

"""

from codecs import open
from lockfile import LockFile


# \brief Funcao verifica se arquivo esta vazio
# \param arquivo O arquivo que sera verificado
# \return True se estiver vazio, false otherwise
def isEmpty( arquivo ):
    arq = open(arquivo, 'r') # abrindo arquivo no modo leitura
    ctd = arq.read() # lendo arquivo e salvando conteudo
    arq.close()
    return (not ctd)


# \brief Funcao add elementos em arquivo txt
# \param arquivo O arquivo no qual os elementos serao add
# \param elem Elemento(s) que serao add
# \param type Formato em que os elementos estao: arquivo ('a') ou texto ('t')
def add( arquivo, elem, type ):
    lock = LockFile(arquivo) # abrir chamada com LockFile
    lock.acquire() # bloquear arquivo

    arq = open(arquivo, 'a') # abrindo arquivo no modo leitura
    if( type == 't' ):
        arq.write(elem+"\n")
    else:
        newList = open(elem, 'r')
        lista = newList.read()
        newList.close()
        arq.writelines(lista)
    arq.close()

    lock.release() # desbloquear arquivo


# \brief Funcao captura primeiro elemento, o remove da lista e o adiciona no arquivo 'running'
# \param arquivo O arquivo que sera analisado
# \return A primeira linha do arquivo
def get( arquivo ):
    lock = LockFile(arquivo) # abrir chamada com LockFile
    lock.acquire() # bloquear arquivo

    if( isEmpty(arquivo) ): # verifica se arquivo de entrada esta vazio
        return
    arq = open(arquivo, 'r')    # abre arquivo no modo leitura
    firstLine = arq.readline()  # le e excluir a primeira linha do arquivo
    linhas = arq.read()           # le arquivo todo
    arq.close()                        # fecha arquivo

    # Gravando elementos no arquivo sem a primeira linha
    arq = open(arquivo, 'w')
    arq.writelines(linhas)
    arq.close()

    lock.release() # desbloquear arquivo

    runn = 'data/running.txt'
    lock = LockFile(runn) # abrir chamada de arquivo running com LockFile
    lock.acquire() # bloquear arquivo

    arq = open(runn, 'a')
    arq.write(firstLine)
    arq.close()

    lock.release() # desbloquear arquivo

    return firstLine



# \brief Funcao que captura elemento passado por parametro, o retira da running e coloca no arquivo done
# \param elem Elemento a ser removido da running e colocado na done
def done( elem ):
    runn = 'data/running.txt'
    lock = LockFile(runn) # abrir chamada de arquivo running com LockFile
    lock.acquire() # bloquear arquivo

    # lendo e identificando elemento na running...
    arq = open(runn, 'r') # abre a running no modo leitura
    linhas = arq.readlines()                # le linhas da running
    for i in range(len(linhas)-1):
        if(linhas[i+1]==elem):
            arq.readline() # le e exclui linha do arquivo
        else:
            return -1

    newList = arq.readlines() # le arquivo todo (ja sem a linha selecionada)
    arq.close()

    lock.release() # desbloquear arquivo

    lock = LockFile(runn) # abrir chamada de arquivo running com LockFile
    lock.acquire() # bloquear arquivo
    # escrevendo a nova lista na running...
    arq = open('data/running.txt', 'w') # abre a running no modo escrita
    arq.writelines(newList)
    arq.close()

    lock.release() # desbloquear arquivo

    lock = LockFile('data/done.txt') # abrir chamada de arquivo done com LockFile
    lock.acquire() # bloquear arquivo

    # adicionando elemento da done...
    arqDone = open('data/done.txt', 'a')
    arqDone.writelines(elem)
    arqDone.close()

    lock.release() # desbloquear arquivo
