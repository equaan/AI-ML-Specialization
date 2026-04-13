from backend.tools.pdf_parser import PDFParser


def test_parse_lab_report_text_extracts_report_type_and_results() -> None:
    parser = PDFParser()
    raw_text = """
    Patient Name: Jonathan Doe
    Age: 39
    Gender: Male
    Date: 2024-09-24

    Hemoglobin 14.2 g/dL 13.5 - 17.5
    Glucose, Fasting 126 mg/dL 70 - 99 HIGH
    Potassium 4.1 mmol/L 3.5 - 5.1
    """

    report = parser.parse_lab_report_text(raw_text)

    assert report.report_type in {"General Lab Report", "Unknown", "CBC"}
    assert report.patient_info.name == "Jonathan Doe"
    assert len(report.test_results) >= 2


def test_parse_lab_report_text_marks_high_values() -> None:
    parser = PDFParser()
    raw_text = "Glucose 126 mg/dL 70 - 99 HIGH"
    report = parser.parse_lab_report_text(raw_text)

    assert report.test_results[0].flag in {"HIGH", "CRITICAL"}
