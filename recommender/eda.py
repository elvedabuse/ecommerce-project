import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Dosyaları yükle
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')
order_products = pd.read_csv('order_products__prior.csv')  # Burayı yeni ekledik

# Veri setlerinin ilk bilgilerini göster
print("Orders Veri Seti Genel Bilgi:")
print(orders.info())
print("\nOrders Veri Seti İlk 5 Satır:")
print(orders.head())

print("\nProducts Veri Seti Genel Bilgi:")
print(products.info())
print("\nProducts Veri Seti İlk 5 Satır:")
print(products.head())

print("\nOrders eksik veri sayısı:")
print(orders.isnull().sum())

print("\nProducts eksik veri sayısı:")
print(products.isnull().sum())

# 🔗 Ürün bilgilerini sipariş edilen ürünlerle birleştir
merged = pd.merge(order_products, products, on='product_id', how='left')

# 📊 En çok satılan 10 ürünü bul
top_products = merged['product_name'].value_counts().head(10)
print("\nEn Popüler 10 Ürün:")
print(top_products)

# 🎨 Grafikle göster
plt.figure(figsize=(10,6))
sns.barplot(x=top_products.values, y=top_products.index, hue=top_products.index, palette='magma', legend=False)
plt.title('En Popüler 10 Ürün')
plt.xlabel('Satış Adedi')
plt.ylabel('Ürün')
plt.tight_layout()
plt.show()


# ===============================
# ZAMAN ANALİZİ: Sipariş Zaman Davranışı
# ===============================

import matplotlib.pyplot as plt
import seaborn as sns

# Haftanın günlerine göre sipariş sayısı
plt.figure(figsize=(8,5))
sns.countplot(data=orders, x='order_dow', hue='order_dow', palette='viridis', legend=False)
plt.title('Haftanın Günlerine Göre Sipariş Dağılımı (0=Pazar)')
plt.xlabel('Haftanın Günü (0=Pazar, 6=Cumartesi)')
plt.ylabel('Sipariş Sayısı')
plt.tight_layout()
plt.show()

# Saatlere göre sipariş sayısı
plt.figure(figsize=(10,5))
sns.countplot(data=orders, x='order_hour_of_day', hue='order_hour_of_day', palette='coolwarm', legend=False)
plt.title('Günün Saatlerine Göre Sipariş Dağılımı')
plt.xlabel('Saat')
plt.ylabel('Sipariş Sayısı')
plt.tight_layout()
plt.show()

# Gün ve saat birleşimi: heatmap
heatmap_data = orders.groupby(['order_dow', 'order_hour_of_day']).size().unstack()

plt.figure(figsize=(12,6))
sns.heatmap(heatmap_data, cmap='YlGnBu')
plt.title('Gün ve Saat Bazlı Sipariş Yoğunluğu')
plt.xlabel('Saat')
plt.ylabel('Gün (0=Pazar)')
plt.tight_layout()
plt.show()



# ===============================
# TEKRAR SİPARİŞ ANALİZİ
# ===============================

order_products_prior = pd.read_csv("order_products__prior.csv")

# Yeniden sipariş edilen ürün yüzdesi
reorder_rate = order_products_prior['reordered'].mean()
print(f"Genel Tekrar Sipariş Oranı: {reorder_rate:.2f}")

# Ürün bazında tekrar sipariş yüzdesi
product_reorder = order_products_prior.groupby('product_id')['reordered'].mean().reset_index()
product_reorder = product_reorder.merge(products, on='product_id')
top_reordered = product_reorder.sort_values(by='reordered', ascending=False).head(10)

# Görselleştir
plt.figure(figsize=(10,5))
sns.barplot(data=top_reordered, x='reordered', y='product_name', hue='product_name', palette='viridis', legend=False)
plt.title('En Çok Tekrar Sipariş Edilen 10 Ürün')
plt.xlabel('Tekrar Sipariş Oranı')
plt.ylabel('Ürün Adı')
plt.tight_layout()
plt.show()
