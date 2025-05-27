# # import requests

# # # URL da sua API
# # url = 'https://rcamgeo.com.br/teste2/api/authUser.php'

# # # Dados do usuário
# # payload = {
# #     'email': 'teste@exemplo.com',
# #     'senha': '123456',
# #     'tokenDispositivo': 'token-unico-do-dispositivo'
# # }

# # # Cabeçalhos

# # # Enviando a requisição
# # response = requests.post(url, data=payload, headers=headers)

# # # Exibindo a resposta
# # if response.status_code == 200:
# #     print("Token recebido:")
# #     print(response.json())
# # else:
# #     print(f"Erro {response.status_code}:")
# #     print(response.text)
    
    
# import requests

# # URL do endpoint
# url2 = 'https://rcamgeo.com.br/teste2/api/validTokenUser.php'  # Altere para a URL real

# # Dados do token e do dispositivo
# payload = {
#     'token_dispositivo': 'token-unico-do-dispositivo',
#     'token': 'teste'  # Supondo que o token seja retornado na resposta anterior
# }

# headers = {
#     # 'X-Api-Key': 'MinhaChaveSecreta',  # Altere conforme definido no PHP
#     'Content-Type': 'application/x-www-form-urlencoded'  # ou multipart/form-data se preferir
# }

# try:
#     # Fazendo a requisição POST
#     response = requests.post(url2, data=payload, headers=headers)

#     # Verifica se a resposta foi bem-sucedida
#     if response.status_code == 200:
#         resultado = response.json()
#         print("✅ Resposta do servidor:")
#         print(resultado)
#     else:
#         print(f"⚠️ Erro {response.status_code}: {response.text}")

# except requests.RequestException as e:
#     print(f"❌ Erro ao fazer a requisição: {e}")
    

# import hashlib
# def hash_password(password: str) -> str:
#     sha256_hash = hashlib.sha256(password.encode()).hexdigest()
#     return sha256_hash


# print(hash_password("123456"))

from client.log.log import LogRequest 

if __name__ == "__main__":
    # Exemplo de uso
    log = LogRequest("Erro de teste", "cliente")
    log.request_log()