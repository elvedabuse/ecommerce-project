import pandas as pd
from scipy.sparse import coo_matrix
import numpy as np

# Verileri oku
orders = pd.read_csv("orders.csv")
order_products_prior = pd.read_csv("order_products__prior.csv")

# order_id üzerinden user_id ile eşleştir
merged_df = pd.merge(order_products_prior, orders[['order_id', 'user_id']], on='order_id', how='left')

# Kullanıcı ve ürün ID'lerini sıralı index'e çevir
user_id_map = {id: i for i, id in enumerate(merged_df['user_id'].unique())}
product_id_map = {id: i for i, id in enumerate(merged_df['product_id'].unique())}

# ID'leri index'e dönüştür
user_indices = merged_df['user_id'].map(user_id_map)
product_indices = merged_df['product_id'].map(product_id_map)

# Sparse matris oluştur (satır: kullanıcı, sütun: ürün, değer: sipariş sayısı)
data = np.ones(len(merged_df), dtype=np.int8)
sparse_matrix = coo_matrix((data, (user_indices, product_indices)))

print("Sparse kullanıcı-ürün matrisi oluşturuldu.")
print("Matris boyutu:", sparse_matrix.shape)
