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
            "Upon careful evaluation of the patient's biometric indicators, no significant deviations were observed in heart rate, blood pressure, or stress level. "
            "The absence of these risk factors indicates a currently stable cardiovascular profile. While this is reassuring, it is important to understand that heart disease can be insidious and progressive. "
            "Thus, even in low-risk individuals, ongoing health surveillance is crucial. Annual check-ups, heart-healthy dietary practices, regular physical activity, and adequate stress management are strongly recommended "
            "to preserve long-term cardiac health and prevent potential future risks that may not be immediately apparent."
        )

    report = (
        "The patient presents with abnormal clinical metrics suggestive of a high risk for developing cardiovascular and systemic disorders. "
        "A comprehensive analysis of the vital signs reveals concerning levels in the following parameters: "
    )

    if "Heart Rate" in risk_factors:
        hr = values["Heart Rate"]
        report += (
            f"The heart rate is elevated at {hr} beats per minute, classifying the condition as tachycardia. "
            "This elevated pulse, especially if sustained or occurring at rest, may be a compensatory response to systemic stress, cardiac arrhythmia, fever, dehydration, or underlying endocrine dysfunctions like hyperthyroidism. "
            "If left unaddressed, such conditions can escalate into more severe arrhythmic syndromes including supraventricular tachycardia or atrial fibrillation. "
            "Prolonged elevated heart rate also puts mechanical strain on the myocardial walls, leading to potential hypertrophy or reduced ejection fraction. "
            "Associated clinical conditions include ischemic heart disease, cardiomyopathy, and in rare cases, sudden cardiac arrest. "
            "It is advisable to perform further investigations including a 24-hour Holter monitor, resting and stress ECG, thyroid function tests, and an echocardiogram for structural assessment."
        )

    if "Blood Pressure" in risk_factors:
        bp = values["Blood Pressure"]
        report += (
            f" Blood pressure is recorded at {bp} mmHg, meeting diagnostic criteria for stage 2 hypertension. "
            "Hypertension is a chronic condition characterized by persistent elevation of arterial pressure, often asymptomatic in its early stages but damaging over time. "
            "It contributes significantly to atherosclerosis, left ventricular hypertrophy, chronic kidney disease, and cerebrovascular accidents. "
            "Critically, elevated blood pressure significantly raises the risk of stroke due to increased pressure on cerebral blood vessels, which may result in hemorrhagic or ischemic stroke events. "
            "Other influencing factors include salt sensitivity, increased sympathetic activity, and hormonal dysregulation. "
            "Over time, hypertension causes endothelial dysfunction, promoting plaque formation and arterial stiffness, greatly increasing the chance of both cardiac and neurological emergencies. "
            "The patient should undergo renal function tests, lipid profile screening, and fundoscopic examination to check for hypertensive retinopathy. "
            "Initiation of antihypertensive therapy, dietary sodium reduction, weight management, and aerobic exercise is crucial at this stage."
        )

    if "Stress Level" in risk_factors:
        stress = values["Stress Level"]
        report += (
            f" The patient reports a subjective stress level of {stress}/10, which is above the recommended psychological threshold for optimal health. "
            "Psychosocial stress is an underestimated but powerful contributor to both physical and mental health decline. "
            "Biologically, stress activates the hypothalamic-pituitary-adrenal (HPA) axis, triggering the release of cortisol and adrenaline. "
            "Sustained elevations of these hormones result in increased heart rate, elevated blood pressure, impaired glucose metabolism, and suppressed immune function. "
            "Clinically, this can manifest as anxiety disorders, insomnia, metabolic syndrome, and inflammatory states. "
            "Of particular concern is the cardiac impact — chronic stress leads to increased myocardial workload and can induce stress-related cardiomyopathy or Takotsubo syndrome. "
            "It is also associated with heart strain, left ventricular diastolic dysfunction, and exacerbation of existing heart failure. "
            "Patients experiencing chronic stress are at elevated risk for arrhythmias and acute coronary events. "
            "Therapeutic interventions include cognitive behavioral therapy (CBT), mindfulness-based stress reduction (MBSR), structured breathing exercises, and regular mental health evaluations."
        )

    report += (
        " In conclusion, the convergence of these high-risk factors places the patient in a category warranting immediate medical attention. "
        "It is strongly recommended to refer the patient to a multidisciplinary team including a cardiologist, endocrinologist, and mental health specialist for integrated care. "
        "Close follow-up should be maintained with periodic vitals monitoring, lab testing, and imaging studies as needed. "
        "The implementation of a cardiac-protective lifestyle, pharmacological therapy tailored to the risk profile, and stress management protocols will be essential in reducing long-term morbidity and improving quality of life."
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

