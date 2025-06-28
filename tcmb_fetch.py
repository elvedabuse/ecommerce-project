import requests
from lxml import etree

# TCMB'nin günlük döviz kuru XML dosyası
url = "https://www.tcmb.gov.tr/kurlar/today.xml"
response = requests.get(url)

# XML içeriğini parse et
tree = etree.fromstring(response.content)

# XPath ile USD satış kuru çek
usd_rate = tree.xpath("//Currency[@Kod='USD']/BanknoteSelling/text()")[0]
eur_rate = tree.xpath("//Currency[@Kod='EUR']/BanknoteSelling/text()")[0]

print(f"USD Satış Kuru: {usd_rate}")
print(f"EUR Satış Kuru: {eur_rate}")
