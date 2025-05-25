from auth.Login.login import Login

if __name__ == "__main__":
    email= "teste@exemplo.com",
    senha =  "123456",
    login = Login(email[0], senha[0])
    sucesso, mensagem = login.authenticate()
    print(f"Login {'sucesso' if sucesso else 'falhou'}: {mensagem}")