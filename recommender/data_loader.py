import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
import pickle

# Verileri oku
orders = pd.read_csv("C:/Users/Elveda Buse/ecommerce_project/recommender/orders_demo.csv")
products = pd.read_csv("C:/Users/Elveda Buse/ecommerce_project/recommender/products_demo.csv")
order_products__prior = pd.read_csv("C:/Users/Elveda Buse/ecommerce_project/recommender/order_products__prior_demo.csv")

# Veri setlerini birleştir
merged_df = pd.merge(order_products__prior, orders, on='order_id')
merged_df = pd.merge(merged_df, products, on='product_id')

# Kullanıcı ve ürünlerin alışveriş sayılarını hesapla
user_counts = merged_df['user_id'].value_counts()
product_counts = merged_df['product_id'].value_counts()

# Eşik belirle (örneğin 400 ve 100)
active_users = user_counts[user_counts > 400].index
popular_products = product_counts[product_counts > 100].index

# Filtreleme uygula
filtered_df = merged_df[
    (merged_df['user_id'].isin(active_users)) & 
    (merged_df['product_id'].isin(popular_products))
]

print(f"Filtrelenmiş veri boyutu: {filtered_df.shape}")

# Örneklem al (%10)
sampled_df = filtered_df.sample(frac=0.1, random_state=42)

print(f"Örneklenmiş veri boyutu: {sampled_df.shape}")

# Kullanıcı-ürün matrisini oluştur
user_codes, user_uniques = pd.factorize(sampled_df['user_id'])
product_codes, product_uniques = pd.factorize(sampled_df['product_id'])

user_product_coo = coo_matrix(
    (np.ones(len(sampled_df)), (user_codes, product_codes)),
    shape=(len(user_uniques), len(product_uniques))
)

# csr formatına çevir (daha hızlı işlemler için)
user_product_csr = user_product_coo.tocsr()

print("Sparse kullanıcı-ürün matrisi oluşturuldu.")
print(f"Matris boyutu: {user_product_csr.shape}")

# Pickle ile kaydet
with open('processed_data.pkl', 'wb') as f:
    pickle.dump({
        'user_product_sparse_matrix': user_product_csr,
        'product_uniques': product_uniques
    }, f)

print("Veriler pickle dosyasına kaydedildi.")
