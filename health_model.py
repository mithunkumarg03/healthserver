import google.generativeai as genai
import pandas as pd
import cirq
import requests

# Step 1: Classify heart disease risk
def classify_heart_disease(row):
    risk_factors = []

    # Always collect all relevant values
    values = {
        "Heart Rate": row.get('heart rate', "N/A"),
        "Blood Pressure": row.get('blood pressure', "N/A"),
        "Stress Level": row.get('stress level', "N/A")
    }

    # Check for abnormalities
    if isinstance(values["Heart Rate"], (int, float)) and values["Heart Rate"] > 100:
        risk_factors.append("Heart Rate")
    if isinstance(values["Blood Pressure"], (int, float)) and values["Blood Pressure"] > 140:
        risk_factors.append("Blood Pressure")
    if isinstance(values["Stress Level"], (int, float)) and values["Stress Level"] > 6:
        risk_factors.append("Stress Level")

    if risk_factors:
        return "High Risk", risk_factors, values
    else:
        return "Low Risk", [], values

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


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
    # Construct prompt for Gemini
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
        return f"⚠️ Error generating report: {str(e)}"


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
    expected_params = {
        "Heart Rate": all_values.get("Heart Rate", "N/A"),
        "Blood Pressure": all_values.get("Blood Pressure", "N/A"),
        "Stress Level": all_values.get("Stress Level", "N/A")
    }
    
    table = "<table border='1' style='border-collapse:collapse; padding:8px;'>"
    table += "<tr><th>Parameter</th><th>Value</th><th>Status</th></tr>"
    
    for k, v in expected_params.items():
        if v == "N/A":
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

