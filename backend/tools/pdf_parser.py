from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import fitz
import pytesseract
from PIL import Image

from backend.models.schemas import LabPatientInfo, LabReport, LabTestResult


@dataclass
class ParsedPdfPage:
    page_number: int
    text: str


class PDFParser:
    def extract_text(self, pdf_path: str | Path) -> str:
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")

        pages: list[ParsedPdfPage] = []
        with fitz.open(path) as document:
            for page_index, page in enumerate(document, start=1):
                text = page.get_text("text").strip()
                if not text:
                    text = self._ocr_page(page)
                pages.append(ParsedPdfPage(page_number=page_index, text=text))

        return "\n\n".join(page.text for page in pages if page.text)

    def parse_lab_report(self, pdf_path: str | Path) -> LabReport:
        raw_text = self.extract_text(pdf_path)
        return self.parse_lab_report_text(raw_text, source_name=Path(pdf_path).name)

    def parse_lab_report_text(self, raw_text: str, source_name: str | None = None) -> LabReport:
        cleaned_text = self._normalize_whitespace(raw_text)
        document_kind = self._classify_document(cleaned_text, source_name=source_name)
        patient_info = self._extract_patient_info(cleaned_text)
        test_results = self._extract_test_results(cleaned_text) if document_kind == "lab" else []
        report_type = self._infer_report_type(cleaned_text, test_results, document_kind=document_kind)
        critical_values = [result.test_name for result in test_results if result.flag == "CRITICAL"]

        return LabReport(
            report_type=report_type,
            patient_info=patient_info,
            test_results=test_results,
            clinical_summary=cleaned_text[:1000],
            critical_values=critical_values,
        )

    def build_context_summary(self, raw_text: str, source_name: str | None = None) -> str:
        cleaned_text = self._normalize_whitespace(raw_text)
        document_kind = self._classify_document(cleaned_text, source_name=source_name)
        title = self._extract_document_title(cleaned_text, source_name=source_name)

        if document_kind == "guideline":
            snippets = self._select_relevant_lines(
                cleaned_text,
                keywords=("diagnosis", "management", "recognition", "assessment", "treatment", "urgent"),
                limit=5,
            )
            body = " ".join(snippets) if snippets else cleaned_text[:600]
            return f"Guideline context: {title}. {body[:900]}"

        if document_kind == "lab":
            report = self.parse_lab_report_text(cleaned_text, source_name=source_name)
            if not report.test_results:
                return f"Lab report context: {title}."
            top_results = ", ".join(
                f"{item.test_name}={item.value}{f' ({item.flag})' if item.flag else ''}"
                for item in report.test_results[:6]
            )
            return f"Lab report context: {title}. Key findings: {top_results}."

        snippets = self._select_relevant_lines(
            cleaned_text,
            keywords=("pain", "fever", "cough", "dyspnea", "shortness of breath", "diagnosis", "assessment"),
            limit=4,
        )
        body = " ".join(snippets) if snippets else cleaned_text[:600]
        return f"Clinical document context: {title}. {body[:900]}"

    def _ocr_page(self, page: fitz.Page) -> str:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return pytesseract.image_to_string(image).strip()

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        text = text.replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _extract_patient_info(self, text: str) -> LabPatientInfo:
        return LabPatientInfo(
            name=self._search_group(text, r"(?:patient name|name)\s*[:\-]\s*([A-Za-z .]+)"),
            age=self._search_group(text, r"(?:age)\s*[:\-]\s*([0-9]{1,3})"),
            gender=self._search_group(text, r"(?:gender|sex)\s*[:\-]\s*(male|female|other)"),
            date=self._search_group(text, r"(?:date|collection date|reported on)\s*[:\-]\s*([0-9/\-]{6,20})"),
        )

    def _extract_test_results(self, text: str) -> list[LabTestResult]:
        results: list[LabTestResult] = []
        pattern = re.compile(
            r"(?P<name>[A-Za-z][A-Za-z0-9 /()%+-]{1,80})\s+"
            r"(?P<value>[<>]?\s?[0-9]+(?:\.[0-9]+)?(?:\s?[A-Za-z/%^0-9.-]+)?)\s+"
            r"(?P<range>[0-9.<>\- ]+(?:to)?[0-9.<>\- ]*[A-Za-z/%^0-9.-]*)?",
            re.IGNORECASE,
        )

        for match in pattern.finditer(text):
            test_name = match.group("name").strip(" :-")
            value = match.group("value").strip()
            range_match = match.group("range")
            reference_range = range_match.strip() if range_match else None
            flag = self._infer_flag(value, reference_range, text, test_name)
            results.append(
                LabTestResult(
                    test_name=test_name,
                    value=value,
                    reference_range=reference_range,
                    flag=flag,
                )
            )

        return self._deduplicate_results(results)

    def _infer_report_type(
        self,
        text: str,
        test_results: list[LabTestResult],
        document_kind: str = "unknown",
    ) -> str:
        lower_text = text.lower()
        if document_kind == "guideline":
            return "Guideline Document"
        if document_kind == "clinical_document":
            return "Clinical Document"
        if "hemoglobin" in lower_text or "wbc" in lower_text or "platelet" in lower_text:
            return "CBC"
        if "bilirubin" in lower_text or "sgot" in lower_text or "sgpt" in lower_text:
            return "LFT"
        if "creatinine" in lower_text or "urea" in lower_text:
            return "KFT"
        if "triglyceride" in lower_text or "hdl" in lower_text or "ldl" in lower_text:
            return "Lipid Panel"
        if "tsh" in lower_text or "t3" in lower_text or "t4" in lower_text:
            return "Thyroid"
        if test_results:
            return "General Lab Report"
        return "Unknown"

    def _classify_document(self, text: str, source_name: str | None = None) -> str:
        lower_text = text.lower()
        lower_name = (source_name or "").lower()

        guideline_markers = (
            "nice guideline",
            "clinical guideline",
            "guideline",
            "diagnosis and management",
            "assessment and diagnosis",
            "recognition, diagnosis",
        )
        if any(marker in lower_text[:1500] or marker in lower_name for marker in guideline_markers):
            return "guideline"

        lab_markers = (
            "patient name",
            "hemoglobin",
            "haemoglobin",
            "glucose",
            "platelet",
            "wbc",
            "rbc",
            "bilirubin",
            "creatinine",
            "reference range",
            "normal range",
            "specimen",
        )
        lab_score = sum(1 for marker in lab_markers if marker in lower_text)
        if lab_score >= 2 or re.search(r"[a-z][a-z0-9 ,()/+-]{2,}\s+[<>]?\s?\d+(?:\.\d+)?\s*[a-z/%]+", lower_text):
            return "lab"

        clinical_markers = (
            "history of present illness",
            "chief complaint",
            "impression",
            "assessment",
            "plan",
        )
        if any(marker in lower_text for marker in clinical_markers):
            return "clinical_document"

        return "unknown"

    @staticmethod
    def _extract_document_title(text: str, source_name: str | None = None) -> str:
        for line in text.splitlines():
            normalized = " ".join(line.split())
            if len(normalized) >= 8 and len(normalized) <= 140:
                return normalized
        if source_name:
            return Path(source_name).stem.replace("-", " ")
        return "Uploaded medical document"

    @staticmethod
    def _select_relevant_lines(text: str, keywords: Iterable[str], limit: int = 5) -> list[str]:
        matches: list[str] = []
        for line in text.splitlines():
            compact = " ".join(line.split())
            if len(compact) < 20:
                continue
            lower = compact.lower()
            if any(keyword in lower for keyword in keywords):
                matches.append(compact)
            if len(matches) >= limit:
                break
        return matches

    def _infer_flag(self, value: str, reference_range: str | None, text: str, test_name: str) -> str | None:
        line = self._find_line_for_test(text, test_name)
        upper_line = line.upper()
        if "CRITICAL" in upper_line:
            return "CRITICAL"
        if "HIGH" in upper_line or " H " in upper_line:
            return "HIGH"
        if "LOW" in upper_line or " L " in upper_line:
            return "LOW"
        if reference_range:
            numeric_value = self._extract_first_number(value)
            bounds = self._extract_bounds(reference_range)
            if numeric_value is not None and bounds:
                lower, upper = bounds
                if numeric_value < lower:
                    return "LOW"
                if numeric_value > upper:
                    return "HIGH"
                return "NORMAL"
        return None

    @staticmethod
    def _search_group(text: str, pattern: str) -> str | None:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        return match.group(1).strip() if match else None

    @staticmethod
    def _find_line_for_test(text: str, test_name: str) -> str:
        for line in text.splitlines():
            if test_name.lower() in line.lower():
                return line
        return ""

    @staticmethod
    def _extract_first_number(text: str) -> float | None:
        match = re.search(r"[<>]?\s*([0-9]+(?:\.[0-9]+)?)", text)
        return float(match.group(1)) if match else None

    @staticmethod
    def _extract_bounds(text: str) -> tuple[float, float] | None:
        values = re.findall(r"[0-9]+(?:\.[0-9]+)?", text)
        if len(values) < 2:
            return None
        return float(values[0]), float(values[1])

    @staticmethod
    def _deduplicate_results(results: list[LabTestResult]) -> list[LabTestResult]:
        deduplicated: dict[str, LabTestResult] = {}
        for result in results:
            key = result.test_name.lower()
            deduplicated[key] = result
        return list(deduplicated.values())
