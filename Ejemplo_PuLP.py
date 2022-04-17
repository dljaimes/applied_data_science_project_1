# -*- coding: utf-8 -*-
"""
Marketing mix - MIIA4102
Author: Andrés L. Medaglia (amedagli@uniandes.edu.co)
Instructor: Alfaima Solano
Asistente: Johan Camacho
Created:  Aug 30, 2019
Modified: Aug 25, 2020
@author: amedagli
"""

#%% Importa las funciones de PuLP 
import pulp

#%%-------------------------------------
# Creación del objeto problema en PuLP
#-------------------------------------

# Crea problema
problema = pulp.LpProblem("Marketing_mix", pulp.LpMaximize)

#%%-----------------------------
#    Variables de Decisión
#-----------------------------

# Creación de variables
# 0 <= x1 <= 12
x1 = pulp.LpVariable("TV", 0, 12)
# 0 <= x2 <= 12
x2 = pulp.LpVariable("FB", 0, 12)

#%%-----------------------------
#    Función objetivo
#-----------------------------

# La función objetivo se añade primero
problema += 3*x1 + 2*x2, "incremento ventas"

#%%-----------------------------
#    Restricciones
#-----------------------------

# No se puede exceder el presupuesto de 15
problema += x1 + x2 <= 15, "presupuesto"

# Debe invertirse 40% en FacebookAds
problema += 0.4*x1 - 0.6*x2 <= 0 ,"inversion FB"

#%%---------------------------
#    Imprimir formato LP
#-----------------------------

# Escribe el problema como un archivo LP 
#problema.writeLP("MarketingMix.lp")

#%%---------------------------
#    Invocar el optimizador
#----------------------------- 

# Resuelve con CBC
problema.solve()
#problema.solve(GUROBI())

#%%---------------------------
#    Imprimir resultados
#-----------------------------

# Imprime estado de la optimización
# Recupera del diccionario el estado: “Not Solved”, “Infeasible”, “Unbounded”,
# “Undefined” or “Optimal”.
print("Estado (optimizador):", pulp.LpStatus[problema.status])

# Imprime el valor del objetivo
print("Incremento ventas=", pulp.value(problema.objective))

# Imprime valor de las variables
for v in problema.variables():
	print(v.name, "=", v.varValue)
