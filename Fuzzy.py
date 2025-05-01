import numpy as np
import skfuzzy as fuzz

voltage_deviation_domain = np.arange(0, 21, 1)
frequency_variation_domain = np.arange(0, 2.1, 0.1)
load_imbalance_domain = np.arange(0, 51, 1)    
severity_domain = np.arange(0, 101, 1)

# Defining the membership functions for each occasion
voltage_low = fuzz.trimf(voltage_deviation_domain, [0, 0, 5])
voltage_medium = fuzz.trimf(voltage_deviation_domain, [2, 7, 12])
voltage_high = fuzz.trimf(voltage_deviation_domain, [10, 20, 20])

frequency_stable = fuzz.trimf(frequency_variation_domain, [0, 0, 0.5])
frequency_unstable = fuzz.trimf(frequency_variation_domain, [0.3, 2, 2])

load_imbalance_balanced = fuzz.trimf(load_imbalance_domain, [0, 0, 20])
load_imbalance_unbalanced = fuzz.trimf(load_imbalance_domain, [15, 50, 50])

severity_low = fuzz.trimf(severity_domain, [0, 0, 30])
severity_moderate = fuzz.trimf(severity_domain, [20, 50, 80])
severity_high = fuzz.trimf(severity_domain, [70, 100, 100])



def fuzzification(voltage_deviation_input, frequency_variation_input, load_imbalance_input):
    voltage_deviation_low_degreee = fuzz.interp_membership(voltage_deviation_domain, voltage_low, voltage_deviation_input)
    voltage_deviation_medium_degreee = fuzz.interp_membership(voltage_deviation_domain, voltage_medium, voltage_deviation_input)
    voltage_deviation_high_degreee = fuzz.interp_membership(voltage_deviation_domain, voltage_high, voltage_deviation_input)

    frequency_variation_stable_degree = fuzz.interp_membership(frequency_variation_domain, frequency_stable, frequency_variation_input)
    frequency_variation_unstable_degree = fuzz.interp_membership(frequency_variation_domain, frequency_unstable, frequency_variation_input)

    load_imbalance_balanced_degree = fuzz.interp_membership(load_imbalance_domain, load_imbalance_balanced, load_imbalance_input)
    load_imbalance_unbalanced_degree = fuzz.interp_membership(load_imbalance_domain, load_imbalance_unbalanced, load_imbalance_input)

    return {
        'voltage_deviation_low_degreee': voltage_deviation_low_degreee, 
        'voltage_deviation_medium_degreee': voltage_deviation_medium_degreee, 
        'voltage_deviation_high_degreee': voltage_deviation_high_degreee,
        'frequency_variation_stable_degree': frequency_variation_stable_degree, 
        'frequency_variation_unstable_degree': frequency_variation_unstable_degree,
        'load_imbalance_balanced_degree': load_imbalance_balanced_degree, 
        'load_imbalance_unbalanced_degree': load_imbalance_unbalanced_degree
    }


#Defining and applying Fuzzy rules 
def fuzzy_rules_application(fuzzy_inputs):

    high_strength = min(fuzzy_inputs['voltage_deviation_high_degreee'], fuzzy_inputs['frequency_variation_unstable_degree'], fuzzy_inputs['load_imbalance_unbalanced_degree'])

    moderate_strength_1 = min(fuzzy_inputs['voltage_deviation_medium_degreee'], fuzzy_inputs['load_imbalance_unbalanced_degree'],fuzzy_inputs['frequency_variation_unstable_degree'])

    low_strength = min(fuzzy_inputs['voltage_deviation_low_degreee'], fuzzy_inputs['frequency_variation_stable_degree'], fuzzy_inputs['load_imbalance_balanced_degree'])

    moderate_strength_2 = min(fuzzy_inputs['voltage_deviation_high_degreee'], fuzzy_inputs['frequency_variation_stable_degree'])

    moderate_strength_3 = min(fuzzy_inputs['voltage_deviation_high_degreee'], fuzzy_inputs['load_imbalance_balanced_degree'])
   
    final_moderate_strength = max(moderate_strength_1, moderate_strength_2, moderate_strength_3)

    return low_strength, final_moderate_strength, high_strength




def defuzzify(low_strength, moderate_strength, high_strength):  

    #Capping the membership function values acoring to the fuzzy output values
    low_output = np.minimum(low_strength, severity_low)
    moderate_output = np.minimum(moderate_strength, severity_moderate)
    high_output = np.minimum(high_strength, severity_high)
    
    #Combining all the capped values for each membership function
    aggregated_output = np.maximum.reduce([low_output, moderate_output, high_output])
    
    #Applying Centroid method to get the crisp ourput (severity level)
    severity = np.sum(aggregated_output * severity_domain) / np.sum(aggregated_output)
    
    
    if severity >= 70:
        action = "Load Balancing"  
    elif 30 <= severity < 70:
        action = "Frequency Regulation"  
    elif 10 <= severity < 30:
        action = "Power factor correction"
    else:
        action = "No action needed" 
    
    
    return severity, action


def run(voltage_deviation, frequency_variation, load_imbalance):
    fuzzy_inputs = fuzzification(voltage_deviation, frequency_variation, load_imbalance)
    low_strength, final_moderate_strength, high_strength = fuzzy_rules_application(fuzzy_inputs)
    severity, action = defuzzify(low_strength, final_moderate_strength, high_strength)
    print("Severity Level", severity)
    print("action", action)

test_cases = [
    {"voltage": 2, "frequency": 0.2, "load": 10},
    {"voltage": 15, "frequency": 1.7, "load": 30},
    {"voltage": 18, "frequency": 2.0, "load": 45},
    {"voltage": 7, "frequency": 0.8, "load": 25},
    {"voltage": 20, "frequency": 0.1, "load": 5}
]

# Run simulation
def run_simulation():
    print("Test cases\n")
    
    for case in test_cases:
        fuzzy_inputs = fuzzification(case["voltage"], case["frequency"], case["load"])
        low, mod, high = fuzzy_rules_application(fuzzy_inputs)
        severity, action = defuzzify(low, mod, high)
        print(f"{case['voltage']:<10} {case['frequency']:<10} {case['load']:<10} {severity:<10} {action:<20}")

run_simulation()
