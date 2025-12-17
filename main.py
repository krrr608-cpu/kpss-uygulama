import flet as ft
import json
import urllib.request
import asyncio

# --- VERSİYON KONTROLÜ İÇİN ---
# Eğer ileride kodda büyük değişiklik yaparsan burayı 1.1, 1.2 diye artıracaksın.
MEVCUT_VERSIYON = 1.0 

def main(page: ft.Page):
    # --- VARSAYILAN AYARLAR (İnternet ve kayıt yoksa) ---
    DEFAULT_VERI = {
        "ayarlar": {
            "baslik": "KPSS", 
            "apk_versiyonu": 1.0,
            "apk_indirme_linki": "https://github.com/krrr608-cpu/kpss-uygulama",
            "tema_rengi": "blue", 
            "arka_plan_rengi": "white"
        },
        "tasarim": {
            "buton_yuvarlakligi": 10,
            "soru_yazi_boyutu": 18,
            "sik_yazi_boyutu": 16,
            "baslik_ortala": True,
            "golge_olsun_mu": False
        },
        "sorular": []
    }
    
    # Güvenli Mod Ayarları
    page.padding = 0
    page.spacing = 0
    ana_liste = ft.ListView(expand=True, spacing=0, padding=0)
    page.add(ana_liste)

    # --- SENİN LİNKİN BURADA ---
    URL = "https://raw.githubusercontent.com/krrr608-cpu/kpss-uygulama/refs/heads/main/sorular.json"
    
    veriler = {}
    durum_mesaji = ""
    
    try:
        # 1. Adım: İnternete Bağlan (3 saniye bekle)
        response = urllib.request.urlopen(URL, timeout=3)
        data_str = response.read().decode('utf-8')
        veriler = json.loads(data_str)
        
        # Başarılıysa hafızaya kaydet
        page.client_storage.set("kpss_full_data_v1", data_str)
        durum_mesaji = "Güncel (Online) ✅"
    except:
        # 2. Adım: İnternet yoksa hafızaya bak
        durum_mesaji = "Offline Mod 📂"
        if page.client_storage.contains_key("kpss_full_data_v1"):
            try:
                veriler = json.loads(page.client_storage.get("kpss_full_data_v1"))
            except:
                veriler = DEFAULT_VERI
        else:
            veriler = DEFAULT_VERI

    # --- VERİLERİ AYIKLA ---
    sorular = veriler.get("sorular", [])
    # Ayarları güvenli şekilde birleştir (Eksik varsa varsayılanı kullan)
    genel_ayar = {**DEFAULT_VERI["ayarlar"], **veriler.get("ayarlar", {})}
    tasarim = {**DEFAULT_VERI["tasarim"], **veriler.get("tasarim", {})}

    # --- GÜNCELLEME KONTROL SİSTEMİ ---
    net_versiyon = genel_ayar.get("apk_versiyonu", 1.0)
    indirme_linki = genel_ayar.get("apk_indirme_linki", "https://github.com")

    if net_versiyon > MEVCUT_VERSIYON:
        def linke_git(e):
            page.launch_url(indirme_linki)
            
        dlg = ft.AlertDialog(
            title=ft.Text("YENİ GÜNCELLEME VAR! 🚀"),
            content=ft.Text("Yeni özellikler eklendi. Lütfen son sürümü indirin."),
            actions=[
                ft.ElevatedButton("İndirmeye Git", on_click=linke_git, bgcolor="green", color="white"),
            ],
            modal=True,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # --- TASARIM DEĞİŞKENLERİ ---
    BASLIK = genel_ayar.get("baslik")
    RENK = genel_ayar.get("tema_rengi")
    BG_RENK = genel_ayar.get("arka_plan_rengi")
    
    RADIUS = tasarim.get("buton_yuvarlakligi", 10)
    FONT_SORU = tasarim.get("soru_yazi_boyutu", 18)
    FONT_SIK = tasarim.get("sik_yazi_boyutu", 16)
    ORTALA = ft.MainAxisAlignment.CENTER if tasarim.get("baslik_ortala") else ft.MainAxisAlignment.START
    GOLGE = ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.1, "black")) if tasarim.get("golge_olsun_mu") else None

    # Sayfa Ayarları
    page.bgcolor = BG_RENK
    page.title = BASLIK

    # Değişkenler
    mevcut_index = 0
    toplam_puan = 0
    dogru = 0
    yanlis = 0
    kalan_sure = genel_ayar.get("toplam_sure_dakika", 0) * 60
    sure_var = genel_ayar.get("sure_var_mi", False)

    # --- ARAYÜZ ---
    txt_baslik = ft.Text(BASLIK, size=20, weight="bold", color="white")
    txt_bilgi = ft.Text(durum_mesaji, color="white70", size=12)
    txt_puan = ft.Text("Puan: 0", color="white")
    txt_sure = ft.Text("", color="white", weight="bold")

    header = ft.Container(
        content=ft.Column([
            ft.Row([txt_baslik], alignment=ORTALA),
            ft.Row([txt_bilgi], alignment=ORTALA),
            ft.Row([txt_sure, txt_puan], alignment="spaceBetween")
        ]),
        bgcolor=RENK,
        padding=20,
        border_radius=ft.border_radius.only(bottom_left=RADIUS, bottom_right=RADIUS)
    )

    async def zamanlayici():
        nonlocal kalan_sure
        while kalan_sure > 0 and sure_var:
            dk, sn = divmod(kalan_sure, 60)
            txt_sure.value = f"{dk:02d}:{sn:02d}"
            txt_sure.update()
            kalan_sure -= 1
            await asyncio.sleep(1)
        if sure_var and kalan_sure <= 0:
            txt_sure.value = "SÜRE BİTTİ"
            txt_sure.update()

    def ciz():
        nonlocal mevcut_index
        ana_liste.controls.clear()
        ana_liste.controls.append(header)
        ana_liste.controls.append(ft.Container(height=20))

        if not sorular:
            ana_liste.controls.append(ft.Text("Soru Yok veya İnternet Hatası", color="red", text_align="center"))
            page.update()
            return

        if mevcut_index < len(sorular):
            soru = sorular[mevcut_index]
            
            # Soru Kutusu
            ana_liste.controls.append(
                ft.Container(
                    content=ft.Text(soru["metin"], size=FONT_SORU, color="black"),
                    bgcolor="white",
                    padding=20,
                    margin=10,
                    border_radius=RADIUS,
                    shadow=GOLGE
                )
            )

            # Şıklar
            for sec in soru["secenekler"]:
                btn = ft.Container(
                    content=ft.Text(sec, size=FONT_SIK, weight="w500"),
                    bgcolor="white",
                    padding=15,
                    margin=ft.margin.symmetric(horizontal=15, vertical=5),
                    border=ft.border.all(1, RENK),
                    border_radius=RADIUS,
                    on_click=lambda e, s=sec: cevapla(e, s),
                    ink=True
                )
                ana_liste.controls.append(btn)
        else:
            ana_liste.controls.append(
                ft.Column([
                    ft.Text("TEST BİTTİ", size=30, color=RENK, weight="bold"),
                    ft.Text(f"Toplam Puan: {toplam_puan}", size=20),
                    ft.Text(f"Doğru: {dogru} | Yanlış: {yanlis}", size=16),
                    ft.ElevatedButton("Yenile", on_click=lambda _: page.window_reload(), bgcolor=RENK, color="white")
                ], horizontal_alignment="center", spacing=10)
            )
        page.update()

    def cevapla(e, secilen):
        nonlocal toplam_puan, dogru, yanlis
        data = sorular[mevcut_index]
        dogru_cvp = data.get("cevap") or data.get("dogru_cevap")
        
        kutu = e.control
        if secilen == dogru_cvp:
            dogru += 1
            toplam_puan += genel_ayar.get("puan_dogru", 5)
            kutu.bgcolor = ft.colors.GREEN_100
            kutu.border = ft.border.all(2, "green")
        else:
            yanlis += 1
            toplam_puan += genel_ayar.get("puan_yanlis", 0)
            kutu.bgcolor = ft.colors.RED_100
            kutu.border = ft.border.all(2, "red")
        
        txt_puan.value = f"Puan: {toplam_puan}"
        header.update()
        kutu.update()
        
        ana_liste.controls.append(
            ft.Container(
                content=ft.ElevatedButton("SONRAKİ >", on_click=lambda _: sonraki(), bgcolor=RENK, color="white"),
                padding=20, alignment=ft.alignment.center
            )
        )
        page.update()

    def sonraki():
        nonlocal mevcut_index
        mevcut_index += 1
        ciz()

    ciz()
    if sure_var:
        page.run_task(zamanlayici)

ft.app(target=main)
