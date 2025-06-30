import google.generativeai as genai
import pandas as pd
import cirq
import numpy as np
import os
from sympy import Symbol

# Step 1: Classify heart disease risk
def classify_heart_disease(row):
    # Convert values to numeric for safety
    values = {
        "Heart Rate": pd.to_numeric(row.get('heart rate', "N/A"), errors='coerce'),
        "Blood Pressure": pd.to_numeric(row.get('blood pressure', "N/A"), errors='coerce'),
        "Stress Level": pd.to_numeric(row.get('stress level', "N/A"), errors='coerce')
    }

    risk_factors = []

    if values["Heart Rate"] > 100:
        risk_factors.append("Heart Rate")
    if values["Blood Pressure"] > 140:
        risk_factors.append("Blood Pressure")
    if values["Stress Level"] > 6:
        risk_factors.append("Stress Level")

    if risk_factors:
        return "High Risk", risk_factors, values
    else:
        return "Low Risk", [], values

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Step 2: Generate detailed medical report using Gemini
def generate_report(risk_factors, values):
    if not risk_factors:
        return (
            "🟢 Low Risk Summary\n"
            "----------------------------------------\n"
            "✅ The patient's biometric indicators are within acceptable ranges.\n\n"
            "Observations:\n"
            "- Normal heart rate\n"
            "- Normal blood pressure\n"
            "- Normal stress level\n\n"
            "Recommendation:\n"
            "- Continue regular exercise and heart-healthy diet\n"
            "- Schedule annual checkups\n"
            "- Maintain low stress levels through relaxation techniques\n"
        )

    prompt = f"""
    You are a medical assistant AI.
    The patient shows the following abnormal vital signs:
    Risk Factors: {', '.join(risk_factors)}
    Measured Values: {', '.join([f"{k} = {v}" for k, v in values.items()])}

    Generate a detailed medical report in paragraph format that includes:
    - Explanation of abnormal values
    - Possible underlying conditions
    - Related diseases
    - Suggested clinical tests
    - Final recommendation

    Use a formal tone and structure the report with medical insights. Format the text as if it's written by a doctor.
    """

    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠ Error generating report: {str(e)}"

# Step 3: Quantum Optimization with QAOA-style logic
def quantum_optimize_health_risk():
    qubits = [cirq.GridQubit(0, i) for i in range(3)]
    gamma = Symbol('gamma')
    beta = Symbol('beta')
    circuit = cirq.Circuit()

    # Initial state
    circuit += [cirq.H(q) for q in qubits]

    # Cost layer
    for q in qubits:
        circuit += cirq.ZPowGate(exponent=gamma / np.pi)(q)

    # Mixer layer
    for q in qubits:
        circuit += cirq.rx(2 * beta)(q)

    circuit += cirq.measure(*qubits, key='result')
    resolver = cirq.ParamResolver({'gamma': np.pi / 2, 'beta': np.pi / 4})
    simulator = cirq.Simulator()
    result = simulator.run(circuit, resolver, repetitions=100)
    histogram = result.histogram(key='result')
    best_state = min(histogram.items(), key=lambda x: bin(x[0]).count("1"))
    binary_state = format(best_state[0], "03b")

    factors = ["Heart Rate", "Blood Pressure", "Stress Level"]
    report = {f: ("High" if binary_state[i] == '1' else "Normal") for i, f in enumerate(factors)}

    return {
        "quantum_state": binary_state,
        "optimized_risk_factors": [f for f, s in report.items() if s == "High"],
        "optimization_report": report,
        "quantum_message": "QAOA-inspired optimization simulated successfully."
    }

# Step 4: Create Risk Table
def create_risk_table(all_values):
    expected_params = {
        "Heart Rate": all_values.get("Heart Rate", "N/A"),
        "Blood Pressure": all_values.get("Blood Pressure", "N/A"),
        "Stress Level": all_values.get("Stress Level", "N/A")
    }

    table = "<table border='1' style='border-collapse:collapse; padding:8px;'>"
    table += "<tr><th>Parameter</th><th>Value</th><th>Status</th></tr>"

    for k, v in expected_params.items():
        if pd.isna(v):
            status = "Not Provided"
            color = "gray"
        else:
            if k == "Heart Rate":
                abnormal = v > 100
            elif k == "Blood Pressure":
                abnormal = v > 140
            elif k == "Stress Level":
                abnormal = v > 6
            else:
                abnormal = False
            status = "Abnormal" if abnormal else "Normal"
            color = "red" if abnormal else "green"

        table += f"<tr><td>{k}</td><td>{v}</td><td style='color:{color};'>{status}</td></tr>"

    table += "</table>"
    return table

# Step 5: Full pipeline
def process_xls(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.drop(columns=['patient id'], errors='ignore')
    row = df.iloc[0]

    status, risk_factors, values = classify_heart_disease(row)
    report = generate_report(risk_factors, values)
    quantum_info = quantum_optimize_health_risk()
    risk_table = create_risk_table(values)
    abnormal_factors = {k: v for k, v in values.items() if k in risk_factors}

    return {
        "risk": status,
        "risk_factors": risk_factors,
        "values": values,
        "abnormal_factors": abnormal_factors,
        "report": report,
        "risk_table": risk_table,
        "quantum": quantum_info
    }
