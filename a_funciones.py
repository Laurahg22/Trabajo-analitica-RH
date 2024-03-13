####### prueba
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer ### para imputación
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import cross_val_predict, cross_val_score, cross_validate
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder 

####Este archivo contienen funciones utiles a utilizar en diferentes momentos del proyecto

###########Esta función permite ejecutar un archivo  con extensión .sql que contenga varias consultas

def ejecutar_sql (nombre_archivo, cur):
  sql_file=open(nombre_archivo)
  sql_as_string=sql_file.read()
  sql_file.close
  cur.executescript(sql_as_string)
  
  
def imp_datos (df, variables):
    for variable in variables:
        # Calcula la moda de la variable
        moda = df[variable].mode()[0]  # Selecciona el primer valor de la moda en caso de que haya múltiples modas
        # Imputa los valores nulos con la moda
        df[variable].fillna(moda, inplace=True)
        # Imprime información sobre los valores nulos imputados
        nulos_imputados = df[variable].isnull().sum()
    # Devuelve el DataFrame modificado
    return df


def sel_variables(modelos,X,y,threshold):
    
    var_names_ac=np.array([])
    for modelo in modelos:
        #modelo=modelos[i]
        modelo.fit(X,y)
        sel = SelectFromModel(modelo, prefit=True,threshold=threshold)
        var_names= modelo.feature_names_in_[sel.get_support()]
        var_names_ac=np.append(var_names_ac, var_names)
        var_names_ac=np.unique(var_names_ac)
    
    return var_names_ac


def medir_modelos(modelos,scoring,X,y,cv):

    metric_modelos=pd.DataFrame()
    for modelo in modelos:
        scores=cross_val_score(modelo,X,y, scoring=scoring, cv=cv )
        pdscores=pd.DataFrame(scores)
        metric_modelos=pd.concat([metric_modelos,pdscores],axis=1)
    
    metric_modelos.columns=["reg_lineal","decision_tree","random_forest","gradient_boosting"]
    return metric_modelos



def preparar_datos(df):

    list_cat = joblib.load("/content/drive/MyDrive/trabajo/Trabajo-analitica-RH/salidas/var_cat.pkl")
    list_dummies = joblib.load("/content/drive/MyDrive/trabajo/Trabajo-analitica-RH/salidas/list_dummies.pkl")
    var_names = joblib.load("/content/drive/MyDrive/trabajo/Trabajo-analitica-RH/salidas/var_names.pkl")
    scaler = joblib.load("/content/drive/MyDrive/trabajo/Trabajo-analitica-RH/salidas/scaler.pkl")

    df = imp_datos(df, list_cat) 
    le = LabelEncoder()
    for column in list_cat:
        if len(df[column].unique()) == 2:
            df[column] = le.fit_transform(df[column])
    df = pd.get_dummies(df)
    df_dummies = pd.get_dummies(df, columns=list_dummies)
    df_dummies = df_dummies.loc[:, ~df_dummies.columns.isin(['EmployeeID'])]
    
    # Asegurar que las dimensiones de los datos coincidan
    X2 = scaler.transform(df_dummies)  # Aplicar la transformación del scaler
    X = pd.DataFrame(X2, columns=df_dummies.columns)
    X = X[var_names]  # Seleccionar las variables necesarias
    
    return X



def imputar_con_moda(df, variables):
    for variable in variables:
        # Calcula la moda de la variable
        moda = df[variable].mode()[0]  # Selecciona el primer valor de la moda en caso de que haya múltiples modas
        # Imputa los valores nulos con la moda
        df[variable].fillna(moda, inplace=True)
        # Imprime información sobre los valores nulos imputados
        nulos_imputados = df[variable].isnull().sum()
    # Devuelve el DataFrame modificado
    return df
