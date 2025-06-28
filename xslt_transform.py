from lxml import etree

# XML ve XSLT dosyalarını oku
dom = etree.parse("orders.xml")
xslt = etree.parse("orders.xsl")

# Dönüştür
transform = etree.XSLT(xslt)
newdom = transform(dom)

# HTML olarak kaydet
with open("orders.html", "wb") as f:
    f.write(etree.tostring(newdom, pretty_print=True, encoding='UTF-8'))

print("✅ orders.html dosyası oluşturuldu.")
