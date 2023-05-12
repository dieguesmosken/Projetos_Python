import numpy as np
import matplotlib.pyplot as plt

# Criando um vetor no espaço-tempo com coordenadas (1, 2, 3, 4)
vetor = np.array([1, 2, 3, 4])

# Criando um gráfico de Minkowski com limites de eixo de -5 a 5 em cada dimensão
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_xlabel('Coordenada espacial x')
ax.set_ylabel('Coordenada espacial y')
ax.set_aspect('equal')

# Plotando o vetor como uma seta no diagrama
ax.arrow(0, 0, vetor[0], vetor[1], head_width=0.2, head_length=0.2, fc='r', ec='r')
