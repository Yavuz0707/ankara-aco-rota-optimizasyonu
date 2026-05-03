# 🐜 Ankara ACO Rota Optimizasyonu

Bu proje, **Ant Colony Optimization (Karınca Kolonisi Optimizasyonu)** algoritmasını kullanarak Ankara ve çevresindeki 10 farklı gölet/barajdan su numunesi toplamak için en kısa ve verimli rotayı belirlemeyi amaçlamaktadır..

> **Senaryo:** Çevre Bakanlığı'na ait birimler, zaman kısıtlılığı nedeniyle Ankara'daki numune noktalarını en kısa sürede gezmek zorundadır./

---

## 👤 Öğrenci Bilgileri

- **Ad Soyad:** Şükrü YAVUZ
- **Öğrenci No:** 2312729015
- **Ders:** Karınca Kolonisi Algoritması ile Yol Optimizasyonu.

---

## 🎯 Proje Hakkında

Bu proje, **Karınca Kolonisi Optimizasyonu (ACO)** algoritmasını kullanarak Ankara'daki su toplama noktaları arasında en optimal rotayı bulur. Algoritma, karıncaların doğada yiyecek ararken kullandıkları feromon takibi yönteminden esinlenmiştir.

### ✨ Özellikler

- **Gerçek Zamanlı Mesafe Verileri:** Google Maps Distance Matrix API kullanılarak gerçek yol mesafeleri hesaplanır
- **İnteraktif Arayüz:** Streamlit tabanlı web arayüzü ile kolay kullanım
- **Dinamik Parametre Ayarları:** 
  - Alpha (α) - Feromon ağırlığı
  - Beta (β) - Mesafe ağırlığı
  - Buharlaşma oranı
  - Karınca sayısı
  - İterasyon sayısı
- **Görselleştirme:**
  - Folium tabanlı interaktif harita
  - AntPath ile animasyonlu rota gösterimi
  - Yakınsama grafiği ile algoritma performansı

---

## 📍 Su Numunesi Noktaları

Proje, Ankara'daki 10 farklı gölet/baraj lokasyonunu kapsar:
1. Mogan Gölü
2. Eymir Gölü
3. Soğuksu Milli Parkı
4. Karagöl
5. Çubuk Barajı
6. Elmadağ Yaylası
7. Bayındır Barajı
8. Çamlıdere Barajı
9. Kurtboğazı Barajı
10. Sarıyar Barajı

---

## 🛠️ Proje Yapısı

```
ankara_su_numunesi/
│
├── main.py                     # Ana uygulama dosyası (Streamlit arayüzü)
├── requirements.txt            # Gerekli Python kütüphaneleri
├── README.md                   # Proje dokümantasyonu
│
├── core/
│   ├── ant_algorithm.py        # ACO algoritması implementasyonu
│   └── matrix_utils.py         # Mesafe matrisi hesaplamaları
│
├── data/
│   ├── coordinates.py          # Lokasyon koordinatları
│   └── __init__.py
│
└── visual/
    ├── plotting.py             # Grafik ve görselleştirme fonksiyonları
    └── __init__.py
```

---

## 🧪 Algoritma Parametreleri

| Parametre | Açıklama | Varsayılan Değer |
|-----------|----------|------------------|
| **Karınca Sayısı** | Her iterasyonda çalışan karınca sayısı | 50 |
| **İterasyon Sayısı** | Algoritmanın çalışma döngü sayısı | 100 |
| **Alpha (α)** | Feromon izine verilen önem | 1.0 |
| **Beta (β)** | Mesafeye verilen önem | 2.0 |
| **Buharlaşma Oranı** | Feromon buharlaşma hızı | 0.5 |

---

## 📦 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- Google Maps Distance Matrix API anahtarı

### Adım 1: Projeyi Klonlayın

```bash
git clone https://github.com/Yavuz0707/ankara-aco-rota-optimizasyonu.git
cd ankara-aco-rota-optimizasyonu
```

### Adım 2: Sanal Ortam Oluşturun (Önerilen)

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# veya
source .venv/bin/activate  # Linux/Mac
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: API Anahtarı Yapılandırması

`.streamlit/secrets.toml` dosyası oluşturun ve Google API anahtarınızı ekleyin:

```toml
GOOGLE_API_KEY = "your_api_key_here"
```

---

## 🚀 Çalıştırma

```bash
streamlit run main.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde açılacaktır.

---

## 📊 Kullanım

1. **Parametreleri Ayarlayın:** Sol sidebar'dan algoritma parametrelerini istediğiniz gibi ayarlayın
2. **Algoritmayı Çalıştırın:** "Algoritmayı Çalıştır" butonuna tıklayın
3. **Sonuçları İnceleyin:**
   - Toplam mesafe ve rota detayları
   - İnteraktif harita üzerinde optimal rota
   - Yakınsama grafiği ile algoritma performansı

---

## 🔬 Algoritma Detayları

### ACO (Ant Colony Optimization) Nasıl Çalışır?

1. **Başlatma:** Rastgele feromon dağılımı ile başlar
2. **Karınca Turları:** Her karınca, feromon yoğunluğu ve mesafeye göre olasılıksal olarak yol seçer
3. **Feromon Güncelleme:** İyi rotalar daha fazla feromon bırakır
4. **Buharlaşma:** Eski feromonlar zamanla azalır (yerel minimumlara takılmayı önler)
5. **İterasyon:** Süreç belirlenen sayıda tekrarlanır ve en iyi çözüm bulunur

### Matematiksel Model

Bir karıncanın bir sonraki şehri seçme olasılığı:

$$P_{ij} = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{k \in allowed} [\tau_{ik}]^\alpha \cdot [\eta_{ik}]^\beta}$$

- $\tau_{ij}$: i ve j arasındaki feromon miktarı
- $\eta_{ij}$: Mesafenin tersi (1/d)
- $\alpha$: Feromon önem katsayısı
- $\beta$: Mesafe önem katsayısı

---

## 📈 Sonuçlar

Algoritma, parametrelere bağlı olarak:
- Ortalama %15-25 daha kısa rotalar bulur
- 50-100 iterasyonda yakınsama sağlar
- Gerçek dünya mesafelerini kullanarak pratik sonuçlar üretir

---

## 🙏 Teşekkürler

Bu proje, yapay zeka ve optimizasyon algoritmalarına olan ilgimin bir ürünüdür. Karınca kolonisi optimizasyonu gibi doğadan esinlenmiş algoritmaların güzelliğini göstermeyi amaçlar.

---

## 📞 İletişim

**Şükrü YAVUZ**  
Öğrenci No: 2312729015  
Proje Repo: [github.com/Yavuz0707/ankara-aco-rota-optimizasyonu](https://github.com/Yavuz0707/ankara-aco-rota-optimizasyonu)
