import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

DB_PATH = 'clientes.db'

# CONFIGURAÇÕES DO SEU E-MAIL (remetente)
EMAIL = 'seu_email@gmail.com'
SENHA = 'sua_senha_de_aplicativo'
DESTINATARIO = 'destinatario@gmail.com'

def buscar_alertas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, processo, data_final FROM clientes")
    alertas = []
    for nome, processo, data_final in cursor.fetchall():
        try:
            if data_final:
                dias = (datetime.strptime(data_final, '%Y-%m-%d') - datetime.today()).days
                if 0 <= dias <= 2:
                    alertas.append(f'Processo: {processo} de {nome} vence em {dias} dia(s) ({data_final})')
        except:
            continue
    conn.close()
    return alertas

def enviar_email(alertas):
    if not alertas:
        print("Nenhum alerta para enviar.")
        return

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = DESTINATARIO
    msg['Subject'] = '⚠️ Alerta de prazos - Sistema de Cadastro'

    corpo = "\n".join(alertas)
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL, SENHA)
            server.send_message(msg)
        print("✅ Alerta enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar:", e)

if __name__ == '__main__':
    alertas = buscar_alertas()
    enviar_email(alertas)