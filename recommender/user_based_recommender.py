import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity

# 1. Veri Yükleme ve Birleştirme
print("Veriler yükleniyor...")
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')
order_products__prior = pd.read_csv('order_products__prior.csv')

merged_df = pd.merge(order_products__prior, orders, on='order_id')
merged_df = pd.merge(merged_df, products, on='product_id')

# 2. Aktif kullanıcılar ve popüler ürünler için filtre
user_counts = merged_df['user_id'].value_counts()
product_counts = merged_df['product_id'].value_counts()

active_users = user_counts[user_counts > 100].index
popular_products = product_counts[product_counts > 100].index

filtered_df = merged_df[(merged_df['user_id'].isin(active_users)) & 
                        (merged_df['product_id'].isin(popular_products))]

print(f"Filtrelenmiş veri boyutu: {filtered_df.shape}")

# 3. Örnekleme (%1)
sampled_df = filtered_df.sample(frac=0.01, random_state=42)
print(f"Örneklenmiş veri boyutu: {sampled_df.shape}")

# 4. Kullanıcı ve ürün kodlama
user_codes, user_uniques = pd.factorize(sampled_df['user_id'])
product_codes, product_uniques = pd.factorize(sampled_df['product_id'])

# 5. Sparse kullanıcı-ürün matrisi oluşturma
user_product_matrix = coo_matrix(
    (np.ones(len(sampled_df)), (user_codes, product_codes)),
    shape=(len(user_uniques), len(product_uniques))
)

print("Sparse kullanıcı-ürün matrisi oluşturuldu.")
print(f"Matris boyutu: {user_product_matrix.shape}")

# 6. Kullanıcı benzerlik matrisi hesaplama
print("Kullanıcı benzerlik matrisi hesaplanıyor...")
user_similarity = cosine_similarity(user_product_matrix, dense_output=False)
print("Kullanıcı benzerlik matrisi oluşturuldu.")

# 7. Öneri fonksiyonu
def recommend_products_for_user(target_user_id, top_n=5, top_k_sim_users=10):
    if target_user_id not in user_uniques:
        print("Kullanıcı bulunamadı.")
        return []
    
    user_idx = np.where(user_uniques == target_user_id)[0][0]
    
    sim_scores = user_similarity[user_idx].toarray().flatten()
    sim_scores[user_idx] = 0  # kendisi hariç
    
    similar_users_idx = sim_scores.argsort()[::-1][:top_k_sim_users]
    
    user_products = set(product_codes[user_codes == user_idx])
    
    recommended_products = {}
    for sim_user_idx in similar_users_idx:
        sim_user_products = product_codes[user_codes == sim_user_idx]
        for p in sim_user_products:
            if p not in user_products:
                recommended_products[p] = recommended_products.get(p, 0) + sim_scores[sim_user_idx]
    
    recommended_products = sorted(recommended_products.items(), key=lambda x: x[1], reverse=True)
    
    recommended_products_real_ids = [product_uniques[p[0]] for p in recommended_products[:top_n]]
    
    return recommended_products_real_ids

# 8. Örnek öneri denemesi
target_user = user_uniques[0]
print(f"\nKullanıcı {target_user} için önerilen ürünler:")
recommendations = recommend_products_for_user(target_user)
for pid in recommendations:
    product_name = products.loc[products['product_id'] == pid, 'product_name'].values[0]
    print(f"- {product_name} (ID: {pid})")
