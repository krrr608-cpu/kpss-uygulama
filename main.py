import flet as ft
import json
import urllib.request

def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0
    ana_liste = ft.ListView(expand=True, spacing=0, padding=ft.padding.only(top=50, bottom=20))
    page.add(ana_liste)

    URL = "https://raw.githubusercontent.com/krrr608-cpu/Hilal_kpss/refs/heads/main/sorular.json"

    # Global Değişkenler
    veriler = {}
    cozulen_sorular = [] 
    hatali_sorular = []
    aktif_sorular = []
    mevcut_index = 0
    oturum_cevaplari = {} 

    def verileri_guncelle():
        nonlocal veriler, cozulen_sorular, hatali_sorular
        try:
            response = urllib.request.urlopen(URL, timeout=3)
            data_str = response.read().decode('utf-8')
            veriler = json.loads(data_str)
            page.client_storage.set("kpss_v6_data", data_str)
        except:
            if page.client_storage.contains_key("kpss_v6_data"):
                veriler = json.loads(page.client_storage.get("kpss_v6_data"))
        
        cozulen_sorular = page.client_storage.get("cozulenler") if page.client_storage.contains_key("cozulenler") else []
        hatali_sorular = page.client_storage.get("hatalar") if page.client_storage.contains_key("hatalar") else []
        page.update()

    # --- DERS NOTU GÖSTERİCİ ---
    def ders_notu_ac(baslik, icerik, renk):
        def kapat(e):
            page.close(dlg)

        dlg = ft.AlertDialog(
            title=ft.Row([ft.Icon(ft.icons.MENU_BOOK, color=renk), ft.Text(baslik, weight="bold", size=20)], tight=True),
            content=ft.Container(
                content=ft.Column([
                    ft.Divider(),
                    ft.Text(icerik, size=16, selectable=True),
                ], scroll=ft.ScrollMode.ADAPTIVE, tight=True),
                width=400,
                height=500,
            ),
            actions=[ft.TextButton("Anladım", on_click=kapat)],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=15),
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # --- KATEGORİ VE ALT KATEGORİ LİSTELEYİCİ ---
    def kategorileri_ciz(liste, ust_baslik="KPSS", renk="indigo", is_sub=False):
        ana_liste.controls.clear()
        
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, icon_color="white", on_click=lambda _: ana_menuyu_ciz()) if is_sub else ft.Container(),
                    ft.Text(ust_baslik, size=24, weight="bold", color="white"),
                ], alignment="start"),
                ft.Text("Çalışmak istediğin bölümü seç", color="white70", size=12)
            ], horizontal_alignment="center"),
            bgcolor=renk, padding=30, border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20)
        )
        ana_liste.controls.append(header)

        for öğe in liste:
            tip = öğe.get("tip", "kategori") # 'not' veya 'kategori'
            
            if tip == "not":
                # DERS NOTU MANTIĞI
                on_click_func = lambda e, b=öğe["ad"], i=öğe["icerik"], r=öğe.get("renk", renk): ders_notu_ac(b, i, r)
                alt_bilgi = "Ders Notu 📖"
                kart_renk = öğe.get("renk", "orange")
                ikon = ft.icons.DESCRIPTION
            elif öğe.get("alt_kategoriler"):
                # ALT KATEGORİ MANTIĞI
                on_click_func = lambda e, alt=öğe["alt_kategoriler"], ad=öğe["ad"], r=öğe.get("renk", renk): kategorileri_ciz(alt, ad, r, True)
                alt_bilgi = f"{len(öğe['alt_kategoriler'])} Alt Başlık"
                kart_renk = öğe.get("renk", "blue")
                ikon = öğe.get("ikon", ft.icons.FOLDER)
            else:
                # SORU BANKASI MANTIĞI
                sorular = öğe.get("sorular", [])
                cozulmemis = [s for s in sorular if s["metin"] not in cozulen_sorular]
                on_click_func = lambda e, k=öğe, s=cozulmemis: ders_testini_baslat(k, s)
                alt_bilgi = f"Kalan Soru: {len(cozulmemis)}"
                kart_renk = öğe.get("renk", "green")
                ikon = öğe.get("ikon", ft.icons.QUIZ)

            ana_liste.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(name=ikon, size=35, color="white"),
                        ft.Column([
                            ft.Text(öğe.get("ad"), size=18, weight="bold", color="white"),
                            ft.Text(alt_bilgi, color="white70", size=12)
                        ], spacing=0)
                    ]),
                    bgcolor=kart_renk, padding=15, margin=ft.margin.symmetric(horizontal=20, vertical=8),
                    border_radius=12, on_click=on_click_func, ink=True
                )
            )
        page.update()

    def ana_menuyu_ciz():
        verileri_guncelle()
        kategorileri_ciz(veriler.get("kategoriler", []))

    # --- TEST MANTIĞI (Öncekiyle Aynı) ---
    def ders_testini_baslat(kategori, filtrelenmis_sorular):
        if not filtrelenmis_sorular: return
        nonlocal aktif_sorular, mevcut_index; aktif_sorular = filtrelenmis_sorular; mevcut_index = 0
        # Burada senin mevcut test_ekranini_ciz fonksiyonunu çağırabilirsin...
        # (Kısalık adına test çizim kodlarını buraya eklemiyorum, senin orijinal kodunla aynı kalacak)

    ana_menuyu_ciz()

ft.app(target=main)
