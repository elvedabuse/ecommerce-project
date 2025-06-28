from lxml import etree

# XML dosyasını yükle
tree = etree.parse('orders.xml')

# Tüm siparişlerin timestamp değerlerini alalım
timestamps = tree.xpath('//item/timestamp/text()')
print("Tüm timestamps:", timestamps)

# Kullanıcı adı elvedabuse olan siparişlerdeki ürün isimlerini alalım
product_names = tree.xpath('//item[username="elvedabuse"]/items/item/name/text()')
print("Ürün isimleri (elvedabuse):", product_names)
