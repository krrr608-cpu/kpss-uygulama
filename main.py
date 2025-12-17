import flet as ft

# --- SORULAR (Aynı sorular) ---
SORULAR = [
    {
        "metin": "İnsan, düşünen bir varlık olmasının yanında, hisseden de bir canlıdır. Sadece mantık süzgecinden geçen kararlar her zaman insanı mutlu etmeyebilir.",
        "secenekler": ["Mantık her zaman üstündür.", "Duygular karar almada önemlidir.", "İnsan sadece düşünür.", "Mutluluk mantıkla gelir.", "Problemler çözümsüzdür."],
        "cevap": "Duygular karar almada önemlidir."
    },
    {
        "metin": "Tarih boyunca medeniyetler su kenarlarında kurulmuştur. Nil, Fırat, Dicle gibi nehirler sadece tarım için değil, ticaret ve ulaşım için de hayati önem taşımıştır.",
        "secenekler": ["Su hayati önem taşır.", "Nehirler ticareti geliştirir.", "Medeniyetler dağlara kurulur.", "Tarım için su gereklidir.", "Ulaşım nehirlerle sağlanır."],
        "cevap": "Medeniyetler dağlara kurulur."
    }
]

def main(page: ft.Page):
    # --- KRİTİK AYARLAR (Çökmeyi önleyen ayarlar) ---
    page.title = "KPSS"
    page.padding = 0  # Kenar boşluğunu sıfırladık
    # page.scroll komutunu SİLDİK (Çökme sebebi olabilir)
    
    # Elemanları tutacak güvenli liste (ListView mobilde daha stabildir)
    liste = ft.ListView(expand=True, spacing=10, padding=20)
    page.add(liste)

    mevcut_index = 0
    dogru_sayisi = 0
    yanlis_sayisi = 0

    # --- ARAYÜZ OLUŞTURUCU ---
    def arayuzu_ciz():
        nonlocal mevcut_index
        liste.controls.clear() # Ekranı temizle

        if mevcut_index < len(SORULAR):
            soru = SORULAR[mevcut_index]
            
            # Başlık
            liste.controls.append(ft.Text(f"SORU {mevcut_index + 1}", size=20, weight="bold", color="blue"))
            
            # Soru Metni (Basit Text, Container yok)
            liste.controls.append(ft.Text(soru["metin"], size=16))
            liste.controls.append(ft.Divider())

            # Şıklar
            for secenek in soru["secenekler"]:
                btn = ft.ElevatedButton(
                    text=secenek,
                    data=secenek,
                    on_click=cevap_kontrol,
                    bgcolor="white",
                    color="black"
                    # width, height ve style ayarlarını kaldırdık (Sadelik iyidir)
                )
                liste.controls.append(btn)
                
        else:
            # Bitiş Ekranı
            liste.controls.append(ft.Text("TEST BİTTİ", size=30, color="green"))
            liste.controls.append(ft.Text(f"Doğru: {dogru_sayisi}", size=20))
            liste.controls.append(ft.Text(f"Yanlış: {yanlis_sayisi}", size=20))
            
        page.update()

    def cevap_kontrol(e):
        nonlocal dogru_sayisi, yanlis_sayisi
        secilen = e.control.data
        dogru = SORULAR[mevcut_index]["cevap"]

        if secilen == dogru:
            dogru_sayisi += 1
            e.control.bgcolor = "green"
            e.control.color = "white"
        else:
            yanlis_sayisi += 1
            e.control.bgcolor = "red"
            e.control.color = "white"
        
        e.control.text = f"{e.control.text} (SEÇİLDİ)"
        page.update()
        
        # Kullanıcı görsün diye azıcık bekleyip geçebiliriz ama şimdilik manuel buton koyalım
        liste.controls.append(ft.ElevatedButton("SONRAKİ >", on_click=sonraki_soru, bgcolor="blue", color="white"))
        page.update()

    def sonraki_soru(e):
        nonlocal mevcut_index
        mevcut_index += 1
        arayuzu_ciz()

    # Uygulamayı başlat
    arayuzu_ciz()

ft.app(target=main)
