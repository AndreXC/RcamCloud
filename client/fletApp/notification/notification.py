import flet as ft
def SnackNotification(page: ft.Page, message:ft.Text, sucess: bool = True):
    """
    Function to display a notification message.
    
    Args:
        message (str): The message to be displayed in the notification.
    """
    page.open(ft.SnackBar(
            message,
            # action=ft.Text("Fechar", color="white") if sucess else ft.Text("Tentar novamente", color="white"),
            bgcolor="#5CB85C" if sucess else "#D9534F",
            open=True
    ))
