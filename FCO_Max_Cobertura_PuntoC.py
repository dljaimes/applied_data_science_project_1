# -*- coding: utf-8 -*-
"""
Petroco - MIIA4102
Profesor: Andrés L. Medaglia (amedagli@uniandes.edu.co)
Instructor: Alfaima Solano
Asistente: Johan Camacho
Created:  Aug. 31, 2020
Modified: Sep. 10, 2020
@author: amedagli
"""
#%% Importar las funciones de PuLP y otros

import pulp as lp
from math import radians, sin, cos, acos #Para calcular distancias
from datetime import datetime            #Para tiempo de ejecución
import pandas as pd
import seaborn as sns

#%% Crear datos del modelo

#------------------
#    Conjuntos 
#------------------

#Conjunto de centros
Centros = ["Andes",
            "Medellín",
            "Dabeiba",
            "Salgar",
            "San Pablo de Borbur",
            "Labranzagrande",
            "Miraflores",
            "Moniquirá",
            "Manizales",
            "Anserma",
            "Pensilvania",
            "Riosucio",
            "Aguadas",
            "Morales",
            "El Tambo",
            "Bolívar",
            "Aguachica",
            "San Diego",
            "Caparrapí",
            "Viotá",
            "Sasaima",
            "Neiva",
            "Pitalito",
            "Gigante",
            "Santa Marta",
            "La Unión",
            "Pasto",
            "Samaniego",
            "Sardinata",
            "Ocaña",
            "Convención",
            "Génova",
            "Calarcá",
            "Quimbaya",
            "Pereira",
            "Santuario",
            "Belén de Umbria",
            "Rionegro",
            "Bucaramanga",
            "Barbosa",
            "Socorro",
            "Simacota",
            "Chaparral",
            "Dolores",
            "Ibagué",
            "Líbano",
            "Cartago",
            "Tulua",
            "Jamundí",
            "Sevilla",
            "Caicedonia",
            "Florencia",
            "Puerto Milán",
            "Nunchía",
            "Mesetas"
            ]

#Conjunto de depósitos
Depositos = ["Medellín",
            "La Dorada",
            "Aguadas",
            "Salamina",
            "Popayán",
            "Valledupar",
            "Bogotá",
            "Santana",
            "Neiva",
            "Santa Marta",
            "Cúcuta",
            "Pasto",
            "Génova",
            "Calarcá",
            "Filandia",
            "Pereira",
            "Bucaramanga",
            "Barbosa",
            "Cali",
            ]

#Conjunto con todas las tuplas (depositos, centros)
Depositos_x_Centros = [(i,j) for i in Depositos for j in Centros]

#------------------
#    Parámetros 
#------------------

# Parámetros no indexados
costo = 300*1000/1000000  #$300/ton/km*factor de conversion (mil ton/millon $)
dist_max = 125            #Distancia máxima de un nivel adecuado de servicio
mejor_costo= 14823.3

dataDepositos= {# Depósito: lat, long, capacidad, costo fijo
        "Medellín": [6.26868, -75.59639, 104, 717.10],
        "La Dorada": [5.53144, -74.72005, 38, 402.27],
        "Aguadas": [5.57937, -75.45557, 38, 402.27],
        "Salamina": [5.34395, -75.40658, 35, 387.96],
        "Popayán": [2.4427, -76.57841, 23, 330.71],
        "Valledupar": [10.46477, -73.25915, 11, 273.47],
        "Bogotá": [4.6483, -74.10781, 10, 268.70],
        "Santana": [3.58706, -74.70524, 42, 421.35],
        "Neiva": [3.03602, -75.29684, 48, 449.97],
        "Santa Marta": [11.23153, -74.1824, 4, 240.08],
        "Cúcuta": [8.07777, -72.4772, 8, 259.16],
        "Pasto": [1.05204, -77.20717, 25, 340.25],
        "Génova": [4.192, -75.74795, 7, 254.39],
        "Calarcá": [4.45392, -75.68058, 5, 244.85],
        "Filandia": [4.66388, -75.65585, 9, 263.93],
        "Pereira": [4.78502, -75.65506, 5, 244.85],
        "Bucaramanga": [7.16502, -73.10824, 18, 306.86],
        "Barbosa": [5.95458, -73.62693, 12, 278.24],
        "Cali": [3.39506, -76.52566, 29, 359.34]
        }


