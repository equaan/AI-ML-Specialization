from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any

import httpx

from backend.config import get_settings


EUTILS_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


@dataclass
class PubMedArticle:
    pmid: str
    title: str
    abstract: str
    url: str


class PubMedTool:
    def __init__(self, max_requests_per_second: float = 3.0) -> None:
        self.settings = get_settings()
        self.min_interval = 1.0 / max_requests_per_second
        self._last_request_ts = 0.0

    def search(self, query: str, max_results: int = 5) -> list[PubMedArticle]:
        if not query.strip():
            return []

        id_list = self._esearch(query, max_results=max_results)
        if not id_list:
            return []
        return self._efetch(id_list)

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_ts
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_request_ts = time.monotonic()

    def _request(self, endpoint: str, params: dict[str, Any]) -> str:
        self._throttle()
        with httpx.Client(timeout=20.0) as client:
            response = client.get(f"{EUTILS_BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.text

    def _esearch(self, query: str, max_results: int) -> list[str]:
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": str(max_results),
            "retmode": "json",
        }
        if self.settings.pubmed_api_key:
            params["api_key"] = self.settings.pubmed_api_key

        payload = self._request("esearch.fcgi", params)
        data = httpx.Response(200, text=payload).json()
        return data.get("esearchresult", {}).get("idlist", [])

    def _efetch(self, id_list: list[str]) -> list[PubMedArticle]:
        params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "xml",
        }
        if self.settings.pubmed_api_key:
            params["api_key"] = self.settings.pubmed_api_key

        xml_text = self._request("efetch.fcgi", params)
        return self._parse_efetch_response(xml_text)

    def _parse_efetch_response(self, xml_text: str) -> list[PubMedArticle]:
        root = ET.fromstring(xml_text)
        articles: list[PubMedArticle] = []

        for article in root.findall(".//PubmedArticle"):
            pmid = (article.findtext(".//PMID") or "").strip()
            title = " ".join(article.findtext(".//ArticleTitle", default="").split())
            abstract_parts = [
                " ".join((elem.text or "").split())
                for elem in article.findall(".//Abstract/AbstractText")
                if (elem.text or "").strip()
            ]
            abstract = " ".join(abstract_parts)
            if not pmid or not title:
                continue
            articles.append(
                PubMedArticle(
                    pmid=pmid,
                    title=title,
                    abstract=abstract,
                    url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                )
            )

        return articles
