import pandas as pd
import numpy as np
import cirq
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load lightweight LLM model (FLAN-T5 Small)
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

# Step 1: Classify heart disease risk
def classify_heart_disease(row):
    risk_factors = []
    values = {}
    if row['heart rate'] > 100:
        risk_factors.append("Heart Rate")
        values['Heart Rate'] = row['heart rate']
    if row['blood pressure'] > 140:
        risk_factors.append("Blood Pressure")
        values['Blood Pressure'] = row['blood pressure']
    if row['stress level'] > 6:
        risk_factors.append("Stress Level")
        values['Stress Level'] = row['stress level']
    if risk_factors:
        return "High Risk", risk_factors, values
    else:
        return "Low Risk", [], values

# Step 2: Generate detailed medical report using LLM
def generate_report(risk_factors, values):
    if not risk_factors:
        return "The patient shows stable vitals with no major risk factors detected. It is advised to continue a healthy lifestyle with regular checkups."

    prompt = f"""Generate a detailed medical report in paragraph format for a patient with high risk of heart disease due to the following:
    Risk Factors: {', '.join(risk_factors)}.
    Corresponding Values: {', '.join([f"{k} = {v}" for k, v in values.items()])}.
    Include possible diseases and medical recommendations. Use formal medical tone."""

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=250)
    report = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return report

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

    # Clean column names: strip spaces and convert to lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Drop 'patient id' if it exists (already lowercase now)
    df = df.drop(columns=['patient id'], errors='ignore')

    row = df.iloc[0]  # Only first record

    # Perform risk classification
    status, risk_factors, values = classify_heart_disease(row)
    
    # Generate detailed report
    report = generate_report(risk_factors, values)
    
    # Quantum Simulation
    quantum_info = simulate_quantum_decision()

    return {
        "risk": status,
        "risk_factors": risk_factors,
        "report": report,
        "quantum": quantum_info,
        "values": values
    }
