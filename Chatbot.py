#coding: utf-8

import subprocess as s
import os
import sys
import json
#import sqlite3
import psycopg2
import base64

#con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='96006430')
#cur = con.cursor()
#sql = "insert into dados (palavra,resposta) values('teste','respteste')"
#cur.execute(sql)
#con.commit()

import speech_recognition as sr
import pyttsx3

#speak = pyttsx3.init('sapi5')

struct = {}
#path = R'C:\sqlite\telegram'
#conn = sqlite3.connect(path + R'\servius.db')
#connection = sqlite3.connect('servius.db')
#c = connection.cursor()

class Chatbot():
    def __init__(self, nome):
        try:
            memoria = open(nome+'.json', 'r')
            memoria1 = open(nome + '1' + '.json', 'r')
        except FileNotFoundError:
            memoria = open(nome+'.json', 'w')
            memoria1 = open(nome + '1' + '.json', 'w')
            memoria.write('["Anderson", "Glauco", "Marlos", "Abreu"]')
            memoria1.write('{"oi": "Olá, qual o seu nome?", "tchau": "tchau"}')
            memoria.close()
            memoria1.close()
            memoria = open(nome + '.json', 'r')
            memoria1 = open(nome + '1' + '.json', 'r')
        self.nome = nome
        self.conhecidos = json.load(memoria)
        self.frases = json.load(memoria1)
        memoria.close()
        memoria1.close()
        self.historico = [None]

    def escuta(self, frase=None):
        if frase == None:
            frase = input('>: ')
        frase = str(frase)
        #frase = frase.lower()
        frase = frase.replace('eh', 'é')
        return frase


    def pensa(self, frase, chatID):
        #frase = frase.lower()
        try:

            retornofrase = self.procura_frase(frase, chatID)
            if retornofrase != 'Não encontrei este item':
                return retornofrase

            if frase == 'aprenda':
                return 'Digite a frase: '
                resp = input('Digite a resposta: ')
                self.frases[chave] = resp
                self.gravaMemoria()
                return 'Aprendido'

            if frase == 'corrija':
                return 'O que devo corrigir: '
                resp = input('Digite a resposta: ')
                self.frases[chave] = resp
                self.gravaMemoria()
                return 'Aprendido'

            if frase == 'proteja':
                return 'Informe a frase: '
                resp = input('Informe a resposta: ')
                self.frases[chave] = resp
                return 'Aprendido'

            if frase == 'corrija e proteja':
                return 'Informe o que devo corrigir: '
                resp = input('Informe a resposta: ')
                self.frases[chave] = resp
                return 'Aprendido'

            if frase == 'lembrar':
                self.historico.append(frase)
                self.chave = frase
                return 'Lembrar o que: '

            try:
                ultimafrase = self.historico[-1]
                penultimafrase = self.historico[-2]
            except:
                pass

            if ultimafrase == 'Olá, qual o seu nome?':
                nome = self.pegaNome(frase)
                frase = self.respondeNome(nome)
                return frase

            if ultimafrase == 'Digite a frase: ':
                self.historico.append(frase)
                self.chave = frase
                return 'Digite a resposta: '

            if ultimafrase == 'O que devo corrigir: ':
                self.historico.append(frase)
                self.chave = frase
                return 'Resposta da correção: '

            if ultimafrase == 'Informe a frase: ':
                self.historico.append(frase)
                self.chave = frase
                return 'Informe a resposta: '

            if ultimafrase == 'Informe o que devo corrigir: ':
                self.historico.append(frase)
                self.chave = frase
                return 'Informe a resposta da correção: '

            if ultimafrase == 'Informe a resposta: ':
                resp = frase
                self.gravapgprotege(penultimafrase, resp, chatID)
                return 'Protegido'

            if ultimafrase == 'Informe a resposta da correção: ':
                resp = frase
                self.corrigepgprotege(penultimafrase, resp, chatID)
                return 'Protegido'

            if ultimafrase == 'Digite a resposta: ':
                resp = frase
                #self.frases[self.chave] = resp
                #self.gravaMemoria()
                self.gravapgfrase(penultimafrase, resp, chatID)
                return 'Aprendi'

            if ultimafrase == 'Resposta da correção: ':
                resp = frase
                #self.frases[self.chave] = resp
                #self.gravaMemoria()
                self.corrigepgfrase(penultimafrase, resp, chatID)
                return 'Corrigido'

            if ultimafrase == 'Lembrar o que: ':
                retornofrase = self.procura_proteja(frase, chatID)
                if retornofrase != '':
                    return retornofrase
                else:
                    return 'Não encontrei este item'



            try:
                resp = str(eval(frase))
                return resp
            except:
                pass
            return 'Não entendi!'
        except:
            return 'Não entendi!'


    # pega o nome do usuario
    def pegaNome(self, nome):
        if 'o meu nome é ' in nome:
            nome = nome[13:]
        elif 'eu me chamo ' in nome:
            nome = nome[12:]
        elif ' é o meu nome' in nome:
            nome = nome[0:-12]
        elif 'eu me chamo ' in nome:
            nome = nome[12:]
        nome = nome.title()
        return nome

    def respondeNome(self, nome):
        if nome in self.conhecidos:
            frase = 'Olá como vai '
        else:
            frase = 'Muito prazer '
            self.conhecidos.append(nome)
            self.gravaMemoria()
        return frase + nome


    def gravaMemoria(self):
        memoria = open(self.nome + '.json', 'w')
        memoria1 = open(self.nome + '1' + '.json', 'w')
        json.dump(self.conhecidos, memoria)
        json.dump(self.frases, memoria1)
        memoria.close()
        memoria1.close()


    def gravapgprotege(self, penultimafrase, resp, chatID):
        con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='96006430')
        cur = con.cursor()
        sqlsalto = 'select salt_id from apoio.tbsalto'
        cur.execute(sqlsalto)
        salto = cur.fetchone()
        palavracript = base64.b64encode((penultimafrase+salto[0]).encode('utf-8'))
        respostacript = base64.b64encode((resp+salto[0]).encode('utf-8'))
        chatIDcript = base64.b64encode((str(chatID)+salto[0]).encode('utf-8'))
        sql = 'INSERT INTO servius.senha (chatID,palavra,resposta) VALUES ('+"'"+chatIDcript.decode('ascii')+"','"+palavracript.decode('ascii')+"', "+"'"+respostacript.decode('ascii')+"'"')'
        cur.execute(sql)
        con.commit()

    def corrigepgprotege(self, penultimafrase, resp, chatID):
        con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='96006430')
        cur = con.cursor()
        sqlsalto = 'select salt_id from apoio.tbsalto'
        cur.execute(sqlsalto)
        salto = cur.fetchone()
        palavracript = base64.b64encode((penultimafrase+salto[0]).encode('utf-8'))
        respostacript = base64.b64encode((resp+salto[0]).encode('utf-8'))
        chatIDcript = base64.b64encode((str(chatID)+salto[0]).encode('utf-8'))
        sql = 'UPDATE servius.senha SET palavra = ' + "'" + palavracript.decode('ascii') + "', resposta = '" + respostacript.decode('ascii') + "' where palavra = '" + palavracript.decode('ascii') + "'"''
        #sql = 'UPDATE servius.senha (chatID,palavra,resposta) VALUES ('+"'"+chatIDcript.decode('ascii')+"','"+palavracript.decode('ascii')+"', "+"'"+respostacript.decode('ascii')+"'"')'
        cur.execute(sql)
        con.commit()

    def gravapgfrase(self, penultimafrase, resp, chatID):
        con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='96006430')
        cur = con.cursor()
        chatid = str(chatID)
        sql = 'INSERT INTO servius.frases (chatid,frase,resposta) VALUES (' +"'"+chatid+"','"+penultimafrase+"','"+resp+"')"''
        cur.execute(sql)
        con.commit()

    def corrigepgfrase(self, penultimafrase, resp, chatID):
        con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='96006430')
        cur = con.cursor()
        chatid = str(chatID)
        sql = 'UPDATE servius.frases SET frase = '+"'"+penultimafrase+"', resposta = '"+resp+"' where frase = '"+penultimafrase+"'"''
        cur.execute(sql)
        con.commit()


    def procura_proteja(self, frase, chatID):
        con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='96006430')
        cur = con.cursor()
        sqlsalto = 'select salt_id from apoio.tbsalto'
        cur.execute(sqlsalto)
        salto = cur.fetchone()
        buscapalavra = base64.b64encode((frase+salto[0]).encode('utf-8'))
        buscapalavra = buscapalavra.decode('ascii')
        buscachatid = base64.b64encode((str(chatID)+salto[0]).encode('utf-8'))
        buscachatid = buscachatid.decode('ascii')
        sql = 'select resposta from servius.senha where palavra ='+"'"+buscapalavra+"'"+' and chatid ='+"'"+buscachatid+"'"+''
        cur.execute(sql)
        consultapalavra = cur.fetchone()
        if consultapalavra == None:
            consultapalavra = 'Não encontrei este item'
        else:
            consultapalavra = base64.b64decode(consultapalavra[0]).decode('ascii')
            consultapalavra = consultapalavra.replace(salto[0], '')
        return consultapalavra


    def procura_frase(self, frase, chatID):
        con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='96006430')
        cur = con.cursor()
        buscachatid = str(chatID)
        sql = 'select resposta from servius.frases where frase ='+"'"+frase+"'"+' and chatid ='+"'"+buscachatid+"'"+''
        cur.execute(sql)
        respostapalavra = cur.fetchone()
        if respostapalavra == None:
            respostapalavra = 'Não encontrei este item'
        else:
            respostapalavra = respostapalavra[0]
        return respostapalavra


    #não estou utilizando seria para gravar no sqlite3
    def gravabanco(self, penultimafrase, resp):
        sql = 'INSERT INTO dados (palavra,resposta) VALUES ('+"'"+penultimafrase+"', "+"'"+resp+"'"')'
        connection = sqlite3.connect('servius.db')
        c = connection.cursor()
        c.execute(sql)
        connection.commit()

    #não utilizado seria para criar tabela no sqlite3
    def create_table():
        connection = sqlite3.connect('servius.db')
        c = connection.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS dados (id integer PRIMARY KEY AUTOINCREMENT, palavra text, resposta text)')


    def fala(self, frase):
        frase
        if 'execute ' in frase:
            plataforma = sys.platform
            comando = frase.replace('execute ', '')
            if 'win' in plataforma:
                os.startfile(comando)
            try:
                if 'linux' in plataforma:
                    s.Popen(comando)
            except FileNotFoundError:
                s.Popen(['xdg-open', comando])

        else:
            print(frase)
        self.historico.append(frase)