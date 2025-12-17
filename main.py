import flet as ft
import json
import urllib.request
import asyncio

def main(page: ft.Page):
    # --- VARSAYILAN AYARLAR (İnternet ve kayıt yoksa) ---
    DEFAULT_VERI = {
        "ayarlar": {
            "baslik": "KPSS (Varsayılan)",
            "tema_rengi": "grey",
            "arka_plan_rengi": "white",
            "sure_var_mi": False
        },
        "sorular": [] 
    }
    
    # Güvenli Mod Ayarları (Siyah ekranı engeller)
    page.padding = 0
    page.spacing = 0
    ana_liste = ft.ListView(expand=True, spacing=0, padding=0)
    page.add(ana_liste)

    # --- VERİ ÇEKME VE KAYDETME MERKEZİ ---
    # Senin verdiğin özel link burada 👇
    URL = "https://raw.githubusercontent.com/krrr608-cpu/kpss-uygulama/refs/heads/main/sorular.json"
    
    veriler = {}
    durum_mesaji = ""
    
    try:
        # 1. Adım: İnternete Bağlanmayı Dene
        # Timeout=3 sn yaptık ki uygulama açılışta çok beklemesin
        response = urllib.request.urlopen(URL, timeout=3) 
        data_str = response.read().decode('utf-8')
        veriler = json.loads(data_str)
        
        # 2. Adım: Başarılıysa veriyi telefona kaydet (Önbellekleme)
        page.client_storage.set("kpss_son_veri", data_str)
        durum_mesaji = "Veriler Güncel (İnternet) ✅"
        print("İnternetten çekildi ve kaydedildi.")
        
    except Exception as e:
        # 3. Adım: İnternet Yoksa, Hafızaya Bak
        print(f"Hata oluştu: {e}")
        durum_mesaji = "İnternet Yok - Kayıtlı Veri Açıldı 📂"
        
        if page.client_storage.contains_key("kpss_son_veri"):
            kayitli_data = page.client_storage.get("kpss_son_veri")
            try:
                veriler = json.loads(kayitli_data)
            except:
                veriler = DEFAULT_VERI
                durum_mesaji = "Kayıtlı veri bozuk! ❌"
        else:
            veriler = DEFAULT_VERI
            durum_mesaji = "İnternet yok ve kayıt bulunamadı! ❌"

    # Verileri Ayıkla
    sorular = veriler.get("sorular", [])
    # Ayarları alırken varsayılan değerleri koru
    gelen_ayarlar = veriler.get("ayarlar", {})
    varsayilan_ayarlar = DEFAULT_VERI["ayarlar"]
    
    # Gelen ayarlarla varsayılanları birleştir (Eksik ayar varsa hata vermesin)
    ayarlar = {**varsayilan_ayarlar, **gelen_ayarlar}

    # --- AYARLARI UYGULA ---
    page.title = ayarlar.get("baslik")
    page.bgcolor = ayarlar.get("arka_plan_rengi")
    ANA_RENK = ayarlar.get("tema_rengi")
    
    # Değişkenler
    mevcut_index = 0
    toplam_puan = 0
    dogru_sayisi = 0
    yanlis_sayisi = 0
    
    # Süre ve Puan Ayarları
    kalan_saniye = ayarlar.get("toplam_sure_dakika", 0) * 60
    sure_aktif = ayarlar.get("sure_var_mi", False)
    puan_d = ayarlar.get("puan_dogru", 5)
    puan_y = ayarlar.get("puan_yanlis", 0)

    # --- ARAYÜZ ELEMANLARI ---
    txt_baslik = ft.Text(ayarlar.get("baslik"), size=20, weight="bold", color="white")
    txt_puan = ft.Text(f"Puan: 0", color="white")
    txt_sure = ft.Text("", color="white", weight="bold", size=16)
    txt_durum = ft.Text(durum_mesaji, color="white70", size=12) 
    
    header = ft.Container(
        content=ft.Column([
            ft.Row([txt_baslik], alignment="center"),
            ft.Row([txt_durum], alignment="center"),
            ft.Row([txt_sure, txt_puan], alignment="spaceBetween")
        ]),
        bgcolor=ANA_RENK,
        padding=15,
        border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
    )

    # --- ZAMANLAYICI ---
    async def sureyi_baslat():
        nonlocal kalan_saniye
        while kalan_saniye > 0 and sure_aktif:
            dk = kalan_saniye // 60
            sn = kalan_saniye % 60
            txt_sure.value = f"⏳ {dk:02d}:{sn:02d}"
            kalan_saniye -= 1
            txt_sure.update()
            await asyncio.sleep(1)
        
        if sure_aktif and kalan_saniye <= 0:
            txt_sure.value = "SÜRE BİTTİ!"
            txt_sure.update()

    # --- EKRAN ÇİZİMİ ---
    def ekrani_ciz():
        nonlocal mevcut_index
        ana_liste.controls.clear()
        ana_liste.controls.append(header)
        ana_liste.controls.append(ft.Container(height=20))

        if not sorular:
            ana_liste.controls.append(ft.Text("Gösterilecek soru yok.\nLütfen internete bağlanıp uygulamayı yeniden açın.", color="red", text_align="center"))
            page.update()
            return

        if mevcut_index < len(sorular):
            soru = sorular[mevcut_index]
            
            ana_liste.controls.append(
                ft.Container(
                    content=ft.Text(soru["metin"], size=18, color="black"),
                    bgcolor="white", padding=15, margin=10, border_radius=10
                )
            )

            for secenek in soru["secenekler"]:
                btn = ft.Container(
                    content=ft.Text(secenek, size=16),
                    bgcolor="white",
                    padding=15,
                    margin=ft.margin.symmetric(horizontal=10, vertical=5),
                    border=ft.border.all(1, ANA_RENK),
                    border_radius=8,
                    on_click=lambda e, s=secenek: cevap_ver(e, s),
                    ink=True
                )
                ana_liste.controls.append(btn)
            
            ana_liste.controls.append(ft.Container(height=50)) # Alt boşluk

        else:
            # Bitiş Ekranı
            ana_liste.controls.append(
                ft.Column([
                    ft.Text("TEST TAMAMLANDI", size=30, weight="bold", color=ANA_RENK),
                    ft.Text(f"Toplam Puan: {toplam_puan}", size=25, color="green"),
                    ft.Text(f"Doğru: {dogru_sayisi} | Yanlış: {yanlis_sayisi}", size=18),
                    ft.ElevatedButton("Yenile / Güncelle", on_click=lambda _: page.window_reload(), bgcolor=ANA_RENK, color="white")
                ], horizontal_alignment="center", spacing=10)
            )
            
        page.update()

    def cevap_ver(e, secilen):
        nonlocal toplam_puan, dogru_sayisi, yanlis_sayisi
        
        # Cevap anahtarını bul (hem "cevap" hem "dogru_cevap" alanını kontrol et)
        soru_data = sorular[mevcut_index]
        dogru_cvp = soru_data.get("cevap") or soru_data.get("dogru_cevap")
        
        kutucuk = e.control
        
        if secilen == dogru_cvp:
            dogru_sayisi += 1
            toplam_puan += puan_d
            kutucuk.bgcolor = ft.colors.GREEN_100
            kutucuk.border = ft.border.all(2, "green")
        else:
            yanlis_sayisi += 1
            toplam_puan += puan_y
            kutucuk.bgcolor = ft.colors.RED_100
            kutucuk.border = ft.border.all(2, "red")

        txt_puan.value = f"Puan: {toplam_puan}"
        header.update()
        kutucuk.update()
        
        # Sonraki butonu
        ana_liste.controls.append(
            ft.Container(
                content=ft.ElevatedButton("SONRAKİ >", on_click=lambda _: sonraki(), bgcolor=ANA_RENK, color="white"),
                padding=20, alignment=ft.alignment.center
            )
        )
        page.update()

    def sonraki():
        nonlocal mevcut_index
        mevcut_index += 1
        ekrani_ciz()

    ekrani_ciz()
    if sure_aktif:
        page.run_task(sureyi_baslat)

ft.app(target=main)
