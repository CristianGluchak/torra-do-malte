import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# define entradas e saidas
temperatura = ctrl.Antecedent(np.arange(0, 251, 1), 'temperatura')
duracao = ctrl.Antecedent(np.arange(0, 61, 1), 'duracao')
delay = ctrl.Consequent(np.arange(0, 11, 1), 'delay')

#aqui foi definido as funções de pertinência para a temperatura
temperatura['baixa'] = fuzz.trimf(temperatura.universe, [0, 0, 125])
temperatura['media'] = fuzz.trimf(temperatura.universe, [100, 150, 200])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [150, 250, 250])

# aqui as funções de pertinência para a duração
duracao['curta'] = fuzz.trimf(duracao.universe, [0, 0, 30])
duracao['media'] = fuzz.trimf(duracao.universe, [20, 30, 40])
duracao['longa'] = fuzz.trimf(duracao.universe, [30, 60, 60])

#aqui as funções de pertinência para o delay
delay['baixo'] = fuzz.trimf(delay.universe, [0, 0, 5])
delay['medio'] = fuzz.trimf(delay.universe, [2, 5, 8])
delay['alto'] = fuzz.trimf(delay.universe, [5, 10, 10])

# aqui definiremos as regras Fuzzy
rule1 = ctrl.Rule(temperatura['baixa'] & duracao['curta'], delay['alto'])
rule2 = ctrl.Rule(temperatura['baixa'] & duracao['media'], delay['medio'])
rule3 = ctrl.Rule(temperatura['baixa'] & duracao['longa'], delay['baixo'])
rule4 = ctrl.Rule(temperatura['media'] & duracao['curta'], delay['medio'])
rule5 = ctrl.Rule(temperatura['media'] & duracao['media'], delay['baixo'])
rule6 = ctrl.Rule(temperatura['media'] & duracao['longa'], delay['baixo'])
rule7 = ctrl.Rule(temperatura['alta'] & duracao['curta'], delay['baixo'])
rule8 = ctrl.Rule(temperatura['alta'] & duracao['media'], delay['baixo'])
rule9 = ctrl.Rule(temperatura['alta'] & duracao['longa'], delay['baixo'])

# Criando o sistema de controle
controlador_delay = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
simulacao_delay = ctrl.ControlSystemSimulation(controlador_delay)

# Simulando uma entrada específica
def simular_controle_fuzzy(temp, dur):
    simulacao_delay.input['temperatura'] = temp
    simulacao_delay.input['duracao'] = dur
    simulacao_delay.compute()
    return simulacao_delay.output['delay']

# Solicitando entradas do usuário
try:
    temperatura_desejada = float(input("Digite a temperatura desejada (°C): "))
    duracao_desejada = float(input("Digite a duração desejada (minutos): "))
except ValueError:
    print("Por favor, insira valores numéricos válidos.")
    exit()

# Verificando se as entradas estão dentro dos limites
if not (0 <= temperatura_desejada <= 250) or not (0 <= duracao_desejada <= 60):
    print("Os valores inseridos estão fora dos limites permitidos.")
    exit()

# Simulando o sistema com os valores fornecidos pelo usuário
valor_delay = simular_controle_fuzzy(temperatura_desejada, duracao_desejada)
print(f'Valor de delay calculado: {valor_delay}')


temperatura.view()
duracao.view()
delay.view()
plt.show()