dataCentros = {#Centro: lat, long, producción
        "Andes": [5.62412, -75.95589, 35.37],
        "Medellín": [6.26868, -75.59639, 10.63],
        "Dabeiba": [6.95267, -76.29085, 27.28],
        "Salgar": [5.96643, -75.97188, 24.05],
        "San Pablo de Borbur": [5.67784, -74.10383, 1.59],
        "Labranzagrande": [5.53, -72.59873, 1.20],
        "Miraflores": [5.15175, -73.17282, 1.11],
        "Moniquirá": [5.86963, -73.54944, 1.28],
        "Manizales": [5.0741, -75.50288, 24.76],
        "Anserma": [5.20035, -75.75022, 8.23],
        "Pensilvania": [5.40334, -75.1766, 6.60],
        "Riosucio": [5.45036, -75.73531, 6.63],
        "Aguadas": [5.57937, -75.45557, 6.74],
        "Morales": [2.84901, -76.74932, 14.19],
        "El Tambo": [2.4527, -76.81132, 13.25],
        "Bolívar": [1.89843, -76.97234, 11.89],
        "Aguachica": [8.30592, -73.61166, 3.60],
        "San Diego": [10.33573, -73.18049, 2.71],
        "Caparrapí": [5.37312, -74.51297, 1.45],
        "Viotá": [4.43705, -74.48354, 1.75],
        "Sasaima": [4.94796, -74.41729, 2.29],
        "Neiva": [3.03602, -75.29684, 22.25],
        "Pitalito": [1.7774, -76.13852, 21.85],
        "Gigante": [2.39452, -75.52775, 21.92],
        "Santa Marta": [11.23153, -74.1824, 3.80],
        "La Unión": [1.60903, -77.14714, 7.59],
        "Pasto": [1.05204, -77.20717, 8.12],
        "Samaniego": [1.3894, -77.72329, 5.70],
        "Sardinata": [8.25885, -72.79639, 2.52],
        "Ocaña": [8.22019, -73.39012, 2.60],
        "Convención": [8.83257, -73.18585, 2.34],
        "Génova": [4.192, -75.74795, 4.99],
        "Calarcá": [4.45392, -75.68058, 6.09],
        "Quimbaya": [4.61334, -75.78586, 5.49],
        "Pereira": [4.78502, -75.65506, 8.89],
        "Santuario": [5.03229, -75.97494, 7.36],
        "Belén de Umbria": [5.19016, -75.86725, 9.06],
        "Rionegro": [7.54004, -73.42111, 1.87],
        "Bucaramanga": [7.16502, -73.10824, 1.79],
        "Barbosa": [5.95458, -73.62693, 8.56],
        "Socorro": [6.46604, -73.24775, 7.92],
        "Simacota": [6.67635, -73.62452, 6.50],
        "Chaparral": [3.75307, -75.59347, 8.73],
        "Dolores": [3.6221, -74.76516, 11.86],
        "Ibagué": [4.47824, -75.2436, 1.43],
        "Líbano": [4.87582, -75.04174, 1.19],
        "Cartago": [4.71034, -75.91931, 6.27],
        "Tulua": [4.03985, -76.06656, 5.94],
        "Jamundí": [3.2012, -76.62458, 3.54],
        "Sevilla": [4.15709, -75.88795, 2.84],
        "Caicedonia": [4.3072, -75.84114, 3.11],
        "Florencia": [1.61887, -75.60384, 0.37],
        "Puerto Milán": [1.33546, -75.51081, 0.33],
        "Nunchía": [5.53209, -72.07238, 0.38],
        "Mesetas": [3.1057, -74.1243, 0.43]
        }

