import flet as ft

# --- SORU BANKASI (Buraya virgül ile istediğin kadar soru ekleyebilirsin) ---
SORULAR = [
    {
        "metin": "İnsan, düşünen bir varlık olmasının yanında, hisseden de bir canlıdır. Sadece mantık süzgecinden geçen kararlar her zaman insanı mutlu etmeyebilir. Duyguların rehberliği, bazen en karmaşık mantık problemlerinden daha doğru bir çıkış yolu sunar. Bu parçada asıl anlatılmak istenen nedir?",
        "secenekler": ["Mantık her zaman üstündür.", "Duygular karar almada önemlidir.", "İnsan sadece düşünür.", "Mutluluk mantıkla gelir.", "Problemler çözümsüzdür."],
        "cevap": "Duygular karar almada önemlidir."
    },
    {
        "metin": "Tarih boyunca medeniyetler su kenarlarında kurulmuştur. Nil, Fırat, Dicle gibi nehirler sadece tarım için değil, ticaret ve ulaşım için de hayati önem taşımıştır. Bu parçaya göre hangisi söylenemez?",
        "secenekler": ["Su hayati önem taşır.", "Nehirler ticareti geliştirir.", "Medeniyetler dağlara kurulur.", "Tarım için su gereklidir.", "Ulaşım nehirlerle sağlanır."],
        "cevap": "Medeniyetler dağlara kurulur."
    },
    {
        "metin": "Bir yazarın üslubu, parmak izi gibidir. Konu ne kadar benzer olsa da, anlatım tarzı eseri biricik kılar. Okur, sayfaları çevirirken yazarın sesini duyar gibi olmalıdır. Bu parçada vurgulanan düşünce nedir?",
        "secenekler": ["Konu seçiminin önemi", "Yazarların benzerliği", "Üslubun özgünlüğü", "Okurun beklentileri", "Kitap sayfa sayısı"],
        "cevap": "Üslubun özgünlüğü"
    }
]

def main(page: ft.Page):
    # --- AYARLAR ---
    page.title = "KPSS Paragraf"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.scroll = "auto" # Ekranı kaydırma özelliği
    
    # Renk Paleti
    RENK_ANA = ft.colors.BLUE_700
    RENK_ARKA = ft.colors.BLUE_50

    # Değişkenler
    mevcut_index = 0
    dogru_sayisi = 0
    yanlis_sayisi = 0

    # --- ARAYÜZ ELEMANLARI ---
    baslik = ft.Container(
        content=ft.Text("KPSS PARAGRAF", size=20, weight="bold", color="white"),
        bgcolor=RENK_ANA,
        padding=15,
        border_radius=10,
        alignment=ft.alignment.center
    )

    soru_sayac = ft.Text(f"Soru: 1 / {len(SORULAR)}", size=14, weight="bold")
    
    # Soru Metni Kutusu
    soru_metni = ft.Text("", size=16, color="black")
    soru_kutusu = ft.Container(
        content=soru_metni,
        padding=15,
        bgcolor="white",
        border=ft.border.all(1, ft.colors.GREY_300),
        border_radius=8
    )

    # Şıkların olduğu alan
    siklar_kolonu = ft.Column(spacing=10)
    
    # Sonuç mesajı
    sonuc_mesaji = ft.Text("", size=16, weight="bold")
    
    # İleri Butonu
    btn_ileri = ft.ElevatedButton(
        "Sonraki Soru >", 
        icon=ft.icons.ARROW_FORWARD,
        bgcolor=RENK_ANA, 
        color="white",
        visible=False
    )

    # --- FONKSİYONLAR ---
    
    def ileri_git(e):
        nonlocal mevcut_index
        mevcut_index += 1
        btn_ileri.visible = False
        sonuc_mesaji.value = ""
        ekrani_guncelle()

    def cevap_ver(e):
        nonlocal dogru_sayisi, yanlis_sayisi
        secilen = e.control.text
        dogru = SORULAR[mevcut_index]["cevap"]

        # Butonları kilitle ve boya
        for btn in siklar_kolonu.controls:
            btn.disabled = True
            if btn.text == dogru:
                btn.bgcolor = ft.colors.GREEN_500
                btn.color = "white"
                btn.icon = ft.icons.CHECK
            elif btn.text == secilen and secilen != dogru:
                btn.bgcolor = ft.colors.RED_500
                btn.color = "white"
                btn.icon = ft.icons.CLOSE
        
        if secilen == dogru:
            dogru_sayisi += 1
            sonuc_mesaji.value = "TEBRİKLER! Doğru Cevap."
            sonuc_mesaji.color = "green"
        else:
            yanlis_sayisi += 1
            sonuc_mesaji.value = "YANLIŞ CEVAP!"
            sonuc_mesaji.color = "red"

        btn_ileri.on_click = ileri_git
        btn_ileri.visible = True
        page.update()

    def ekrani_guncelle():
        if mevcut_index < len(SORULAR):
            soru = SORULAR[mevcut_index]
            soru_sayac.value = f"Soru: {mevcut_index + 1} / {len(SORULAR)}"
            soru_metni.value = soru["metin"]
            
            siklar_kolonu.controls.clear()
            for secenek in soru["secenekler"]:
                btn = ft.ElevatedButton(
                    text=secenek,
                    width=1000, # Tam genişlik
                    bgcolor="white",
                    color="black",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=cevap_ver
                )
                siklar_kolonu.controls.append(btn)
            
            page.update()
        else:
            # Bitiş Ekranı
            page.clean()
            page.add(
                ft.Column([
                    ft.Icon(ft.icons.EMOJI_EVENTS, size=80, color="orange"),
                    ft.Text("TEST BİTTİ!", size=30, weight="bold"),
                    ft.Text(f"Doğru Sayısı: {dogru_sayisi}", size=20, color="green"),
                    ft.Text(f"Yanlış Sayısı: {yanlis_sayisi}", size=20, color="red"),
                    ft.ElevatedButton("Başa Dön", on_click=lambda _: page.window_reload())
                ], alignment="center", horizontal_alignment="center")
            )

    # --- BAŞLANGIÇ ---
    page.add(
        baslik,
        ft.SizedBox(height=10),
        soru_sayac,
        soru_kutusu,
        ft.SizedBox(height=20),
        siklar_kolonu,
        ft.SizedBox(height=20),
        sonuc_mesaji,
        btn_ileri
    )
    
    ekrani_guncelle()

ft.app(target=main)
