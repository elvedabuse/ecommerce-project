import json
import dicttoxml
from xml.dom.minidom import parseString

# JSON dosyasını oku
with open('orders.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# JSON verisini XML'e dönüştür
xml_data = dicttoxml.dicttoxml(data, custom_root='Orders', attr_type=False)

# XML stringini daha okunabilir hale getir
xml_pretty = parseString(xml_data).toprettyxml(indent="  ")

# XML dosyasına yaz
with open('orders_pretty.xml', 'w', encoding='utf-8') as xml_file:
    xml_file.write(xml_pretty)

print("JSON dosyası başarıyla biçimlendirilmiş XML formatına dönüştürüldü!")
