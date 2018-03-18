#!/usr/bin/env python3

import sys
import subprocess
import csv
import time
import re
import os
import datetime
if sys.version_info[0] == 3:
    import urllib.request
    py3 = True
    qtd_float = 1

else:
    import urllib2
    py3 = False
    qtd_float = 0


datenow = datetime.datetime.now()
nome_arquivo = "Booking_Rating_WiFi_" + datenow.strftime("%Y-%m-%d %H:%M:%S")

contagem = 1

hotel_nome = []
hotel_nota_wifi = []
hotel_nota_overall = []


print("\n")
print("-----------------------------")
print("B O O K I N G  S C R A P E R")
print("-----------------------------")


bd_num = input("Usar BD principal[1] ou BD teste[2]? ")
while bd_num != str(1) and bd_num != str(2):
    bd_num = input("Usar BD principal[1] ou BD teste[2]? ")




def tratamento_de_string(html):
    global nota_wifi

    try:

        #Overall
        posicao1 = html.find('<span class="review-score-badge"')
        posicao2 = html[posicao1:].find('</span>')
        posicao_final = html[posicao1:][:posicao2]
        posicao_numero = re.search("\d", posicao_final).start()
        nota_overall = posicao_final[posicao_numero:posicao_numero+3].replace(',', '.')

        #Wifi
        posi_wifi_tag = html.find("hotel_wifi")
        if posi_wifi_tag == -1:
            posi_wifi_tag = html.find("hotel_paid_wifi")

        posi_score = html[posi_wifi_tag:].find('</li>')
        final = html[posi_wifi_tag:posi_wifi_tag+posi_score]
        final = html[posi_wifi_tag+posi_score-13:posi_wifi_tag+posi_score].replace(',', '.')
        if "." in final:
            match = re.search(r'\d+\.\d+', final)
            match_float = match.group()
            nota_wifi = match_float

        else:
            match = re.search(r'\d', final)
            match_inter = match.group()
            nota_wifi = match_inter+'.0'

    except:
        nota_wifi = "error!!!"
        nota_overall = "error!!!"



    finally:
        return nota_wifi, nota_overall


#Fazendo download da pagina html
with open('bd'+str(bd_num)+'.csv', 'r', encoding="utf-8") as f:
    print("Obtendo dados do Booking...")
    print(" ")
    reader = csv.reader(f)
    lista_hoteis = list(reader)
    for i in lista_hoteis:
        if "https://www.booking.com" in i[1]:
            #Validando se o usuario esta rodando python3
            if py3 == True:
                with urllib.request.urlopen(i[1]) as response:
                    page_code = response.read()
            else:
                response = urllib2.urlopen(i[1])
                page_code = response.read()

            

            #Retirando NOMES/NOTAS e armazenando em arrays
            wifi, overall = tratamento_de_string(str(page_code))
            hotel_nota_wifi.append(wifi)
            hotel_nota_overall.append(overall)
            hotel_nome.append(i[0])

        else:
            hotel_nota_wifi.append("n/a")
            hotel_nota_overall.append("n/a")
            hotel_nome.append(i[0])
            wifi = "n/a"
            overall = "n/a"

        

        #Imprimindo progresso
        progresso = contagem * 100 / len(lista_hoteis)
        contagem = contagem + 1

        #print("[%.1f%%] %s - Wifi: %s  Overall: %s" %(progresso, i[0], wifi, overall))
        print("[{0:.{4}f}%] {1} - Wifi: {2}  Overall: {3}".format(progresso, i[0], wifi, overall, qtd_float))



# Escrevendo no ficheiro
print("Escrevendo Resultados no ficheiro...")
with open("uuuuu.csv", 'w') as resultado:
    escrevendo = csv.writer(resultado)
    escrevendo.writerow(["Hoteis", "WiFi", "Overall"])
    for i in range(len(hotel_nome)):
        escrevendo.writerow([hotel_nome[i], hotel_nota_wifi[i], hotel_nota_overall[i]])
    resultado.close()

demorou = datetime.datetime.now() - datenow
print("Done!")
print("processo demorou:", datetime.datetime.now() - datenow)
