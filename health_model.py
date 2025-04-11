import pandas as pd
import cirq
import requests

# Step 1: Classify heart disease risk based on key vitals
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

# Step 2: AI-style dynamic report generation (LLM API or fallback to long dynamic logic)
def generate_report(risk_factors, values):
    if not risk_factors:
        return ("The patient's vital parameters — including heart rate, blood pressure, and stress level — "
                "appear within acceptable medical limits. No immediate indicators of cardiovascular strain or "
                "risk were found. However, it is advised to maintain a healthy lifestyle with balanced diet, "
                "regular physical activity, stress reduction techniques, and annual cardiovascular screening.")

    # ---- Attempt to use Hugging Face Falcon 7B Instruct Model ----
    prompt = f"""Generate a **long, formal medical report** for a patient showing HIGH RISK of heart disease.
    Risk Factors: {', '.join(risk_factors)}.
    Corresponding Values: {', '.join([f"{k} = {v}" for k, v in values.items()])}.
    Include a deep explanation of each parameter's abnormality, how it can contribute to heart disease,
    and provide detailed doctor recommendations in medical language."""

    api_url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_TOKEN"}  # Replace with your token

    try:
        response = requests.post(api_url, headers=headers, json={"inputs": prompt}, timeout=40)
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
    except Exception as e:
        pass  # If API fails, fallback below

    # ---- Fallback: Manual dynamic long explanation ----
    explanation = ["The patient's clinical assessment reveals the presence of several key physiological parameters exceeding normal thresholds, indicating an elevated risk for cardiovascular disorders. Below is an in-depth analysis:"]

    for param, val in values.items():
        if param == "Heart Rate":
            explanation.append(f"\n**Heart Rate ({val} bpm):** A heart rate exceeding 100 beats per minute is considered tachycardia. Persistent tachycardia can reduce the efficiency of the heart, causing strain on myocardial tissue. This condition can lead to reduced oxygen delivery and increase the likelihood of arrhythmias, heart failure, or even cardiac arrest.")
        elif param == "Blood Pressure":
            explanation.append(f"\n**Blood Pressure ({val} mmHg):** Hypertension, defined as blood pressure greater than 140 mmHg systolic, is a leading contributor to heart attacks and strokes. It causes progressive arterial damage and promotes left ventricular hypertrophy, making the heart less efficient over time.")
        elif param == "Stress Level":
            explanation.append(f"\n**Stress Level ({val}/10):** Chronic stress contributes to elevated cortisol levels, vasoconstriction, and sympathetic overactivation. This exacerbates existing conditions such as hypertension and can trigger inflammatory processes that damage endothelial function, accelerating plaque formation in arteries.")

    explanation.append("\n**Conclusion and Recommendations:**\nBased on the combination of these parameters, the patient is classified as HIGH RISK for cardiovascular events. It is strongly advised to schedule a comprehensive cardiac evaluation including ECG, echocardiography, and blood lipid profiling. The patient should immediately adopt lifestyle changes, including reducing sodium intake, engaging in daily aerobic exercise, stress management (e.g., meditation, therapy), and pharmacological interventions under clinical supervision.")

    return "\n".join(explanation)

# Step 3: Quantum simulation for symbolic decision (not used for logic but visual feedback)
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
        "explanation": "Quantum simulation completed using 3-qubit hybrid gates. Result visualizes potential health state bifurcation under probabilistic scenarios."
    }

# Step 4: Create HTML health parameter table
def create_risk_table(values):
    if not values:
        return "<p>No abnormal health parameters detected.</p>"
    
    table = "<table border='1' style='border-collapse:collapse; padding:8px;'>"
    table += "<tr><th>Parameter</th><th>Value</th></tr>"
    for k, v in values.items():
        table += f"<tr><td>{k}</td><td>{v}</td></tr>"
    table += "</table>"
    return table

# Step 5: Main end-to-end report generation pipeline
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