# Partir diccionarios por facilidad de modelamiento
# Parámetros indexados en depósitos
(lat_d, lon_d, capacidad, costo_fijo) = lp.splitDict(dataDepositos)
# Parámetros indexados en centros
(lat_c, lon_c, produccion) = lp.splitDict(dataCentros)

# Parámetros con los dos índices 
#{(Depósitos, centros): distancia}
'''
i.e.
distancia = ('Medellín', 'Andes'):  81.96,
            ('La Dorada', 'Andes'): 137.16,
            ('Aguadas',  'Andes'):  55.59,
             ...
'''
# Calcular la distancia entre depósitos y centros
distancias = {}
for i in Depositos: 
    lat_x, lon_x = radians(lat_d[i]), radians(lon_d[i])
    for j in Centros:
        lat_y, lon_y = radians(lat_c[j]), radians(lon_c[j])
        distancias[i,j] = 6371 * acos(sin(lat_x)*sin(lat_y) \
                                 + cos(lat_x)*cos(lat_y)*cos(lon_x - lon_y))
# -----

#%% Definir modelo de minimización de costos

# Iniciando temporizador
start = datetime.now()

# Creación de listas para guardar los resultados:

costos_lista = []
cobertura_lista = []
depositos_abiertos = []


#Iteraciones
#for ii in range(0,60,5):
 #   print ("Porcentaje:", ii/1000)
#-------------------------------------
# Creación del objeto problema en PuLP
#-------------------------------------
problema = lp.LpProblem("FCO",lp.LpMaximize)

#-----------------------------
#    Variables de Decisión
#-----------------------------
activar= lp.LpVariable.dicts("Activar",
                             Depositos,
                             lowBound=0,
                             upBound=1,
                             cat=lp.LpBinary)

atender= lp.LpVariable.dicts("Atender",
                             Depositos_x_Centros,
                             lowBound=0,
                             cat=lp.LpContinuous)
#-----------------------------
#    Función objetivo
#-----------------------------
#Maximizar cobertura
# 
problema+= lp.lpSum([atender[i,j] for i, j in Depositos_x_Centros\
                     if distancias[i,j]<=dist_max]),\
                    "Satisfacción total"

#-----------------------------
#    Restricciones
#-----------------------------

# 1. Se deben atender todos los centros de acopio
for j in Centros:
    print(lp.lpSum([atender[i,j] for i in Depositos]) == produccion[j]) ,"Atender el centro" + j

# 2. Capacidad limitada en los depósitos.
        
for i in Depositos:
    problema+= lp.lpSum([atender[i,j] for j in Centros])\
        <=capacidad[i]*activar[i], \
            "respetar la capacidad de " + i

# 3. Restricción sobre los costos o cobertura 

  
#problema+= lp.lpSum([costo_fijo[i]*activar[i] for i in Depositos]) + costo*lp.lpSum([distancias[i,j]*produccion[j]*atender[i,j] for i,j in Depositos_x_Centros]) <= (1+ii/1000)*mejor_costo,'No sobrepasar el costo minimo'


#-----------------------------
#    Invocar el optimizador
#-----------------------------
solver=lp.PULP_CBC_CMD(msg=0)
problema.solve(solver)

#-----------------------------
#    Guardar los resultados
#-----------------------------
costo_obj = round(sum([costo_fijo[i]*activar[i].value() for i in Depositos]) +
                  costo*sum([distancias[i,j]*atender[i,j].value() \
                             for i,j in Depositos_x_Centros]),1)

#mejor_costo = costo_obj   # Se guarda la mejor solución
    
cobertura_obj =round(sum([atender[i,j].value() \
                          for i,j in Depositos_x_Centros \
                              if distancias[i,j]<= dist_max])\
                     /sum(produccion[j] for j in Centros),3)

    
distancias

atender.values()




