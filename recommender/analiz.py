import pandas as pd

try:
    orders = pd.read_csv("orders.csv")
    order_products = pd.read_csv("order_products__train.csv")
    products = pd.read_csv("products.csv")

    merged = pd.merge(order_products, products, on='product_id')

    print("En popüler ürünler:")
    print(merged['product_name'].value_counts().head(10))

except FileNotFoundError as e:
    print("Dosya bulunamadı:", e)
except Exception as e:
    print("Bir hata oluştu:", e)
