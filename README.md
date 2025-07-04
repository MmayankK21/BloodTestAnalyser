```markdown
# Blood Test Report Analysis System

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)](https://fastapi.tiangolo.com/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.13.0-orange.svg)](https://www.crewai.com/)

## Bugs Found and Fixes

### Critical Architecture Issues
1. **Undefined LLM Variable**  
   - **Problem**: `llm = llm` caused immediate failure
   - **Fix**: Implemented custom execution flow bypassing CrewAI's LLM system
   - **Files Changed**: `custom_crew.py`, `main.py`

2. **CrewAI Internal Conflicts**  
   - **Problem**: "LLM Provider NOT provided" errors
   - **Fix**: Complete bypass of CrewAI's LiteLLM integration
   - **Files Changed**: `custom_crew.py`

3. **Tool Implementation Flaws**  
   - **Problem**: Missing tool decorator and PDFLoader imports
   - **Fix**: Proper BaseTool implementation with content normalization
   - **Files Changed**: `tools.py`
   ```python
   # Before
   class BloodTestReportTool():  # No base class
   
   # After
   class BloodTestReportTool(BaseTool):  # Proper inheritance
       def _run(self, path: str) -> str:
           # Added content cleaning
           content = re.sub(r'\n{3,}', '\n\n', content)
   ```

### Agent & Task System Defects
4. **Single Agent Overload**  
   - **Problem**: Doctor agent handling all tasks
   - **Fix**: Specialized task assignments
   - **Files Changed**: `task.py`
   ```python
   # Before
   help_patients = Task(agent=doctor)
   nutrition_analysis = Task(agent=doctor)  # Wrong assignment
   
   # After
   verification = Task(agent=verifier)  # Correct specialist
   nutrition_analysis = Task(agent=nutritionist)
   ```

5. **Unprofessional Personas**  
   - **Problem**: Agents encouraged misinformation
   - **Fix**: Evidence-based professional profiles
   - **Files Changed**: `agents.py`
   ```python
   # Before
   "You love to diagnose rare diseases from simple symptoms"
   
   # After
   "You are an experienced doctor with 20+ years in clinical practice"
   ```

### File Processing Problems
6. **Temporary File Accumulation**  
   - **Problem**: Files remained after processing
   - **Fix**: UUID-based storage with guaranteed cleanup
   - **Files Changed**: `main.py`
   ```python
   finally:
       if os.path.exists(file_path):
           os.remove(file_path)  # Guaranteed cleanup
   ```

7. **Missing File Validation**  
   - **Problem**: Non-PDF files caused crashes
   - **Fix**: Added strict file type validation
   - **Files Changed**: `main.py`
   ```python
   if not file.filename.lower().endswith('.pdf'):
       raise HTTPException(400, "Only PDF files accepted")
   ```

### API & Execution Flaws
8. **Inconsistent Variable Formatting**  
   - **Problem**: Prompt formatting mismatches
   - **Fix**: Unified input handling
   - **Files Changed**: `custom_crew.py`

9. **Resource Management Gaps**  
   - **Problem**: Potential infinite loops
   - **Fix**: Added execution constraints
   - **Files Changed**: `agents.py`
   ```python
   max_iter=5,  # Prevent infinite loops
   max_rpm=10   # Rate limiting
   ```

## Setup and Usage Instructions

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed (for local LLMs)
- API key for cloud LLMs (OpenAI/Anthropic)

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/blood-test-analysis.git
cd blood-test-analysis

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
```

### Configuration (.env file)
```ini
# Choose one LLM provider:
LLM_TYPE=ollama       # Options: openai|anthropic|ollama
OLLAMA_MODEL=llama3   # Local model name

# For cloud providers (uncomment and fill):
# OPENAI_API_KEY=your_api_key_here
# OPENAI_MODEL=gpt-4-turbo
# ANTHROPIC_API_KEY=your_api_key_here
```

### Running the Application
```bash
# Start local LLM service (in separate terminal)
ollama serve

# Start API server
uvicorn main:app --reload --port 8000
```

### Testing the System
1. Create a test PDF file in the repository root
2. Use the test script:
```bash
python tests/test_api.py
```

## API Documentation

### Base URL
`http://localhost:8000`

### Endpoints

#### POST /analyze
Analyzes blood test reports and provides health recommendations

**URL:** `http://localhost:8000/analyze`

**Method:** `POST`

**Form Data:**
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `file` | File | PDF blood test report | Yes |
| `query` | String | Analysis request | No |

**Success Response:**
```json
{
  "status": "success",
  "query": "User's original query",
  "analysis": "Multipart analysis report",
  "file_processed": "original_filename.pdf"
}
```

**Error Response:**
```json
{
  "detail": "Error message describing the issue"
}
```

**Example Request using curl:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@blood_test.pdf" \
  -F "query='Analyze my cholesterol levels'"
```

**Example Response:**
```json
{
  "status": "success",
  "query": "Analyze my cholesterol levels",
  "analysis": "## Senior Doctor\nLDL cholesterol levels at 150 mg/dL...",
  "file_processed": "blood_test.pdf"
}
```

### Common Status Codes
| Code | Description |
|------|-------------|
| 200 | Successful analysis |
| 400 | Invalid file type or missing file |
| 500 | Internal server error |

## Agent Reference

| Agent | Inputs | Outputs | Tools |
|-------|--------|---------|-------|
| **Senior Doctor** | Blood report PDF, User query | Medical analysis | BloodTestReportTool |
| **Report Verifier** | Blood report PDF | Verification status | BloodTestReportTool |
| **Nutritionist** | Blood report data | Nutrition plan | BloodTestReportTool |
| **Exercise Specialist** | Blood report data | Exercise program | BloodTestReportTool |

## Troubleshooting
- **LLM Connection Issues**: Verify Ollama is running (`ollama serve`)
- **PDF Processing Errors**: Ensure files are valid PDFs
- **Module Not Found**: Run `pip install -r requirements.txt`
- **Rate Limiting Errors**: Increase `max_rpm` in agent definitions

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
```
