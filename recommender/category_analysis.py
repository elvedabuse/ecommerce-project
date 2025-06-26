import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV dosyalarını yükle
products = pd.read_csv("products.csv")
departments = pd.read_csv("departments.csv")
aisles = pd.read_csv("aisles.csv")
order_products = pd.read_csv("order_products__prior.csv")

# Ürün bilgilerini birleştir
products_merged = products.merge(departments, on='department_id').merge(aisles, on='aisle_id')

# Sipariş verileri ile birleştir
product_orders = order_products.merge(products_merged, on='product_id')

# En çok sipariş edilen 10 department (kategori)
top_departments = product_orders['department'].value_counts().head(10)
plt.figure(figsize=(10, 6))
# Örneğin ilk grafik için:
sns.barplot(x=top_departments.values, y=top_departments.index, hue=top_departments.index, legend=False, palette="Set2")
plt.title("En Popüler 10 Ürün Kategorisi (Department)")
plt.xlabel("Sipariş Sayısı")
plt.ylabel("Kategori")
plt.tight_layout()
plt.show()

# En popüler 10 aisle (raf)
top_aisles = product_orders['aisle'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_aisles.values, y=top_aisles.index, palette="Set3")
plt.title("En Popüler 10 Raf (Aisle)")
plt.xlabel("Sipariş Sayısı")
plt.ylabel("Aisle")
plt.tight_layout()
plt.show()
