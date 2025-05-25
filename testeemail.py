# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# # Configurações do servidor SMTP da Hostinger
# smtp_server = 'smtp.hostinger.com'
# smtp_port =  587
# email_sender = 'ccontato@rcamgeo.com.br'
# email_password = 'Q8rUH_25Rcam'

# # Destinatário
# email_receiver = 'andrecr7r102014@gmail.com'  # Substitua pelo destinatário real

# # Criando o conteúdo do e-mail
# codigo_acesso = 'ABC123'

# html_content = f"""
# <html>
#   <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
#     <div style="background-color: #fff; padding: 20px; border-radius: 10px; max-width: 500px; margin: auto; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
#       <h2 style="color: #333;">Seu Código de Acesso</h2>
#       <p style="font-size: 16px; color: #555;">
#         Olá, segue abaixo o seu código de acesso:
#       </p>
#       <div style="font-size: 24px; font-weight: bold; color: #d32f2f; text-align: center; margin: 20px 0;">
#         {codigo_acesso}
#       </div>
#       <p style="font-size: 14px; color: #888;">Se você não solicitou este código, ignore este e-mail.</p>
#     </div>
#   </body>
# </html>
# """

# # Criando o e-mail
# msg = MIMEMultipart("alternative")
# msg["Subject"] = "Código de Acesso"
# msg["From"] = email_sender
# msg["To"] = email_receiver

# # Anexando o conteúdo HTML
# msg.attach(MIMEText(html_content, "html"))

# # Enviando o e-mail
# try:
#     with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
#         server.login(email_sender, email_password)
#         server.sendmail(email_sender, email_receiver, msg.as_string())
#         print("E-mail enviado com sucesso!")
# except Exception as e:
#     print("Erro ao enviar e-mail:", e)



import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurações do servidor SMTP da Hostinger (TLS)
smtp_server = 'smtp.hostinger.com'
smtp_port = 587  # Porta TLS
email_sender = 'contato@rcamgeo.com.br'
email_password = 'Q8rUH_25Rcam'  # ATENÇÃO: proteja essa informação
email_receiver = 'andrecr7r102014@gmail.com'  # Altere para o destinatário real

# Código de acesso personalizado
codigo_acesso = 'ABC123'

# HTML formatado do e-mail
html_content = f"""
<html>
  <body style="margin:0; padding:0; background-color:#f4f6f9; font-family:Segoe UI, Roboto, Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center">
          <table width="100%" style="max-width:600px; margin:40px auto; background-color:#ffffff; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.05); padding:30px;">
            <tr>
              <td align="center" style="padding-bottom:20px;">
                <img src="https://img.icons8.com/ios-filled/100/4a90e2/cloud.png" width="60" alt="RcamCloud Logo" style="display:block;" />
                <h1 style="margin:10px 0 0; font-size:24px; color:#4a90e2;">RcamCloud</h1>
                <p style="margin:0; font-size:14px; color:#999;">Conectado com segurança na nuvem</p>
              </td>
            </tr>
            <tr>
              <td style="padding:20px 0; border-top:1px solid #eee;">
                <h2 style="font-size:20px; color:#333; margin:0 0 10px;">Seu código de acesso</h2>
                <p style="font-size:16px; color:#555; margin:0 0 20px;">
                  Olá, aqui está o seu código de verificação seguro para acessar nossos serviços:
                </p>
                <div style="background-color:#f0f4ff; padding:15px; border-radius:8px; text-align:center;">
                  <span style="font-size:28px; font-weight:bold; color:#003f8c; letter-spacing:2px;">{codigo_acesso}</span>
                </div>
                <p style="font-size:14px; color:#999; margin-top:30px;">
                  Se você não solicitou este código, por favor ignore este e-mail ou entre em contato com nosso suporte.
                </p>
              </td>
            </tr>
            <tr>
              <td style="text-align:center; padding-top:30px; font-size:12px; color:#ccc;">
                &copy; 2025 RcamCloud. Todos os direitos reservados.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


# Montagem do e-mail
msg = MIMEMultipart("alternative")
msg["Subject"] = "Código de Acesso"
msg["From"] = email_sender
msg["To"] = email_receiver
msg.attach(MIMEText(html_content, "html"))

# Envio com TLS (STARTTLS)
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        print("✅ E-mail enviado com sucesso!")
except Exception as e:
    print("❌ Erro ao enviar e-mail:", e)
