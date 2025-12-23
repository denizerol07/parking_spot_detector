"""
PARK YERİ TESPİT SİSTEMİ - DÜZELTİLMİŞ
Mantık: Boş park yeri AÇIK renk, Araba konunca KOYU olur
"""

import cv2
import numpy as np

# =====================================================
# AYARLAR
# =====================================================

KAMERA = 1

# Sarı renk - geniş aralık
SARI_ALT = np.array([15, 80, 80])
SARI_UST = np.array([35, 255, 255])

MIN_ALAN = 2000

# EŞİK DEĞERİ - DÜŞÜK!
# MANTIK: Ortalama parlaklık
# Boş park = YÜKSEK parlaklık (açık zemin)
# Araba var = DÜŞÜK parlaklık (araba gölgesi)
PARLAKLIM_ESIK = 120  # 0-255 arası, ortalama gri değer

# =====================================================
# FONKSİYONLAR
# =====================================================

def sari_cerceveleri_bul(kare):
    hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, SARI_ALT, SARI_UST)
    
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    konturlar, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    park_yerleri = []
    
    for kontur in konturlar:
        alan = cv2.contourArea(kontur)
        if alan < MIN_ALAN:
            continue
        
        x, y, w, h = cv2.boundingRect(kontur)
        aspect_ratio = float(w) / h if h > 0 else 0
        
        if 0.2 < aspect_ratio < 5:
            koseler = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
            park_yerleri.append(koseler)
    
    park_yerleri.sort(key=lambda p: p[0][1])
    return park_yerleri


def park_yeri_kontrol(kare_gri, park_yeri_koseler):
    """
    YENİ MANTIK - PARLAKLIM KONTROLÜ
    
    Boş park yeri = AÇIK renk = Yüksek ortalama gri değer (>120)
    Araba var = KOYU renk = Düşük ortalama gri değer (<120)
    """
    mask = np.zeros(kare_gri.shape, dtype=np.uint8)
    pts = np.array(park_yeri_koseler, np.int32)
    cv2.fillPoly(mask, [pts], 255)
    
    # Park yerindeki pikselleri al
    park_alani = cv2.bitwise_and(kare_gri, mask)
    
    # Ortalama parlaklığı hesapla (sadece park yeri içinde)
    alan_pikseller = park_alani[mask == 255]
    
    if len(alan_pikseller) > 0:
        ortalama_parlaklim = np.mean(alan_pikseller)
    else:
        ortalama_parlaklim = 0
    
    # KARAR: Yüksek parlaklık = BOŞ, Düşük parlaklık = DOLU
    bos_mu = ortalama_parlaklim > PARLAKLIM_ESIK
    
    return bos_mu, ortalama_parlaklim


# =====================================================
# ANA PROGRAM
# =====================================================

def ana_program():
    print("=" * 60)
    print("  PARK YERİ TESPİT - PARLAKLIM KONTROLÜ")
    print("=" * 60)
    print("🟢 Yeşil = BOŞ (açık renk)")
    print("🔴 Kırmızı = DOLU (koyu renk, araba gölgesi)")
    print("\nKontroller:")
    print("  'q' = Çıkış")
    print("  'd' = Debug (gri görüntü)")
    print("  '+' = Eşik arttır (boş yere dolu diyorsa)")
    print("  '-' = Eşik azalt (dolu yere boş diyorsa)")
    print("=" * 60 + "\n")
    
    cap = cv2.VideoCapture(KAMERA)
    
    if not cap.isOpened():
        print("❌ Kamera açılamadı!")
        return
    
    print("✅ Kamera açıldı!")
    print("Telefonu park yerlerine doğrult...\n")
    
    debug_modu = False
    esik = PARLAKLIM_ESIK
    
    while True:
        ret, kare = cap.read()
        if not ret:
            break
        
        kare_kopya = kare.copy()
        
        # Gri tonlama
        kare_gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
        
        # Sarı çerçeveleri bul
        park_yerleri = sari_cerceveleri_bul(kare)
        
        bos = 0
        dolu = 0
        
        for i, park_yeri in enumerate(park_yerleri):
            bos_mu, parlaklim = park_yeri_kontrol(kare_gri, park_yeri)
            
            # Geçici eşik kullan
            bos_mu = parlaklim > esik
            
            pts = np.array(park_yeri, np.int32)
            
            # Renk ve durum
            if bos_mu:
                renk = (0, 255, 0)  # Yeşil
                durum = "BOS"
                bos += 1
            else:
                renk = (0, 0, 255)  # Kırmızı
                durum = "DOLU"
                dolu += 1
            
            # Çiz
            cv2.polylines(kare_kopya, [pts], True, renk, 4)
            
            cx = int(np.mean([p[0] for p in park_yeri]))
            cy = int(np.mean([p[1] for p in park_yeri]))
            
            # Durum
            cv2.putText(kare_kopya, durum, (cx-35, cy+25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, renk, 2)
        
        # İstatistik
        if len(park_yerleri) > 0:
            cv2.rectangle(kare_kopya, (15, 15), (320, 190), (0, 0, 0), -1)
            cv2.rectangle(kare_kopya, (15, 15), (320, 190), (255, 255, 255), 2)
            
            cv2.putText(kare_kopya, "PARK DURUMU", (25, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            cv2.putText(kare_kopya, f"Bos:  {bos}", (25, 115),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(kare_kopya, f"Dolu: {dolu}", (25, 145),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            print(f"\r🟢 Boş: {bos} | 🔴 Dolu: {dolu}",
                  end='', flush=True)
        else:
            h, w = kare_kopya.shape[:2]
        
        # Göster
        cv2.imshow("Park Yeri Tespiti", kare_kopya)
        
        if debug_modu:
            cv2.imshow("Debug - Gri Goruntu", kare_gri)
        
        # Klavye
        tus = cv2.waitKey(1) & 0xFF
        if tus == ord('q'):
            break
        elif tus == ord('d'):
            debug_modu = not debug_modu
            if not debug_modu:
                cv2.destroyWindow("Debug - Gri Goruntu")
        elif tus == ord('+') or tus == ord('='):
            esik += 5
            print(f"\n🔼 Eşik: {int(esik)} (Boş yere dolu diyorsa ARTTIR)")
        elif tus == ord('-') or tus == ord('_'):
            esik = max(50, esik - 5)
            print(f"\n🔽 Eşik: {int(esik)} (Dolu yere boş diyorsa AZALT)")
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n\nProgram kapatıldı. En iyi eşik: {int(esik)}")
    print("\nBu eşik değerini kodda PARLAKLIM_ESIK olarak kaydet!")


if __name__ == "__main__":
    ana_program()