from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ConditionProfile:
    condition: str
    icd10: str
    summary: str
    hallmark_terms: tuple[str, ...] = field(default_factory=tuple)
    supporting_terms: dict[str, int] = field(default_factory=dict)
    document_terms: tuple[str, ...] = field(default_factory=tuple)
    next_steps: tuple[str, ...] = field(default_factory=tuple)
    red_flags: tuple[str, ...] = field(default_factory=tuple)


CONDITION_PROFILES: tuple[ConditionProfile, ...] = (
    ConditionProfile(
        condition="Sepsis",
        icd10="A41.9",
        summary="Systemic infection syndrome with fever, tachycardia, reduced responsiveness, and organ dysfunction risk.",
        hallmark_terms=("fever", "tachycardia", "less responsive", "weakness"),
        supporting_terms={
            "fever": 2,
            "tachycardia": 2,
            "weakness": 1,
            "fatigue": 1,
            "reduced appetite": 1,
            "less responsive": 4,
            "confusion": 3,
            "altered mental status": 4,
            "hypotension": 3,
            "sepsis": 4,
        },
        document_terms=("sepsis", "recognition", "early management"),
        next_steps=(
            "Escalate urgently for sepsis screening, full vitals, and clinician review.",
            "Obtain CBC, lactate, blood cultures, and organ-function labs promptly.",
        ),
        red_flags=("altered mental status", "reduced responsiveness", "hypotension", "tachycardia"),
    ),
    ConditionProfile(
        condition="Community-Acquired Pneumonia",
        icd10="J18.9",
        summary="Lower respiratory infection with cough, fever, chest discomfort, and shortness of breath.",
        hallmark_terms=("cough", "fever"),
        supporting_terms={
            "cough": 2,
            "productive cough": 2,
            "fever": 2,
            "shortness of breath": 2,
            "dyspnea": 2,
            "chest discomfort": 1,
            "pleuritic chest pain": 2,
            "infiltrate": 3,
            "consolidation": 3,
            "opacity": 2,
            "crackles": 2,
            "pneumonia": 4,
        },
        document_terms=("pneumonia", "respiratory", "management"),
        next_steps=(
            "Order chest imaging correlation, CBC, and inflammatory markers.",
            "Assess severity and oxygenation before deciding outpatient versus urgent treatment.",
        ),
        red_flags=("shortness of breath", "oxygen saturation drop", "respiratory distress"),
    ),
    ConditionProfile(
        condition="Viral Upper Respiratory Infection",
        icd10="J06.9",
        summary="Acute viral respiratory illness with sore throat, cough, fever, and body aches.",
        hallmark_terms=("sore throat", "cough"),
        supporting_terms={
            "sore throat": 3,
            "dry cough": 2,
            "cough": 1,
            "fever": 1,
            "body ache": 2,
            "myalgia": 2,
            "runny nose": 2,
            "nasal congestion": 2,
            "viral": 2,
        },
        next_steps=(
            "Provide supportive care advice and re-evaluate if fever or breathing worsens.",
        ),
    ),
    ConditionProfile(
        condition="Influenza-like Illness",
        icd10="J11.1",
        summary="Acute febrile viral illness with sore throat, cough, myalgias, and fatigue.",
        hallmark_terms=("fever", "body ache"),
        supporting_terms={
            "fever": 2,
            "dry cough": 2,
            "body ache": 3,
            "myalgia": 3,
            "fatigue": 1,
            "sore throat": 2,
            "headache": 2,
            "influenza": 4,
        },
        next_steps=(
            "Consider viral testing based on local protocol and symptom severity.",
        ),
    ),
    ConditionProfile(
        condition="Acute Bronchitis",
        icd10="J20.9",
        summary="Acute airway inflammation with cough, throat irritation, and mild fever.",
        hallmark_terms=("cough",),
        supporting_terms={
            "cough": 2,
            "sputum": 2,
            "sore throat": 1,
            "mild fever": 1,
            "wheeze": 1,
            "bronchitis": 4,
        },
        next_steps=(
            "Provide symptomatic respiratory care and monitor for worsening fever or dyspnea.",
        ),
    ),
    ConditionProfile(
        condition="COVID-19",
        icd10="U07.1",
        summary="Viral respiratory syndrome with fever, cough, myalgias, and lower respiratory involvement in some patients.",
        hallmark_terms=("fever", "cough"),
        supporting_terms={
            "fever": 1,
            "cough": 1,
            "shortness of breath": 2,
            "loss of smell": 3,
            "loss of taste": 3,
            "myalgia": 2,
            "body ache": 2,
            "covid": 4,
            "ground glass": 3,
        },
        next_steps=(
            "Consider respiratory viral testing and isolate if clinically indicated.",
        ),
    ),
    ConditionProfile(
        condition="Pulmonary Embolism",
        icd10="I26.99",
        summary="Acute thromboembolic disease causing pleuritic chest pain, tachycardia, hypoxia, and sudden dyspnea.",
        hallmark_terms=("pleuritic chest pain", "sudden shortness of breath"),
        supporting_terms={
            "pleuritic chest pain": 4,
            "pleuritic": 3,
            "sudden shortness of breath": 4,
            "tachycardia": 2,
            "d-dimer": 3,
            "hemoptysis": 3,
            "oxygen saturation drop": 3,
            "hypoxia": 3,
            "unilateral leg swelling": 3,
            "pulmonary embolism": 4,
        },
        next_steps=(
            "Assess hemodynamic stability and consider D-dimer plus urgent CT pulmonary angiography when appropriate.",
        ),
        red_flags=("oxygen saturation drop", "hypoxia", "tachycardia"),
    ),
    ConditionProfile(
        condition="Acute Coronary Syndrome",
        icd10="I24.9",
        summary="High-risk cardiac ischemia with new pressure-like chest pain radiating to arm, diaphoresis, and nausea.",
        hallmark_terms=("chest pain", "radiating to left arm"),
        supporting_terms={
            "new-onset chest pain": 4,
            "chest pain": 2,
            "pressure-like": 3,
            "radiating to left arm": 4,
            "left arm": 2,
            "sweating": 2,
            "diaphoresis": 2,
            "nausea": 2,
            "cardiac": 2,
            "troponin": 2,
        },
        document_terms=("chest pain", "cardiac origin", "assessment and diagnosis"),
        next_steps=(
            "Obtain ECG and serial troponin testing urgently.",
            "Escalate promptly for clinician assessment of possible acute coronary syndrome.",
        ),
        red_flags=("chest pain", "radiating to left arm", "sweating"),
    ),
    ConditionProfile(
        condition="Stable Angina",
        icd10="I20.9",
        summary="Cardiac ischemic chest discomfort that may radiate and warrants risk stratification even if not clearly acute.",
        hallmark_terms=("chest pain",),
        supporting_terms={
            "chest pain": 2,
            "pressure-like": 2,
            "cardiac": 2,
            "exertional": 3,
            "radiating": 1,
            "angina": 4,
        },
        document_terms=("chest pain", "cardiac"),
        next_steps=(
            "Risk-stratify chest pain and evaluate with ECG and clinician review.",
        ),
    ),
    ConditionProfile(
        condition="Asthma Exacerbation",
        icd10="J45.901",
        summary="Airflow obstruction flare with wheeze, chest tightness, and shortness of breath.",
        hallmark_terms=("wheeze", "shortness of breath"),
        supporting_terms={
            "wheeze": 3,
            "shortness of breath": 2,
            "chest tightness": 2,
            "tightness": 1,
            "night cough": 2,
            "bronchodilator": 2,
            "asthma": 4,
        },
        next_steps=(
            "Check peak flow and bronchodilator response; escalate if oxygenation is impaired.",
        ),
    ),
    ConditionProfile(
        condition="Acute Heart Failure",
        icd10="I50.9",
        summary="Cardiopulmonary congestion with orthopnea, edema, and breathlessness that may mimic pneumonia.",
        hallmark_terms=("orthopnea", "breathlessness"),
        supporting_terms={
            "orthopnea": 4,
            "paroxysmal nocturnal dyspnea": 4,
            "edema": 2,
            "breathlessness": 2,
            "cardiomegaly": 2,
            "pulmonary edema": 3,
            "heart failure": 4,
        },
        next_steps=(
            "Evaluate for cardiac decompensation with ECG, BNP, and imaging as available.",
        ),
        red_flags=("orthopnea", "pulmonary edema", "hypoxia"),
    ),
    ConditionProfile(
        condition="Bacterial Pharyngitis",
        icd10="J02.8",
        summary="Acute sore throat illness, potentially bacterial, without dominant lower respiratory compromise.",
        hallmark_terms=("sore throat",),
        supporting_terms={
            "sore throat": 3,
            "fever": 1,
            "tonsil": 2,
            "exudate": 3,
            "swollen lymph nodes": 2,
            "pharyngitis": 4,
        },
        next_steps=(
            "Perform focused throat examination and consider testing if bacterial features are present.",
        ),
    ),
    ConditionProfile(
        condition="Cellulitis",
        icd10="L03.90",
        summary="Skin and soft tissue infection with localized redness, warmth, swelling, and fever.",
        hallmark_terms=("redness", "swelling"),
        supporting_terms={
            "redness": 2,
            "warmth": 2,
            "swelling": 2,
            "fever": 1,
            "cellulitis": 4,
            "skin infection": 3,
        },
        next_steps=(
            "Examine the affected skin area closely and assess for systemic spread.",
        ),
    ),
    ConditionProfile(
        condition="Melanoma",
        icd10="C43.9",
        summary="Suspicious pigmented skin lesion that may need urgent dermatology assessment.",
        hallmark_terms=("skin lesion",),
        supporting_terms={
            "irregular border": 3,
            "pigmented lesion": 2,
            "changing mole": 4,
            "skin lesion": 2,
            "melanoma": 4,
            "asymmetry": 3,
        },
        next_steps=(
            "Arrange focused dermatology review and lesion assessment if malignant features are suspected.",
        ),
    ),
)
