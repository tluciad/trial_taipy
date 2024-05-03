from taipy.gui import Gui, Html
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
import gdown
from taipy.gui import Markdown


url = 'https://drive.google.com/uc?id=' + '1aJJXEYaGJmO2FZdRptnCbmIBUBaz5mg2'
output = 'supermarket_sales.csv'
gdown.download(url, output, quiet=False)
Supermk = pd.read_csv(output)

    
Supermk = Supermk.rename(columns={'Customer type': 'CustomerType', 'Product line': 'ProductLine',
                         'gross income': 'grossIncome', 'Tax 5%': 'Tax5%', 'Unit price': 'UnitPrice', 'gross margin percentage':'grossMarginPercentage'})

Supermk = Supermk.drop(columns=['Invoice ID', 'Branch', 'grossMarginPercentage'], axis=1)

product_frequency = Supermk['ProductLine'].value_counts().reset_index()
product_frequency.columns = ['ProductLine', 'Frequency']
product_frequency=pd.DataFrame(product_frequency)

fig_table = go.Figure(data=[go.Table(
    header=dict(values=list(product_frequency.columns),
                font=dict(size=20, family='Arial', color='rgb(0,0,0)'),
                line_color='rgb(90, 134, 000)',
                fill_color='rgb(179, 207, 150)',
                align="center"),                
    cells=dict(values=[product_frequency.ProductLine, product_frequency.Frequency],
               font=dict(size=14, family='Arial', color='rgb(0,0,0)'),
                line_color='rgb(90, 134, 000)',
                fill_color='rgb(179, 207, 254)',
                align="center")),
]) 
fig_table.update_layout(title="Tabla de frecuencia por linea de producto", autosize=False, margin=dict(l=150, r=100, b=50, t=90, pad=2))

Supermk['Date'] = pd.to_datetime(Supermk['Date'], format='%m/%d/%Y')
Supermk['Month'] = Supermk['Date'].dt.month
monthly_totals = Supermk.groupby('Month')['Total'].sum().reset_index()

# Plot line graph using Plotly Express
fig_lin1 = px.line(monthly_totals, x='Month', y='Total', title='Grafico de linea del total Ventas por mes')
fig_lin1.update_xaxes(title='Month')
fig_lin1.update_yaxes(title='Total')
fig_lin1.update_layout(autosize=False, margin=dict(l=100, r=100, b=100, t=100, pad=4))

Supermk['Week'] = Supermk['Date'].dt.isocalendar().week
weekly_totals = Supermk.groupby('Week')['Total'].sum().reset_index()

# Plot line graph using Plotly Express
fig_lin2 = px.line(weekly_totals, x='Week', y='Total', title='Grafico de linea con Ventas totales por semana')
fig_lin2.update_xaxes(title='Semana')
fig_lin2.update_yaxes(title='Total')
fig_lin2.update_layout(autosize=False, margin=dict(l=100, r=100, b=100, t=100, pad=4))
fig_bar1 = px.bar(Supermk, x="City", y="grossIncome", color="Gender", title="Gráfico de barras apiladas de ingresos brutos")
fig_bar1.update_layout(autosize=False, margin=dict(l=200, r=80, b=100, t=100, pad=4))

fig_Hist = px.histogram(Supermk, y="ProductLine", orientation='h', title='Histograma Linea de productos',
                        histfunc='count', template='gridon')
fig_Hist.update_layout(autosize=False, margin=dict(
    l=250, r=80, b=80, t=80, pad=4))

fig_scatter = px.scatter(Supermk, x="UnitPrice", y="Rating", color="ProductLine", marginal_x="histogram")
fig_scatter.update_layout(title="Gráfico de Dispersión: Precio Unitario vs. Calificación", autosize=False, margin=dict(l=200, r=80, b=100, t=100, pad=4))

fig_box = px.box(Supermk, x="Month", y="Total", points="all", title='Boxplot totales por mes')
fig_box.update_layout(autosize=False, margin=dict(l=90, r=80, b=80, t=80, pad=4))
fig_heat = px.density_heatmap(Supermk, x="ProductLine", y="UnitPrice", text_auto=True, title='Mapa de Calor Linea de producto vs Precio unitario')
fig_heat.update_layout(autosize=False, margin=dict(l=90, r=80, b=80, t=80, pad=4))

fig_Pie = px.pie(Supermk, names='ProductLine', title='Grafico pastel por linea de productos',
                 template='seaborn')
fig_Pie.update_layout(autosize=False, margin=dict(l=80, r=80, b=80, t=80, pad=4))
fig_funnel = px.funnel(Supermk, y='ProductLine', x='Rating',
                       template='gridon', color= 'ProductLine')
fig_funnel.update_layout(autosize=False, margin=dict(l=250, r=80, b=100, t=100, pad=4),)
fig_Pie2 = px.pie(Supermk, names='Payment', title='Grafico dona con las formas de pago',  hole=.4, template='seaborn')
fig_Pie2.update_layout(autosize=False, margin=dict(l=80, r=80, b=80, t=80, pad=4))


fig_ecdf = px.ecdf(Supermk, x="ProductLine", color="Gender", marginal="histogram")
fig_ecdf.update_layout(autosize=False, margin=dict(l=80, r=80, b=80, t=80, pad=4))
fig_area = px.area(Supermk, y="grossIncome", x="Gender", color="City")
fig_area.update_layout(autosize=False, margin=dict(l=80, r=80, b=80, t=80, pad=4))
fig_icicle = px.icicle(Supermk, path=[px.Constant("all"), 'Gender', 'City'],
                values='Total', color='Gender', title='Grafico de mosaico por genero y ciudad')
fig_icicle.update_layout(autosize=False, margin=dict(l=80, r=80, b=80, t=80, pad=4))


with tgb.Page() as root_page:
    tgb.navbar()
    tgb.text("Reporte de Ventas SuperMercado", class_name="h1")

with tgb.Page() as page_1:
    tgb.text("Visualización de datos masivos", class_name="h3")

    with tgb.layout("1 1 1"):
        with tgb.part():
            tgb.text("Total ventas", class_name="h3")
            tgb.text("{int(Supermk['Total'].sum())}", class_name="h6")
        with tgb.part():
            tgb.text("Promedio Rating", class_name="h3")
            tgb.text("{int(Supermk['Rating'].mean())}", class_name="h6")
        with tgb.part():
            tgb.text("Total productos vendidos", class_name="h4")
            tgb.text("{int(Supermk['Quantity'].sum())}", class_name="h6")

    tgb.table("{Supermk}", filter=True, page_size=30)
  

    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_Hist}")
        tgb.chart(figure="{fig_table}")

    tgb.text(" \n, \n")
    tgb.chart(figure="{fig_scatter}")


with tgb.Page() as page_2:
    tgb.text("Pagina 2", class_name="h3")

    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_box}")
        tgb.chart(figure="{fig_funnel}")
    
    tgb.text(" \n, \n")
    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_lin1}")
        tgb.chart(figure="{fig_Pie}")

with tgb.Page() as page_3:
    tgb.text("Pagina 3", class_name="h3")

    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_heat}")
        tgb.chart(figure="{fig_bar1}")

    tgb.text(" \n, \n")
    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_Pie2}")
        tgb.chart(figure="{fig_lin2}")

with tgb.Page() as page_4:
    tgb.text("Pagina 4", class_name="h3")

    with tgb.layout("1"):
        tgb.chart(figure="{fig_ecdf}")

    tgb.text(" \n, \n")
    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_area}")
        tgb.chart(figure="{fig_icicle}")

pages = {
    "/": root_page,
    "Inicio": page_1,
    "Productos": page_2,
    "Otros": page_3,
    "Generos": page_4
}

if __name__ == "__main__":
    
    gui = Gui(pages=pages)
    gui.run(title="Ventas supermercado", port=5018, dark_mode=False)


