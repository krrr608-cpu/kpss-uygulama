import flet as ft

def main(page: ft.Page):
    page.title = "Test"
    page.bgcolor = "white"
    page.add(ft.Text("ÇALIŞTI!", size=50, color="green"))

ft.app(target=main)
