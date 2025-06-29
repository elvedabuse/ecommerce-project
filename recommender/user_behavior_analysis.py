import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

orders = pd.read_csv("C:/Users/Elveda Buse/ecommerce_project/recommender/orders_demo.csv") 

# Kullanıcı başına toplam sipariş sayısı
user_order_counts = orders.groupby('user_id')['order_id'].count().sort_values(ascending=False)

print("En çok sipariş veren ilk 10 kullanıcı:")
print(user_order_counts.head(10))

# Kullanıcı başına ortalama sipariş aralığı (days_since_prior_order sütunu)
# days_since_prior_order sütunu, siparişler arası gün farkını veriyor
# Kullanıcı bazında ortalamasını alalım (NaN hariç)
user_avg_days_between_orders = orders.groupby('user_id')['days_since_prior_order'].mean().sort_values()

print("\nKullanıcı başına ortalama sipariş aralığı (gün):")
print(user_avg_days_between_orders.head(10))

# Grafik: En çok sipariş veren ilk 10 kullanıcı
plt.figure(figsize=(12,6))
sns.barplot(x=user_order_counts.head(10).index.astype(str), y=user_order_counts.head(10).values, color='mediumseagreen')
plt.title("En Çok Sipariş Veren İlk 10 Kullanıcı")
plt.xlabel("User ID")
plt.ylabel("Sipariş Sayısı")
plt.show()

# Grafik: Ortalama sipariş aralığı (en düşük 10 kullanıcı)
plt.figure(figsize=(12,6))
sns.barplot(x=user_avg_days_between_orders.head(10).index.astype(str), y=user_avg_days_between_orders.head(10).values, color='coral')
plt.title("En Düşük Ortalama Sipariş Aralığına Sahip 10 Kullanıcı")
plt.xlabel("User ID")
plt.ylabel("Ortalama Sipariş Aralığı (gün)")
plt.show()
