import pandas as pd

# Orijinal ürün listesini oku
products = pd.read_csv("recommender/products.csv")

# İlk 100 ürünü seç (örneklem)
products_demo = products.head(100)

# Bu ürünlerle ilişkili order_products kayıtlarını al
order_products = pd.read_csv("recommender/order_products__prior.csv")
order_products_demo = order_products[order_products['product_id'].isin(products_demo['product_id'])]

# Bu order_product kayıtlarındaki order_id'lere göre orders.csv'yi filtrele
orders = pd.read_csv("recommender/orders.csv")
orders_demo = orders[orders['order_id'].isin(order_products_demo['order_id'])]

# Kaydet (demo versiyonları)
products_demo.to_csv("recommender/products_demo.csv", index=False)
order_products_demo.to_csv("recommender/order_products__prior_demo.csv", index=False)
orders_demo.to_csv("recommender/orders_demo.csv", index=False)

print("Demo dosyalar başarıyla oluşturuldu.")
