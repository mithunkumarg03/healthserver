import pandas as pd
import cirq
import requests

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

# Step 2: Generate detailed medical report using Hugging Face API
def generate_report(risk_factors, values):
    if not risk_factors:
        return (
            "The patient shows stable vital signs with no significant indicators of heart disease. "
            "It is recommended to maintain regular exercise, a balanced diet, and schedule periodic check-ups to ensure continued health."
        )

    prompt = f"""
You are a senior medical consultant. Write a comprehensive, formal medical report for a patient showing high risk for heart disease.

Detected Risk Factors: {', '.join(risk_factors)}.
Measured Values: {', '.join([f"{k}: {v}" for k, v in values.items()])}.

Include:
1. Explanation of the significance of each abnormal parameter.
2. Possible medical conditions or diseases associated with these values.
3. Advice on further diagnostic tests or immediate medical actions.
4. General health recommendations and lifestyle changes.
Use a professional, medical tone. Write at least 3 paragraphs.
"""

    api_url = "https://api-inference.huggingface.co/models/tiiuae/falcon-rw-1b"
    headers = {  
        "Accept": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 500,
            "do_sample": True
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        elif isinstance(result, dict) and 'generated_text' in result:
            return result['generated_text']
        else:
            return "The patient shows high risk. Please consult a healthcare professional."
    except Exception as e:
        return f"Unable to generate AI report due to API error: {str(e)}"

# Step 3: Quantum Optimization Simulation (Cirq)
def simulate_quantum_decision():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append([cirq.H(q) for q in qubits])
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

# Step 4: Create Risk Table in HTML format
def create_risk_table(values):
    if not values:
        return "<p>No abnormal health parameters detected.</p>"
    
    table = "<table border='1' style='border-collapse:collapse; padding:8px;'>"
    table += "<tr><th>Parameter</th><th>Value</th></tr>"
    for k, v in values.items():
        table += f"<tr><td>{k}</td><td>{v}</td></tr>"
    table += "</table>"
    return table

# Step 5: Full Process Function
def process_xls(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.drop(columns=['patient id'], errors='ignore')
    row = df.iloc[0]

    status, risk_factors, values = classify_heart_disease(row)
    report = generate_report(risk_factors, values)
    quantum_info = simulate_quantum_decision()
    risk_table = create_risk_table(values)

    return {
        "risk": status,
        "risk_factors": risk_factors,
        "values": values,
        "report": report,
        "risk_table": risk_table,
        "quantum": quantum_info
    }
