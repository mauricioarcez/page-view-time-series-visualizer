import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
nulos = df.isnull()
df_nulos = df[nulos.any(axis=1)] #the data does not contain null values
low = 2.5
high = 97.5

low_quantile = df['value'].quantile(low/100)
high_quantile = df['value'].quantile(high/100)
df = df[(df['value'] > low_quantile) & (df['value'] < high_quantile)]
filtrado = df[(df['value'] >= low_quantile) & (df['value'] <= high_quantile)]

def draw_line_plot():
    # Draw line plot
  fig, ax = plt.subplots(figsize=(20,10))
  ax.plot(filtrado.index, filtrado['value'], color='red')
  ax.set_xlabel('Date')
  ax.set_ylabel('Page Views')
  ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
  fecha = filtrado.copy()
  fecha['año'] = fecha.index.year
  fecha['mes'] = fecha.index.month
  pivot = fecha.pivot_table(index='año',columns='mes',values='value', aggfunc='mean', fill_value=0)
  meses={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
  pivot.rename(columns=meses, inplace=True)
  
    # Draw bar plot
  fig, ax = plt.subplots(figsize=(10,8))
  pivot.plot(kind= 'bar', ax=ax)

  ax.legend(title='Months', labels=pivot.columns)
  ax.set_ylabel('Average Page Views')
  ax.set_xlabel('Years')

    # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]
  box_clean = df_box[(df_box['value'] >= low_quantile) & (df_box['value'] <= high_quantile)]

  # Draw box plots (using Seaborn)
  fig, ax = plt.subplots(1,2, figsize=(18,6))

  sns.boxplot(x=box_clean['year'], y=box_clean['value'], hue= 'year',palette='tab10',legend=False,flierprops=dict(markerfacecolor='black', marker='D', markersize=2), data=box_clean, ax=ax[0])
  ax[0].set_title('Year-wise Box Plot (Trend)')
  ax[0].set_xlabel('Year')
  ax[0].set_ylabel('Page Views')


  sns.boxplot(x=box_clean['month'], y=box_clean['value'], hue='month',flierprops=dict(markerfacecolor='black', marker='D', markersize=2), data=box_clean,order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec' ], ax=ax[1])
  ax[1].set_title('Month-wise Box Plot (Seasonality)')
  ax[1].set_xlabel('Month')
  ax[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
