# 🚗 Park Yeri Tespit Sistemi

OpenCV kullanarak gerçek zamanlı park yeri tespiti. Telefon kamerasıyla sarı çerçeveleri algılar, boş/dolu durumunu gösterir.

## 🎯 Ne İşe Yarar?

- 🟡 Sarı çerçeveleri otomatik algılar
- 🟢 Boş park yeri → Yeşil
- 🔴 Dolu park yeri → Kırmızı
- 📱 DroidCam ile telefon kamerası kullanır

## 🚀 Kurulum

```bash
# Projeyi indir
git clone https://github.com/denizerola/parking-spot-detector.git
cd parking-spot-detector

# Gereksinimleri yükle
pip install opencv-python numpy
```

## 💻 Kullanım

```bash
# Kamera ID'sini bul
python kamera_bul.py

# Programı çalıştır
python park_PARLAKLIM.py
```

## 🎮 Kontroller

- `q` - Çıkış
- `d` - Debug modu
- `+` - Eşik arttır (boş yere dolu diyorsa)
- `-` - Eşik azalt (dolu yere boş diyorsa)

## ⚙️ Ayarlar

`park_PARLAKLIM.py` dosyasında:

```python
KAMERA = 1              # Kamera numarası (0, 1, 2)
PARLAKLIM_ESIK = 120    # Hassasiyet (100-150 arası dene)
MIN_ALAN = 2000         # Minimum çerçeve boyutu
```

## 🔧 Nasıl Çalışır?

1. Sarı çerçeveleri bulur (HSV renk aralığı)
2. Her çerçevenin parlaklığını ölçer
3. Parlaklık > 120 → BOŞ
4. Parlaklık < 120 → DOLU (araba gölgesi)

## 📋 Gereksinimler

- Python 3.7+
- OpenCV
- NumPy
- DroidCam (telefon kamerası için)

## 🐛 Sorunlar?

**Sarı tespit edilmiyor:** Işığı aç veya `SARI_ALT/UST` değerlerini ayarla  
**Yanlış tespit:** `+/-` tuşlarıyla eşiği ayarla

## 👤 Yazar

**Deniz Erol**

## 📄 Lisans

MIT

---
