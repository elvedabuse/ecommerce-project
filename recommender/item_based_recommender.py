import numpy as np
import pandas as pd
import pickle
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

class ItemBasedRecommender:
    def __init__(self, products_path, pickle_path='recommender/processed_data.pkl'):
        self.products_path = products_path
        self.pickle_path = pickle_path
        self.product_id_to_name = {}
        self.item_similarity = None
        self.product_uniques = None
        self.user_product_matrix = None

    def load_and_prepare_data(self):
        # Pickle dosyasını yükle
        with open(self.pickle_path, 'rb') as f:
            data = pickle.load(f)

        self.user_product_matrix = data['user_product_sparse_matrix']
        self.product_uniques = data['product_uniques']

        # Ürün adları için CSV'den eşleştirme yap
        products = pd.read_csv(self.products_path)
        self.product_id_to_name = dict(zip(
            products['product_id'],
            products['product_name']
        ))

    def calculate_similarity(self):
        if self.user_product_matrix is None:
            raise ValueError("Data not loaded yet. Call load_and_prepare_data() first.")
        self.item_similarity = cosine_similarity(self.user_product_matrix.T)

    def get_similar_products(self, product_id, top_n=5):
        if self.item_similarity is None:
            raise ValueError("Similarity matrix not computed. Call calculate_similarity() first.")
        try:
            product_index = list(self.product_uniques).index(product_id)
        except ValueError:
            return []  # Ürün bulunamazsa boş liste döner

        similarities = self.item_similarity[product_index]
        similar_indices = similarities.argsort()[::-1][1:top_n+1]

        results = []
        for idx in similar_indices:
            pid = self.product_uniques[idx]
            pname = self.product_id_to_name.get(pid, "Bilinmeyen Ürün")
            score = similarities[idx]
            results.append({'product_id': pid, 'product_name': pname, 'similarity': float(score)})
        return results