#-----------------------------
#    Imprimir resultados
#-----------------------------
print("======================================")
print("Federación de cafeteros de origen")
print("======================================")
print("Costo:\t", costo_obj)
print("Cobertura:\t", str(cobertura_obj*100)+"%")
print("Depósitos abiertos:\t", sum(activar[i].value() for i in Depositos))
print("======================================")
print("Tiempo de solucion:",datetime.now()-start)

costos_lista.append(costo_obj)
cobertura_lista.append(cobertura_obj*100)
depositos_abiertos.append(sum(activar[i].value() for i in Depositos))



'''GENERAR MATRIZ (DF) CON RELACIÓN DE CAC y DEPOSITOS POR CANTIDADES '''

variables_ = []
valores_ = []

for variable in problema.variables():
    variables_.append(variable.name)
    valores_.append(variable.varValue)

df_variables = pd.DataFrame({'variables_':variables_, 'valores_':valores_})

df_atender = df_variables.iloc[19:]
df_atender.insert(0, 'Deposito',  df_atender['variables_'].apply(lambda x: x.split(',_')[0] ))
df_atender.insert(1, 'CAC',  df_atender['variables_'].apply(lambda x: x.split(',_')[1] ))
df_atender['Deposito'] = df_atender['Deposito'].apply(lambda x: x.strip('Atender_('))
df_atender['CAC'] = df_atender['CAC'].apply(lambda x: x.strip(')'))
df_atender.drop('variables_', axis=1, inplace=True)
df_atender = pd.pivot_table(data=df_atender,columns='CAC', index='Deposito', values='valores_')
df_atender_mayor = df_atender>0
df_atender_mayor.sum()

df_atender


''' GENERAR MATRIZ DE DISTANCIAS '''

df_distancias = pd.DataFrame.from_dict(distancias, orient= 'index')
df_distancias.columns= ['Distancia']
df_distancias.reset_index(inplace=True)
df_distancias.columns = ['ind', 'Distancia']

df_distancias['CAC'] =  df_distancias['ind'].apply(lambda x: str(x).split(',')[1])
df_distancias['Deposito'] = df_distancias['ind'].apply(lambda x: str(x).split(',')[0])
df_distancias['CAC'] = df_distancias['CAC'].apply(lambda x: x.strip(')'))
df_distancias['Deposito'] = df_distancias['Deposito'].apply(lambda x: x.strip('('))
df_distancias.drop('ind', axis=1, inplace=True)
df_distancias = pd.pivot_table(df_distancias, columns='CAC', index='Deposito', values='Distancia')
df_distancias_menor_125 =  df_distancias<=125
df_distancias_menor_125







df_variables.to_excel(r'C:\Users\57310\Documents\Semestre I - MIIA\Modelaje y mejora de procesos\FCO/Base.xlsx')
    
    
    
    
df = pd.DataFrame({'costos':costos_lista, 'cobertura':cobertura_lista, 'depósitos abiertos':depositos_abiertos })

df['depósitos abiertos'] = df['depósitos abiertos'].astype('str')
sns.scatterplot(data=df, y='costos', x = 'cobertura', hue='depósitos abiertos', size='costos')


df_2 =  df.pct_change()
 
df = pd.concat([df, df_2], axis=1)

df

'''
for i,j in Depositos_x_Centros: 
    if atender[i,j].value()>0.1:
        print(i,"\t",j)
'''


#%% Gráficar 
#-----------------------------
#    Realizar gráficas
#-----------------------------
import matplotlib.pyplot as plt

utilizado = []
nombres = []
for i in Depositos:
    if activar[i].value() > 0.5: 
        nombres.append(i)
for i in nombres:
    utilizado.append(sum([produccion[j]*atender[i,j].value() for j in Centros]))

zipped_lists = zip(utilizado, nombres)
sorted_zipped_lists = sorted(zipped_lists)
sorted_nombres = [element for _, element in sorted_zipped_lists]
sorted_utilizado = [u for u,_ in sorted_zipped_lists]

plt.barh(sorted_nombres,sorted_utilizado, alpha = .5)
plt.xlim(0,105)
plt.title('Producción recibida en cada depósito abierto')
plt.show()

#%% End of file
