from lxml import etree

# XML dosyasını oku
xml_doc = etree.parse('orders.xml')

# XSD şemasını oku
xmlschema_doc = etree.parse('orders.xsd')
xmlschema = etree.XMLSchema(xmlschema_doc)

# Doğrulama yap
if xmlschema.validate(xml_doc):
    print("XML dosyası XSD'ye uygundur. Doğrulama başarılı.")
else:
    print("XML dosyası XSD'ye uygun değil. Hatalar:")
    for error in xmlschema.error_log:
        print(error.message)
