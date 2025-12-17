import flet as ft
import time
import asyncio

# --- SORULAR BURAYA ---
# İleride soru eklemek istersen buradaki listeye virgül koyup yenisini ekleyebilirsin.
SORULAR_LISTESI = [
  {
    "id": 1,
    "metin": "İnsan, düşünen bir varlık olmasının yanında, hisseden de bir canlıdır. Sadece mantık süzgecinden geçen kararlar her zaman insanı mutlu etmeyebilir. Duyguların rehberliği, bazen en karmaşık mantık problemlerinden daha doğru bir çıkış yolu sunar. Bu parçada asıl anlatılmak istenen nedir?",
    "secenekler": ["Mantık her zaman duygudan üstündür.", "Duygular karar almada mantık kadar önemlidir.", "İnsan sadece düşünen bir varlıktır.", "Mutluluk sadece mantıklı kararlarla gelir.", "Karmaşık problemler çözümsüzdür."],
    "dogru_cevap": "Duygular karar almada mantık kadar önemlidir."
  },
  {
    "id": 2,
    "metin": "Tarih boyunca medeniyetler su kenarlarında kurulmuştur. Nil, Fırat, Dicle gibi nehirler sadece tarım için değil, ticaret ve ulaşım için de hayati önem taşımıştır. Su, medeniyetin kan damarıdır. Bu parçaya göre medeniyetlerin su kenarına kurulma nedeni hangisi olamaz?",
    "secenekler": ["Tarımsal üretim", "Ticaret imkanları", "Ulaşım kolaylığı", "Sadece balıkçılık yapmak", "Hayati ihtiyaçlar"],
    "dogru_cevap": "Sadece balıkçılık yapmak"
  }
]

def main(page: ft.Page):
    page.title = "KPSS Paragraf"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.scroll = "adaptive"  # Mobilde kaydırmayı iyileştirir
    
    # Soruları doğrudan listeden al
    sorular = SORULAR_LISTESI

    mevcut_soru_index = 0
    dogru_sayisi = 0
    yanlis_sayisi = 0
    
    # --- ARAYÜZ ---
    baslik = ft.Text("KPSS Paragraf", size=20, weight="bold", color="blue")
    
    soru_metni = ft.Text("", size=18, color="black")
    soru_kutusu = ft.Container(
        content=soru_metni, 
        padding=15, 
        bgcolor=ft.colors.BLUE_50, 
        border_radius=10,
        border=ft.border.all(1, ft.colors.BLUE_100)
    )
    
    secenekler_column = ft.Column(spacing=10)
    sonuc_metni = ft.Text("", size=18, weight="bold")
    
    def sonraki_soru(e):
        nonlocal mevcut_soru_index
        mevcut_soru_index += 1
        sonuc_metni.value = ""
        soruyu_goster()

    btn_sonraki = ft.ElevatedButton("Sonraki Soru >", on_click=sonraki_soru, visible=False, bgcolor="blue", color="white")

    def cevap_kontrol(e):
        nonlocal dogru_sayisi, yanlis_sayisi
        secilen = e.control.data
        dogru = sorular[mevcut_soru_index]["dogru_cevap"]
        
        # Tüm butonları kilitle
        for btn in secenekler_column.controls:
            btn.disabled = True
            if btn.data == dogru:
                btn.bgcolor = ft.colors.GREEN_500
                btn.color = ft.colors.WHITE
            elif btn.data == secilen and secilen != dogru:
                btn.bgcolor = ft.colors.RED_500
                btn.color = ft.colors.WHITE
        
        if secilen == dogru:
            dogru_sayisi += 1
            sonuc_metni.value = "DOĞRU! 🎉"
            sonuc_metni.color = "green"
        else:
            yanlis_sayisi += 1
            sonuc_metni.value = "YANLIŞ!"
            sonuc_metni.color = "red"

        btn_sonraki.visible = True
        page.update()

    def soruyu_goster():
        if mevcut_soru_index < len(sorular):
            soru = sorular[mevcut_soru_index]
            soru_metni.value = f"Soru {mevcut_soru_index + 1}:\n{soru['metin']}"
            
            secenekler_column.controls.clear()
            for secenek in soru["secenekler"]:
                btn = ft.ElevatedButton(
                    text=secenek, 
                    data=secenek, 
                    on_click=cevap_kontrol, 
                    width=1000, # Ekrana yayılması için
                    height=50
                )
                secenekler_column.controls.append(btn)
            
            btn_sonraki.visible = False
            page.update()
        else:
            page.clean()
            page.vertical_alignment = "center"
            page.horizontal_alignment = "center"
            page.add(
                ft.Column([
                    ft.Text("TEST BİTTİ!", size=30, color="blue"),
                    ft.Text(f"Doğru: {dogru_sayisi}", size=22, color="green"),
                    ft.Text(f"Yanlış: {yanlis_sayisi}", size=22, color="red"),
                ], alignment="center")
            )

    page.add(
        baslik,
        ft.Divider(),
        soru_kutusu, 
        ft.SizedBox(height=10),
        secenekler_column, 
        ft.SizedBox(height=20),
        sonuc_metni, 
        btn_sonraki
    )
    
    soruyu_goster()

ft.app(target=main)
