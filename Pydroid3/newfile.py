import matplotlib.pyplot as plt
import numpy as np

# Definindo os pontos do vetor de imagem
x = np.linspace(-2, 2, 1000)
y = np.sin(np.pi * x) / x

# Criando a imagem com os pontos definidos
fig, ax = plt.subplots()
ax.plot(x, y, 'k')
ax.fill_between(x, y, 0, where=(y > 0), interpolate=True, color='brown')
ax.fill_between(x, y, 0, where=(y < 0), interpolate=True, color='white')

# Configurando a imagem
ax.axis('off')
ax.set_xlim(-2, 2)
ax.set_ylim(-1.5, 1.5)

# Exibindo a imagem
plt.show()
