import requests
import os

# Configuration
API_URL = "http://localhost:8000/analyze"
PDF_PATH = r"C:\Users\MAYANK\Downloads\blood-test-analyser-debug\data\sample.pdf"
QUERY = "Please analyze my blood test report"


def test_api():
    print("Testing Blood Test Analysis API...")
    print(f"Using sample PDF: {PDF_PATH}")

    if not os.path.exists(PDF_PATH):
        print("Error: Sample PDF file not found.")
        return

    try:
        with open(PDF_PATH, "rb") as f:
            files = {"file": (os.path.basename(PDF_PATH), f, "application/pdf")}
            data = {"query": QUERY}
            response = requests.post(API_URL, files=files, data=data)

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            print(response.json())
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Test failed: {str(e)}")


if __name__ == "__main__":
    test_api()