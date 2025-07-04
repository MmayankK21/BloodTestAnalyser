import traceback
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import verification, help_patients, nutrition_analysis, exercise_planning
from custom_crew import CustomCrew

app = FastAPI(title="Blood Test Report Analyser")

def run_crew(query: str, file_path: str):
    """Run the crew with the given query and file path"""
    try:
        medical_crew = CustomCrew(
            agents=[doctor, verifier, nutritionist, exercise_specialist],
            tasks=[verification, help_patients, nutrition_analysis, exercise_planning]
        )
        inputs = {
            'query': query,
            'file_path': file_path
        }
        return medical_crew.kickoff(inputs)
    except Exception as e:
        traceback.print_exc()
        return f"Crew execution failed: {str(e)}"


@app.get("/")
async def root():
    return {"message": "Blood Test Report Analyser API is running"}


@app.post("/analyze")
async def analyze_blood_report(
        file: UploadFile = File(...),
        query: str = Form("Analyze my Blood Test Report")
):
    # Generate a unique file name
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"

    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are accepted")

        # Run the crew
        response = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "query": query,
            "analysis": response,
            "file_processed": file.filename
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    finally:
        # Clean up the file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )