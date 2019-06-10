import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Select, CategoricalColorMapper, Slider, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row

data = pd.read_csv('gapminder_tidy.csv', index_col = 'Year')

# bikin ColumnDataSource
source = ColumnDataSource(data={
    'x'       : data.loc[1970].fertility,
    'y'       : data.loc[1970].life,
    'country'      : data.loc[1970].Country,
    'pop'      : (data.loc[1970].population / 20000000) + 2,
    'region'      : data.loc[1970].region,
})

# min dan max dari kolom fertility xmin, xmax
xmin, xmax = min(data.fertility), max(data.fertility)

# min dan max dari kolom life expectancy : ymin, ymax
ymin, ymax = min(data.life), max(data.life)

# membuat figure: plot
plot = figure(title='Gapminder Data for 1970', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))

# membuat cirle glyph 
plot.circle(x='x', y='y', fill_alpha=0.8, source=source)

# x-label
plot.xaxis.axis_label ='Fertility(Angka kesuburan )'

# y-label
plot.yaxis.axis_label = 'Life Expectancy(Harapan hidup)'

# nyuapin warna buat tiap region
regions_list = data.region.unique().tolist()


# membuat color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

# tambahkan color_mapper ke circle glyph
plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
            color=dict(field='region', transform=color_mapper), legend='region')

# lokasi legend di kanan atas
plot.legend.location = 'top_right'

# membuat fungsi callback: update_plot
def update_plot(attr, old, new):
    # membaca nilai slider dan 2 dropdowns: yr, x, y
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label x
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # buat data baru: new_data
    new_data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'country' : data.loc[yr].Country,
        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region,
    }
    # Assign new_data ke source.data
    source.data = new_data

    # Set range untuk setiap axis
    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

    # title plot
    plot.title.text = 'Gapminder data untuk tahun %d' % yr

# ngebuat slider
slider = Slider(start=1970, end=2010, step=1, value=1970, title='Year')

# manggil fungsi callback
slider.on_change('value', update_plot)

# bikin dropdown Select buat data x: x_select
x_select = Select(
    options=['fertility (kesuburan', 'life (angka hidup)', 'child_mortality (kematian anak)', 'gdp'],
    value='fertility',
    title='x-axis data'
)

# panggil fungsi callback : updata_plot untul x_select
x_select.on_change('value', update_plot)

# bikin dropdown Select buat data y : y_select
y_select = Select(
    options=['fertility (kesuburan)', 'life (angka hidup)', 'child_mortality (kematian anak)', 'gdp'],
    value='life',
    title='y-axis data'
)

# panggil fungsi callback : updata_plot untuk y_select
y_select. on_change('value', update_plot)

# bikin HoverTool: hover
hover = HoverTool(tooltips=[('Country', '@country')])

# tambahin HoverTool ke plot
plot.add_tools(hover)

# bikin layout 
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)
show(layout)
