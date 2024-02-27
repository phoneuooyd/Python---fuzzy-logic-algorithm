import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def fuzzy(patient_age_to_func, patient_weight_to_func, type_of_medicine = "Paracetamol"):
    amount_of_medicine_simulation.input['Wiek pacjenta'] = patient_age_to_func
    amount_of_medicine_simulation.input['Waga pacjetna'] = patient_weight_to_func
    amount_of_medicine_simulation.compute()
    amt_med = amount_of_medicine_simulation.output['Dawkowanie leku']
    
    print(f"Dla pacjenta o Wieku/Wadze {patient_age_to_func}/{patient_weight_to_func}: Dawka leku {type_of_medicine} = {amt_med} mg /6 godzin, {amt_med * 4} mg /24h")

print("Program przedstawiający działanie logiki rozmytej! Przed spożyciem leku należy się zastosować do wskazań lekarza lub \n ulotki dołąconej do opakowania! Niepoprawne stosowanie leku grozi utratą życia lub zdrowia")
patient_age = ctrl.Antecedent(np.arange(1, 101, 1), 'Wiek pacjenta')
patient_weight = ctrl.Antecedent(np.arange(1, 151, 1), 'Waga pacjetna')
amount_of_medicine = ctrl.Consequent(np.arange(1, 680, 1), 'Dawkowanie leku')

patient_age['Młody'] = fuzz.trapmf(patient_age.universe,                     [1, 1, 14, 21])
patient_age['W średnim wieku'] = fuzz.trapmf(patient_age.universe,           [18, 35, 45, 60])
patient_age['Stary'] = fuzz.trapmf(patient_age.universe,                     [45, 65, 85, 100])
patient_weight['Mała waga'] = fuzz.trapmf(patient_weight.universe,           [1, 1, 15, 30])
patient_weight['Średnia waga'] = fuzz.trapmf(patient_weight.universe,        [25, 50, 60,  80])
patient_weight['Duża waga'] = fuzz.trapmf(patient_weight.universe,           [75, 95, 115, 150])
amount_of_medicine['Doraźna'] = fuzz.trapmf(amount_of_medicine.universe,     [1, 20, 40, 60])
amount_of_medicine['Mała'] = fuzz.trapmf(amount_of_medicine.universe,        [40, 50, 70, 130])
amount_of_medicine['Średnia'] = fuzz.trapmf(amount_of_medicine.universe,     [80, 250, 300, 400])
amount_of_medicine['Duża'] = fuzz.trapmf(amount_of_medicine.universe,        [380, 400, 450, 550])
amount_of_medicine['Bardzo duża'] = fuzz.trapmf(amount_of_medicine.universe, [490, 600, 620, 680])

rule1 = ctrl.Rule(patient_age['Młody'] &           patient_weight['Mała waga'],    amount_of_medicine['Doraźna'])
rule2 = ctrl.Rule(patient_age['Młody'] &           patient_weight['Średnia waga'], amount_of_medicine['Mała'])
rule3 = ctrl.Rule(patient_age['Młody'] &           patient_weight['Duża waga'],    amount_of_medicine['Średnia'])
rule4 = ctrl.Rule(patient_age['W średnim wieku'] & patient_weight['Mała waga'],    amount_of_medicine['Średnia'])
rule5 = ctrl.Rule(patient_age['W średnim wieku'] & patient_weight['Średnia waga'], amount_of_medicine['Duża'])
rule6 = ctrl.Rule(patient_age['W średnim wieku'] & patient_weight['Duża waga'],    amount_of_medicine['Bardzo duża'])
rule7 = ctrl.Rule(patient_age['Stary'] &           patient_weight['Mała waga'],    amount_of_medicine['Mała'])
rule8 = ctrl.Rule(patient_age['Stary'] &           patient_weight['Średnia waga'], amount_of_medicine['Średnia'])
rule9 = ctrl.Rule(patient_age['Stary'] &           patient_weight['Duża waga'],    amount_of_medicine['Duża'])

amount_of_medicine_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
amount_of_medicine_simulation = ctrl.ControlSystemSimulation(amount_of_medicine_ctrl)
fuzzy( 5, 25)
fuzzy( 15, 75)
fuzzy( 20, 80)
fuzzy( 30, 80)
fuzzy( 40, 80)
fuzzy( 40, 120)
fuzzy( 50, 130)
fuzzy( 70, 80)
patient_weight.view()
patient_age.view()
amount_of_medicine.view()
plt.show()