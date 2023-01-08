# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 11:39:26 2022

@author: nicol
"""

# Import relevant libraries
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


#Load Data File
absolute_path = '/Users/chandlerhall/Desktop/Github/' # Change to your path
data_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/all_data.csv'
df = pd.read_csv(data_path)



## Setting the data, deleting negative values and outliers
# df = pd.read_csv(os.path.join(my_path, fname1))

df = df[(df['pts_prediction_mod1'] >= 0) & (df['pts_prediction_mod1'] < 2)]
df = df[(df['pts_prediction_mod2'] >= 0) & (df['pts_prediction_mod2'] < 2)]
df = df[(df['pts_prediction_mod3'] >= 0) & (df['pts_prediction_mod3'] < 2)]
df = df[(df['pts_prediction_mod4'] >= 0) & (df['pts_prediction_mod4'] < 2)]

df3 = df

df['Model 1 Error: Points'] = df['pts_prediction_mod1'] - df['pts_per_min']

### Static graphs
## Static Graph 1
## We are only analyzing 2022 predictions

df2 = df[df['season']==2022]

models = ['pts_prediction_mod1', 
          'pts_prediction_mod2', 
          'pts_prediction_mod3',
          'pts_prediction_mod4']

new_cols = ['player', 'pts_per_min'] + models
df2 = df2[new_cols]

## Melting the df so we can see the models and their statistics as variables
df2_melt = df2.melt(id_vars=['player', 'pts_per_min'],
                    value_vars=models,
                    var_name='pred_models',
                    value_name='pts_predic_per_model'
                    )

new_names = ['Model 1', 'Model 2', 'Model 3', 'Model 4']
new_names = {old_name:new_name for (old_name, new_name) in zip(models, new_names)}
    
df2_melt['pred_models'] = df2_melt['pred_models'].replace(new_names)

## Plot
# https://stackoverflow.com/questions/29813694/how-to-add-a-title-to-seaborn-facet-plot
# https://seaborn.pydata.org/tutorial/axis_grids.html
# https://stackoverflow.com/questions/48145924/different-colors-for-points-and-line-in-seaborn-regplot
g = sns.FacetGrid(df2_melt,
                  col='pred_models',
                  )
g \
    .map(sns.regplot, 'pts_per_min', 'pts_predic_per_model',
      scatter_kws={"color": "cadetblue", 'alpha':0.3}, line_kws={"color": "red"}) \
    .set(ylabel='Predicted Points per Min',
         xlabel='Points per Min') \
    .set_titles( col_template = '{col_name}')

g.fig.subplots_adjust(top=0.8) # adjust the Figure in rp
g.fig.suptitle('Prediction vs Performance for 2022 average points')
g.savefig('PNGs_and_Screenshots/static_plot1')
plt.show()
plt.close()

### Static graph 2

## Creating a new dataset with the mean values
errors_list = df.columns.tolist()[-12:]
errors_value_list = [df[error].mean() for error in errors_list]

models_list = ['Model 1', 'Model 2', 'Model 3', 'Model 4']
mod_list = ['mod1', 'mod2', 'mod3', 'mod4']
models_list_new = models_list[1:3]
mod_list_new = mod_list[1:3]

for (model, mod) in zip(models_list_new, mod_list_new):
    df[f'{model} Error: Points'] = df[f'pts_prediction_{mod}'] - df['pts_per_min']

for (model, mod) in zip(models_list, mod_list):
    df[f'{model} Error: Assists'] = df[f'assists_prediction_{mod}'] - df['assists_per_min']
    df[f'{model} Error: Rebounds'] = df[f'reb_prediction_{mod}'] - df['reb_per_min']

for mod in mod_list:   
    df3['Points'] = df3[f'pts_prediction_{mod}'] - df3['pts_per_min']
    df3['Assists'] = df3[f'assists_prediction_{mod}'] - df3['assists_per_min']
    df3['Rebounds'] = df3[f'reb_prediction_{mod}'] - df3['reb_per_min']

models_list4 = models_list + models_list + models_list 

errors_list1 = ['Points per Min', 'Points per Min', 'Points per Min', 'Points per Min', 
                'Assists per Min', 'Assists per Min', 'Assists per Min', 'Assists per Min', 
                'Rebounds per Min', 'Rebounds per Min', 'Rebounds per Min', 'Rebounds per Min']
errors_value_list1 = [df3[error].mean() for error in errors_list]

df4 = pd.DataFrame(list(zip(models_list4, errors_list1, errors_value_list1)),
                   columns=['Model', 'Error', 'Value'])

## Plot
# https://matplotlib.org/stable/gallery/color/named_colors.html
# https://wckdouglas.github.io/2016/12/seaborn_annoying_title
ax = sns \
    .scatterplot(data=df4, 
                  x='Value', 
                  y='Error',
                  hue='Model',
                  legend=True) \
    .set(title="Errors for each Model's Predictions",
         xlabel='Errors',
         ylabel='Statistics')
plt.axvline(x=0, color='Red', lw=1).set_linestyle("--")
plt.xlim(-0.7, 0.7)
plt.savefig('PNGs_and_Screenshots/static_plot2')
plt.show()
plt.close()



