#!/usr/bin/env python3

import sys
import subprocess
import csv
import datetime
import time
import re
import os
import datetime
import re


datenow = datetime.datetime.now()
nome_arquivo = "Booking_Rating_WiFi_" + datenow.strftime("%Y-%m-%d %H:%M:%S")

contagem = 0

hotel_nome = []
hotel_nota_wifi = []
hotel_nota_overall = []
total_clientes = range(len(hotel_nome))

print("\n")
print("-----------------------------")
print("B O O K I N G  S C R A P E R")
print("-----------------------------")
print(" ")


def main(html):
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
with open('bd2.csv', 'r') as f:
    print("Obtendo dados do Booking...")
    print(" ")
    reader = csv.reader(f)
    lista_hoteis = list(reader)
    for i in lista_hoteis:
        if "https://www.booking.com" in i[1]:
            progresso = contagem * 100 / len(lista_hoteis)
            #print(i[0])
            contagem = contagem + 1
            process = subprocess.Popen('wget -qO- --no-check-certificate "'+i[1]+'"',stdout=subprocess.PIPE, shell=True)
            # Retirando NOMES/NOTAS e armazenando em arrays
 
            wifi, overall = main(str(process.communicate()))
            hotel_nota_wifi.append(wifi)
            hotel_nota_overall.append(overall)
            hotel_nome.append(i[0])
            print("[%.1f%%] %s - Wifi: %s  Overall: %s" %(progresso, i[0], wifi, overall))
        else:
            hotel_nota_wifi.append("n/a")
            hotel_nota_overall.append("n/a")
            hotel_nome.append(i[0])



# Escrevendo no ficheiro
print("Escrevendo Resultados no ficheiro...")
with open(nome_arquivo+".csv", 'w') as resultado:
    escrevendo = csv.writer(resultado)
    escrevendo.writerow(["Hoteis", "WiFi", "Overall"])
    for i in range(len(hotel_nome)):
        escrevendo.writerow([hotel_nome[i], hotel_nota_wifi[i], hotel_nota_overall[i]])
    resultado.close()

datelater = datetime.datetime.now()
print("Done!")
print(datelater-datenow)

