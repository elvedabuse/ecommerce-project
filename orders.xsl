<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" indent="yes"/>

  <xsl:template match="/">
    <html>
      <head>
        <title>Orders - elvedabuse</title>
        <style>
          body { font-family: Arial; background-color: #f9f9f9; padding: 20px; }
          h1 { color: #333; }
          .order { border: 1px solid #ccc; margin-bottom: 20px; padding: 15px; background-color: #fff; border-radius: 8px; }
          .item-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
          .item-table th, .item-table td { border: 1px solid #ccc; padding: 8px; text-align: left; }
          .item-table th { background-color: #eee; }
        </style>
      </head>
      <body>
        <h1>User Orders</h1>

        <xsl:for-each select="Orders/item">
          <div class="order">
            <p><strong>Username:</strong> <xsl:value-of select="username" /></p>
            <p><strong>Timestamp:</strong> <xsl:value-of select="timestamp" /></p>
            <p><strong>Total Price:</strong> <xsl:value-of select="total_price" /> ₺</p>

            <table class="item-table">
              <tr>
                <th>Product ID</th>
                <th>Name</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total</th>
              </tr>

              <xsl:for-each select="items/item">
                <tr>
                  <td><xsl:value-of select="product_id" /></td>
                  <td><xsl:value-of select="name" /></td>
                  <td><xsl:value-of select="quantity" /></td>
                  <td><xsl:value-of select="price" /> ₺</td>
                  <td><xsl:value-of select="item_total" /> ₺</td>
                </tr>
              </xsl:for-each>

            </table>
          </div>
        </xsl:for-each>

      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
