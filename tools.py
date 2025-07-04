from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader
from typing import Type
from pydantic import BaseModel, Field


class BloodTestReportInput(BaseModel):
    path: str = Field(..., description="Path to the PDF file")


class BloodTestReportTool(BaseTool):
    name: str = "Blood Test Report Reader"
    description: str = "Reads data from a PDF blood test report file"
    args_schema: Type[BaseModel] = BloodTestReportInput

    def _run(self, path: str) -> str:
        try:
            loader = PyPDFLoader(file_path=path)
            docs = loader.load()
            full_report = "\n".join([doc.page_content for doc in docs])
            return full_report
        except Exception as e:
            return f"Error reading PDF: {str(e)}"


# Create tool instance
blood_test_report_reader = BloodTestReportTool()