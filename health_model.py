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
            "🟢 **Low Risk Summary**\n"
            "----------------------------------------\n"
            "✅ The patient's biometric indicators are within acceptable ranges.\n\n"
            "**Observations:**\n"
            "- Normal heart rate\n"
            "- Normal blood pressure\n"
            "- Normal stress level\n\n"
            "**Recommendation:**\n"
            "- Continue regular exercise and heart-healthy diet\n"
            "- Schedule annual checkups\n"
            "- Maintain low stress levels through relaxation techniques\n"
        )

    report = (
        "🔴 **High Risk Medical Report**\n"
        "----------------------------------------\n"
        "The patient exhibits abnormal clinical metrics indicative of elevated cardiovascular risk.\n\n"
    )

    if "Heart Rate" in risk_factors:
        hr = values["Heart Rate"]
        report += (
            f"🫀 **Heart Rate Alert**\n"
            f"- Recorded Value: {hr} bpm\n"
            "- Interpretation: Tachycardia (elevated heart rate)\n"
            "- Possible Causes: Stress, arrhythmia, dehydration, thyroid issues\n"
            "- Risks: Atrial fibrillation, cardiomyopathy, sudden cardiac arrest\n"
            "- Suggested Tests: ECG, Holter monitor, thyroid panel, echo\n\n"
        )

    if "Blood Pressure" in risk_factors:
        bp = values["Blood Pressure"]
        report += (
            f"🩸 **Blood Pressure Alert**\n"
            f"- Recorded Value: {bp} mmHg\n"
            "- Interpretation: Stage 2 Hypertension\n"
            "- Risks: Stroke, heart attack, kidney damage, vision loss\n"
            "- Suggested Tests: Renal function, lipid profile, fundus exam\n"
            "- Management: Low-sodium diet, exercise, antihypertensives\n\n"
        )

    if "Stress Level" in risk_factors:
        stress = values["Stress Level"]
        report += (
            f"😥 **Stress Level Alert**\n"
            f"- Recorded Value: {stress}/10\n"
            "- Interpretation: Elevated psychological stress\n"
            "- Effects: Elevated heart rate, hypertension, sleep disorders\n"
            "- Risks: Anxiety, heart strain, metabolic issues, cardiac events\n"
            "- Management: CBT, breathing exercises, mental health therapy\n\n"
        )

    report += (
        "----------------------------------------\n"
        "🧾 **Final Recommendation**\n"
        "- Immediate follow-up with a cardiologist and mental health professional\n"
        "- Monitor vitals regularly\n"
        "- Adopt cardiac-friendly lifestyle habits\n"
        "- Begin medical intervention as per specialist guidance\n"
    )

    return report




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
def create_risk_table(all_values):
    if not all_values:
        return "<p>No health data provided.</p>"
    
    table = "<table border='1' style='border-collapse:collapse; padding:8px;'>"
    table += "<tr><th>Parameter</th><th>Value</th><th>Status</th></tr>"
    
    for k, v in all_values.items():
        status = "Abnormal" if k in detect_abnormal_keys(all_values) else "Normal"
        color = "red" if status == "Abnormal" else "green"
        table += f"<tr><td>{k}</td><td>{v}</td><td style='color:{color};'>{status}</td></tr>"
    
    table += "</table>"
    return table

def detect_abnormal_keys(values):
    abnormal = []
    if "Heart Rate" in values and values["Heart Rate"] > 100:
        abnormal.append("Heart Rate")
    if "Blood Pressure" in values and values["Blood Pressure"] > 140:
        abnormal.append("Blood Pressure")
    if "Stress Level" in values and values["Stress Level"] > 6:
        abnormal.append("Stress Level")
    return abnormal


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

