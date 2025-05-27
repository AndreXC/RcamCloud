import flet as ft
from auth.CheckAuthToken.checkAuthToken import checkAuthToken
from App.login.login import LoginApp
from App.dashboard.dash import Dashboard
from App.Loader.loader import Loader
from log.log import LogRequest
import flet as ft

def main(page: ft.Page):
    loader = Loader(page)
    loader.show()

    instanceCheckAuthToken = checkAuthToken()
    response = instanceCheckAuthToken.request_token()

    loader.clear()

    if response['status']:
        if response['message'] == 'Token válido':
            Dashboard(page=page)
        else:
            LoginApp(page=page)
    else:
        if response.get('error'):
            LogRequest(response['error'], 'client').request_log()
        LoginApp(page=page)

ft.app(target=main)