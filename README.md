# Ecommerce Project - XML & Web Services

Bu proje, Flask ile geliştirilmiş bir e-ticaret uygulamasıdır.  
Projede **XML ve JSON** formatlarında veri alışverişi yapılmakta,  
**XPath, XSLT, XML Schema (XSD)** gibi XML teknolojileri etkin şekilde kullanılmaktadır.

---

## Proje Özellikleri

- Kullanıcı kaydı, giriş ve oturum yönetimi
- Ürün listeleme, kategoriye göre filtreleme
- Sepete ürün ekleme/çıkarma, sepet görüntüleme
- Sipariş oluşturma ve kaydetme (JSON ve XML desteği)
- API üzerinden ürün ve sipariş verisi sağlama (JSON/XML)
- Swagger (Flasgger) ile API dokümantasyonu
- TCMB döviz kuru XML servisinden canlı veri çekme
- XML dosyalarından XPath ile veri okuma
- XSLT ile XML'den HTML dönüşümü yapma
- Basit API key ile güvenlik kontrolü
- Item-based öneri sistemi

---

## Kurulum

1. Depoyu klonlayın:
git clone https://github.com/elvedabuse/ecommerce-project.git
cd ecommerce-project

2.Sanal ortam oluşturun ve etkinleştirin:
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate

3.Gerekli paketleri yükleyin:
pip install -r requirements.txt

4.Uygulamayı çalıştırın:
python app.py

5.Tarayıcıda http://127.0.0.1:5000 adresine gidin.

## API Kullanımı

# Ürünleri Listeleme
JSON formatı için:
curl http://127.0.0.1:5000/api/v1/products

XML formatı için:
curl -H "Accept: application/xml" http://127.0.0.1:5000/api/v1/products

# Siparişler
Kullanıcı giriş yaptıktan sonra sipariş sorgulama:
curl -H "X-API-KEY: 123456" -H "Accept: application/xml" http://127.0.0.1:5000/orders
Yeni sipariş ekleme (XML örnek):
curl -X POST -H "Content-Type: application/xml" -H "X-API-KEY: 123456" --data @order.xml http://127.0.0.1:5000/orders

## Swagger
API dokümantasyonuna tarayıcıdan aşağıdaki adresten ulaşabilirsiniz:
http://127.0.0.1:5000/apidocs

## Dosyalar ve Klasörler
app.py : Ana Flask uygulaması

recommender/ : Öneri sistemi modülleri ve veri

templates/ : HTML şablonları

static/ : CSS ve görseller (varsa)

orders.xml, orders.xsd, orders.xsl : XML veri ve şema dosyaları

users.json, orders.json : JSON tabanlı veri dosyaları


## Notlar
API erişimi için X-API-KEY başlığı zorunludur.

Sipariş verisi JSON ve XML formatında alınır ve kaydedilir.

TCMB güncel döviz kuru XML servisi ile entegredir.

Projede temel güvenlik önlemleri vardır ancak production için geliştirilmelidir.

## Lisans
Bu proje sadece eğitim amaçlıdır. Ticari kullanım için uygun değildir.

## İletişim
Elveda Buse Akbulut
https://github.com/elvedabuse
https://tr.linkedin.com/in/elveda-buse-akbulut-55379b238
