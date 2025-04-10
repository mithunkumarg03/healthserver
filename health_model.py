import pandas as pd
import numpy as np
import cirq




# Step 1: Classify heart disease risk
def classify_heart_disease(row):
    risk_factors = []
    if row['Heart Rate'] > 100:
        risk_factors.append("Heart Rate")
    if row['Blood Pressure'] > 140:
        risk_factors.append("Blood Pressure")
    if row['Stress Level'] > 6:
        risk_factors.append("Stress Level")
    if risk_factors:
        return "High Risk", risk_factors
    else:
        return "Low Risk", []

# Step 2: Generate health report using LLM
def generate_report(risk_factors):
    if not risk_factors:
        return "The patient is at low risk of heart disease. Maintain a healthy lifestyle."
    else:
        reasons = ', '.join(risk_factors)
        return f"The patient is at high risk of heart disease due to {reasons}. Immediate medical attention is advised."
# Step 3: Quantum Optimization Simulation (Cirq)
def simulate_quantum_decision():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append([cirq.H(q) for q in qubits])  # Initial layer of Hadamard gates

    # Simulate simple parameterized quantum gates (like QAOA)
    for q in qubits:
        circuit.append(cirq.Z(q) ** 0.5)
        circuit.append(cirq.X(q) ** 0.3)

    circuit.append(cirq.measure(*qubits, key='result'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=100)
    histogram = result.histogram(key='result')

    most_common = max(histogram, key=histogram.get)
    return {
        "quantum_result": format(most_common, '03b'),
        "explanation": "Quantum simulation completed. Used to explore risk decision landscape."
    }

# Step 4: Full Process Function
def process_xls(file_path):
    df = pd.read_excel(file_path)
    df = df.drop(columns=['patient id'], errors='ignore')

    row = df.iloc[0]  # Only first record
    status, risk_factors = classify_heart_disease(row)
    report = generate_report(risk_factors)
    quantum_info = simulate_quantum_decision()

    return {
        "risk": status,
        "risk_factors": risk_factors,
        "report": report,
        "quantum": quantum_info
    }
