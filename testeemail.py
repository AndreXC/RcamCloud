import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurações do servidor SMTP da Hostinger
smtp_server = 'smtp.hostinger.com'
smtp_port = 465
email_sender = 'ccontato@rcamgeo.com.br'
email_password = 'Q8rUH_25Rcam'

# Destinatário
email_receiver = 'andrecr7r102014@gmail.com'  # Substitua pelo destinatário real

# Criando o conteúdo do e-mail
codigo_acesso = 'ABC123'

html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
    <div style="background-color: #fff; padding: 20px; border-radius: 10px; max-width: 500px; margin: auto; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
      <h2 style="color: #333;">Seu Código de Acesso</h2>
      <p style="font-size: 16px; color: #555;">
        Olá, segue abaixo o seu código de acesso:
      </p>
      <div style="font-size: 24px; font-weight: bold; color: #d32f2f; text-align: center; margin: 20px 0;">
        {codigo_acesso}
      </div>
      <p style="font-size: 14px; color: #888;">Se você não solicitou este código, ignore este e-mail.</p>
    </div>
  </body>
</html>
"""

# Criando o e-mail
msg = MIMEMultipart("alternative")
msg["Subject"] = "Código de Acesso"
msg["From"] = email_sender
msg["To"] = email_receiver

# Anexando o conteúdo HTML
msg.attach(MIMEText(html_content, "html"))

# Enviando o e-mail
try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        print("E-mail enviado com sucesso!")
except Exception as e:
    print("Erro ao enviar e-mail:", e)
