import flet as ft
from auth.CheckAuthToken.checkAuthToken import checkAuthToken
from fletApp.login.login import LoginApp
from fletApp.dashboard.dash import Dashboard
from log.log import LogRequest
def main(page: ft.Page):
    instanceCheckAuthToken = checkAuthToken()
    response = instanceCheckAuthToken.request_token()     
    if response['status']:
       if response['message'] =='Token válido':
            Dashboard(page=page)
       else:
            LoginApp(page=page)
    else:
        if response['error']:
            LogRequest().request_log(response['error'], 'client')
        LoginApp(page=page)
        
ft.app(target=main)
