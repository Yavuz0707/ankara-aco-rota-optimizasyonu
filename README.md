# 🐜 Ankara ACO Su Numunesi Toplama Rota Optimizasyonu

## Karınca Kolonisi Algoritması ile Rota Optimizasyonu

Bu proje, **Karınca Kolonisi Optimizasyonu (Ant Colony Optimization – ACO)** algoritması kullanılarak  
Ankara ve çevresinde belirlenen **su numunesi toplama noktaları** için **en kısa ve en verimli rotanın**
belirlenmesini amaçlamaktadır.

Uygulama, gerçek mesafe verileri için **Google Maps Distance Matrix API**,  
görselleştirme için **Streamlit** ve **Folium** kütüphanelerini kullanmaktadır.

---

## 👤 Öğrenci Bilgileri

- **Ad Soyad:** Şükrü YAVUZ  
- **Öğrenci No:** 2312729015  
- **Yöntem:** Karınca Kolonisi Optimizasyonu (ACO)  
- **Uygulama Türü:** Gerçek mesafe verileri ile rota optimizasyonu  

---

## 🎯 Problem Tanımı

Su kaynaklarından numune toplama süreçlerinde, ziyaret edilecek noktaların sayısı arttıkça  
toplam yol uzunluğu ve zaman maliyeti önemli ölçüde artmaktadır.

Bu problem, tüm numune noktalarını **en az toplam mesafe** ile ziyaret eden bir rotanın
belirlenmesini gerektiren bir **kombinatoryal optimizasyon problemidir**.

Bu çalışmada amaç, verilen lokasyonlar için **toplam yol mesafesini minimize eden**
optimum rotayı belirlemektir.

---

## 🧠 Kullanılan Algoritma  
### Karınca Kolonisi Optimizasyonu (ACO)

Karınca Kolonisi Algoritması, karıncaların yiyecek ararken bıraktıkları **feromon izleri**
sayesinde en kısa yolu zamanla keşfetme davranışını temel alır.

Bu projede algoritma şu şekilde çalışmaktadır:

- Her karınca tüm lokasyonları ziyaret eden bir rota oluşturur  
- Kısa rotalar daha fazla feromon bırakır  
- Feromonlar zamanla buharlaşır (decay)  
- İterasyonlar ilerledikçe en iyi rota belirginleşir  

---

## 📍 Senaryo Tanımı – Ankara Su Numunesi Toplama

Çalışmada kullanılan lokasyonlar şunlardır:

- Merkez (Başlangıç Noktası)  
- Mogan Gölü  
- Eymir Gölü  
- Göksu Parkı  
- Mavi Göl  
- Çubuk-1 Barajı  
- Kurtboğazı Barajı  
- Karagöl  
- Soğuksu Milli Parkı  
- Kesikköprü Barajı  

Tüm mesafeler **Google Maps Distance Matrix API** üzerinden
**gerçek yol mesafesi (km)** olarak hesaplanmaktadır.

---

## ⚙️ Algoritma Parametreleri

Uygulamada kullanıcı tarafından ayarlanabilen parametreler:

- Karınca Sayısı (Popülasyon)  
- İterasyon Sayısı  
- Buharlaşma Oranı (Decay)  
- Feromon Etkisi (Alpha)  
- Mesafe Etkisi (Beta)  

Bu parametreler, algoritmanın yakınsama hızı ve çözüm kalitesi üzerinde doğrudan etkilidir.

---

## 📊 Görsel Çıktılar

- Folium ile interaktif harita  
- AntPath animasyonu ile optimum rota gösterimi  
- İterasyonlara göre toplam mesafe yakınsama grafiği  
- Detaylı durak sıralaması  

---

## 🔐 Google Maps API Kullanımı

API anahtarı güvenlik sebebiyle kod içerisinde tutulmamaktadır.

Aşağıdaki dosya oluşturulmalıdır:

.streamlit/secrets.toml

css
Kodu kopyala

Dosya içeriği:

```toml
GOOGLE_API_KEY = "API_ANAHTARINIZ"
🛠️ Kullanılan Teknolojiler
Python

Streamlit

NumPy

Pandas

Matplotlib

Folium

streamlit-folium

Google Maps Distance Matrix API

🚀 Uygulamanın Çalıştırılması
bash
Kodu kopyala
pip install streamlit folium streamlit-folium numpy pandas matplotlib requests
streamlit run app.py
📌 Sonuç ve Değerlendirme
Bu çalışma, doğadan ilham alan optimizasyon algoritmalarının
gerçek hayat problemlerine başarıyla uygulanabileceğini göstermektedir.

Karınca Kolonisi Algoritması, uygun parametrelerle
kararlı ve verimli sonuçlar üretmiş,
harita ve grafikler ile sonuçlar görsel olarak desteklenmiştir.
