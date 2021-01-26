import datetime
import os
import time
from pynput.keyboard import Key, Controller
import pandas as pd
import subprocess

#abrir o profit
os.system("start C:/Users/1998a/AppData/Roaming/Nelogica/ClearTrader/profitchart.exe")

#esperar carregar, conectar, se estabelecer
time.sleep(15)

#abrir planilha atrelada ao DDE do profit
os.chdir("C:/Users/1998a/Documents/GitHub/bolsistas_da/planilhas_diarias")

os.system("start EXCEL.EXE fonte_DDE.xlsx")

#esperar carregar
time.sleep(10)

#apertar ENTER para autorizar a atualização dos dados
keyboard = Controller()
keyboard.press(Key.enter)
time.sleep(2)
keyboard.release(Key.enter)

#carregar todos os dados
time.sleep(10)

#salvar
keyboard.press(Key.ctrl)
keyboard.press('b')
time.sleep(1)
keyboard.release('b')
keyboard.release(Key.ctrl)

time.sleep(2)

#fechar ambos
os.system('TASKKILL /F /IM excel.exe')
os.system('TASKKILL /F /IM profitchart.exe')

#usar pandas pra ler a tabela atualiazda e salvar em outro arquivo com o nome de hoje
df = pd.read_excel("fonte_DDE.xlsx")
today = datetime.date.today()
df.to_excel(f"{today}.xlsx")
