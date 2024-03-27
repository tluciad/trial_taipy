from taipy.gui import Gui, Html
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
import gdown
import re

url = 'https://drive.google.com/uc?id=' + '1je20eESs-kdNufav4yU4FKoEJxhgTUoc'
output = 'Electronics.csv'
gdown.download(url, output, quiet=False)

Electronics = pd.read_csv(output)
df_sample = Electronics.head(15)

def extraer_marca(texto):
    patron = r'^(\w+)'
    coincidencia = re.match(patron, texto)
    if coincidencia:
        return coincidencia.group(1)
    else:
        return None


Electronics['Brand'] = Electronics['name'].apply(extraer_marca)

def classify_electronics(product_name):
    # Convert product name to lowercase for case-insensitive matching
    product_name = product_name.lower()
    if 'smartphone' in product_name or 'phone' in product_name or 'realme' in product_name or 'galaxy' in product_name or 'vivo' in product_name or 'oppo' in product_name or 'nokia' in product_name or 'OnePlus' in product_name:
        return 'Smartphone'
    elif 'charger' in product_name or 'adapter' in product_name or 'Power Bank' in product_name or 'Charging' in product_name:
        return 'Charger or Adapter'
    elif 'earphones' in product_name or 'earbuds' in product_name or 'headphones' in product_name or 'Airpods' in product_name:
        return 'Earphones'
    elif 'smart watch' in product_name or 'watch' in product_name:
        return 'Smart Watch'
    elif 'computer' in product_name or 'mouse' in product_name or 'drive' in product_name or 'laptop' in product_name or 'Pen Drive' in product_name:
        return 'Computer Accesories'
    elif 'printer' in product_name or 'laserjet' in product_name or 'inkjet' in product_name:
        return 'Printer'
    elif 'pen' in product_name or 'Gel Pens' in product_name:
        return 'Gel Pens'
    elif 'E-Book' in product_name or 'tablet' in product_name:
        return 'E-Book or tablet'
    elif 'tv' in product_name or 'smart tv' in product_name:
        return 'TV or smartTV'
    elif 'batteries' in product_name or 'battery' in product_name:
        return 'Batteries'
    elif 'camera' in product_name or 'camera' in product_name or 'Instax' in product_name or 'Webcam' in product_name or 'Selfie Sticks' in product_name:
        return 'Camera and suplies'
    else:
        return 'Other Electronics'


Electronics['category'] = Electronics['name'].apply(classify_electronics)

fig_count = px.histogram(Electronics, x="category", color='category',
                        histfunc='count', width=1200, height=500, title='Category Distribution')

top_brands = Electronics['Brand'].value_counts().head(25).index
top_brands_df = Electronics[Electronics['Brand'].isin(top_brands)]
fig_Hist = px.histogram(top_brands_df, x="Brand", color='Brand',
                        histfunc='count', width=600, height=400, title='Top 5 Brand Distribution')

fig_Pie = px.pie(Electronics, names='category', title='Category Distribution')

with tgb.Page() as page:
    tgb.text("Amazon Electronics", class_name="h1")

    with tgb.layout("1 1 1"):
        with tgb.part():
            tgb.text("Total cost", class_name="h2")
            tgb.text(
                "{int(Electronics['actual_price'].sum())}", class_name="h3")

    tgb.chart(figure="{fig_count}")
    tgb.table("{df_sample}")

    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_Hist}")
        tgb.chart(figure="{fig_Pie}")

if __name__ == "__main__":
    gui = Gui(page)
    gui.run(title="Electronics in Amazon", port=5003)


