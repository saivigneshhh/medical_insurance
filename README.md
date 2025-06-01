# HealthPay Claim Processor Backend

## Project Objective
This project implements a simplified, real-world agentic backend pipeline for processing medical insurance claim documents using AI tools and agent orchestration. It provides a FastAPI endpoint to classify documents, extract relevant data, validate it, and return a claim decision.

## Architecture & Logic

The application is structured into modular components to manage the claim processing workflow:

-   **`my_app.py`**: The main FastAPI application. It defines the `/process-claim` endpoint, which is the entry point for document uploads. It also handles loading environment variables from `.env` using `python-dotenv`.
-   **`orchestrator.py`**: Contains the `ClaimOrchestrator` class. This is the central hub that manages the overall workflow. It receives uploaded PDF files, delegates tasks to the `PDFParser` and various AI agents, aggregates their results, and constructs the final structured response.
-   **`ai_client.py`**: Provides the `OpenAIClient` (aliased as `AIClient`), which abstracts the interaction with the OpenAI API. It handles chat completions for the AI agents.
-   **`schemas.py`**: Defines all Pydantic models (data structures) used throughout the application, including input models for the API, internal data models for agents, and the final structured JSON response, adhering to the assignment's output example.
-   **`pdf_parser.py`**: Contains the `PDFParser` class responsible for extracting raw text content from uploaded PDF files using `PyPDF2`.
-   **`agents/` directory**: This package holds individual AI agents, each focused on a specific task:
    -   `document_classifier_agent.py`: Classifies the type of document (e.g., Medical Bill, Insurance Card).
    -   `data_extraction_agent.py`: Extracts structured data (e.g., patient name, billed amount) from the document text.
    -   `claim_validation_agent.py`: Validates the extracted data for consistency and completeness.

**Workflow (`/process-claim` endpoint):**
1.  Receives multiple PDF files via `multipart/form-data`.
2.  For each PDF:
    a.  Parses the PDF to extract raw text content using `pdf_parser`.
    b.  Calls the `document_classifier_agent` (LLM-based) to determine the document's type.
    c.  Calls the `data_extraction_agent` (LLM-based) to extract structured `ClaimData` into a Pydantic model.
    d.  Stores the individual document's processed results (`DocumentResult`).
3.  Aggregates relevant extracted data from all documents for overall processing.
4.  Calls the `claim_validation_agent` (LLM-based) to perform an overall check on the aggregated data.
5.  Constructs a final JSON response conforming to the specified `ClaimProcessingResponse` schema, including details for each processed document, overall validation status, and a claim decision.

## Tech Requirements Met
-   FastAPI backend using `async` where appropriate.
-   Custom agent orchestration logic (`orchestrator.py`).
-   LLMs (via OpenAI API) used for classification, extraction, and validation.
-   File upload support (`multipart/form-data`).
-   Modular, clean, and organized Python code.

## Setup and Run Instructions

1.  **Clone/Download the repository:**
    * Ensure the directory structure matches the one described above.

2.  **Navigate to the project root:**
    ```bash
    cd C:\healthcare
    ```

3.  **Create a Python Virtual Environment (if you haven't already):**
    ```bash
    python -m venv venv
    ```

4.  **Activate the Virtual Environment:**
    ```bash
    .\venv\Scripts\activate
    ```
    (You should see `(venv)` at the beginning of your command prompt.)

5.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Or manually install: `pip install fastapi uvicorn pydantic python-multipart PyPDF2 openai python-dotenv`)

6.  **Set your OpenAI API Key:**
    * Obtain a **secret key with "All" permissions** from [OpenAI Platform](https://platform.openai.com/account/api-keys).
    * In your `C:\healthcare` directory, create a new file named `.env` (note the leading dot).
    * Add your key to this `.env` file in the format:
        ```
        OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```
        (Replace `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your actual key. Do NOT use quotes unless your key contains spaces.)

7.  **Run the FastAPI Application:**
    ```bash
    uvicorn my_app:app --reload
    ```

8.  **Access the API Documentation:**
    * Open your web browser and go to: `http://127.0.0.1:8000/docs`
    * You can use the interactive Swagger UI to test the `/process-claim` endpoint by uploading PDF files.

## AI Tool Usage (Mandatory)

I heavily utilized AI tools throughout this assignment to accelerate development, ensure correctness, and aid in debugging.

-   **[Your Primary LLM Tool, e.g., Google Gemini / ChatGPT / Claude]**:
    * **Code Scaffolding**: I frequently prompted [Tool Name] to generate initial boilerplate code for FastAPI endpoints, Pydantic models, and the basic structure of the AI client and agent functions. This saved significant time in setting up file structures and common patterns.
    * **Debugging**: When encountering `SyntaxError`, `ImportError`, or runtime exceptions, I copied the full traceback and asked [Tool Name] for explanations and solutions. For example, [**Provide a specific example prompt and how it helped you debug, like the `Attribute 'app' not found` or the indentation error.**]
    * **Prompt Design**: I iterated with [Tool Name] to refine the system and user prompts for the AI agents (classification, extraction, validation) to ensure they returned responses in the expected JSON format and handled edge cases effectively.
    * **Architectural Guidance**: [Tool Name] helped in discussing design choices, such as the best way to structure the agent orchestration and pass data between different steps.

-   **[Your AI Coding Assistant, e.g., Cursor.ai / VS Code's Copilot / Other IDE AI Feature]**:
    * **Code Completion & Generation**: Used [Tool Name] for intelligent code completion, generating entire function bodies, and suggesting variable names, which significantly sped up coding.
    * **Syntax Correction**: Helped in quickly identifying and fixing minor syntax errors as I typed.

### Actual Prompt Examples Used:

1.  **Initial FastAPI Project Structure:**
    ```
    "Generate a Python FastAPI application structure for processing medical claim documents using multiple AI agents (classification, extraction, validation). The main endpoint should accept PDF files and return structured JSON. Include placeholder files for orchestrator, agents, and schemas."
    ```
    *How it helped:* Provided the foundational `my_app.py`, `orchestrator.py`, `ai_client.py` structure, saving initial setup time.

2.  **Debugging an Import Error:**
    ```
    "I'm encountering an `ImportError: cannot import name 'ClaimOrchestrator' from 'orchestrator' (C:\\healthcare\\orchestrator.py)` when running my FastAPI app. My orchestrator.py definitely has the class defined. What are common reasons for this error in a multi-file Python project on Windows, and how can I resolve it?"
    ```
    *How it helped:* Led to checking for `__pycache__` issues, verifying file content, and ultimately resolving the persistent file reading problem after multiple attempts.

3.  **Refining Schema for AI Extraction:**
    ```
    "I need a Pydantic BaseModel for medical claim data extraction by an LLM. The fields should include claim_id, patient_name, patient_dob (YYYY-MM-DD), insurance_provider, policy_number, service_date (YYYY-MM-DD), service_description, billed_amount (float), diagnosis_code, procedure_code, and provider_name. Generate the Pydantic class and an example JSON output."
    ```
    *How it helped:* Provided the `ClaimData` schema, which was then directly used in `schemas.py` and referenced in the `data_extraction_agent`'s system prompt for strict JSON output.

---
[Optional: Add a link to your 2-3 min Loom/video explanation here if you create one]
[Optional: Add sections for Dockerfile, Redis/PostgreSQL setup, or Vector Store usage if you implement them]
[Optional: Add a section "Failures & Tradeoffs" to discuss any challenges and decisions made during development]


## AI Tool Usage (Mandatory)

I heavily utilized AI tools throughout this assignment to accelerate development, ensure correctness, and aid in debugging.

-   **Google Gemini (Primary LLM Tool)**:
    * **Code Scaffolding**: I frequently prompted Gemini to generate initial boilerplate code for FastAPI endpoints, Pydantic models, and the basic structure of the AI client and agent functions (`document_classifier_agent.py`, `data_extraction_agent.py`). This significantly sped up the initial setup and ensured adherence to common Python/FastAPI patterns.
    * **Debugging**: When encountering various `ImportError` (e.g., `PDFParser`, `ClaimDecision`, `OpenAIClient` not found) or `SyntaxError` (like the stray 'S' in `pdf_parser.py`), I copied the full traceback and relevant code snippets. I asked Gemini to "Explain this Python error and suggest a fix, considering my project structure" or "Why is this `SyntaxError` occurring on this line?" This helped me quickly identify the root cause (missing imports, typos, environment variable issues) and apply the correct patches.
    * **Prompt Design & Refinement**: I iterated with Gemini to refine the system and user prompts for the AI agents (classification, extraction, validation) to ensure they returned responses in the expected JSON format and handled missing information gracefully. For instance, specifically asking for JSON output conforming to the `ClaimData` schema.
    * **Architectural Guidance**: Discussed with Gemini the best way to structure the agent orchestration (`orchestrator.py`) to manage multiple agents and handle document flows.

-   **VS Code's Built-in AI Features / Cursor.ai (AI Coding Assistant)**:
    * **Code Completion & Generation**: Used the IDE's integrated AI for intelligent code completion, suggesting variable names, and generating small code blocks based on context. This streamlined the coding process.
    * **Syntax Correction**: Helped in quickly identifying and fixing minor syntax errors or formatting issues as I typed, improving code quality on the fly.

### Actual Prompt Examples Used:

1.  **Initial FastAPI Backend Structure & Agent Logic:**
    ```
    "Design a Python FastAPI application structure for processing medical insurance claim documents. The main endpoint should accept multiple PDF file uploads. Outline the classes and methods needed for:
    - PDF parsing
    - Document classification (agent)
    - Data extraction (agent)
    - Claim validation (agent)
    - An orchestrator to manage the flow.
    Provide placeholder code for `my_app.py`, `orchestrator.py`, `ai_client.py`, `schemas.py`, `pdf_parser.py`, and an `agents` directory with example agent files. Ensure async operations where appropriate."
    ```
    *How it helped:* This comprehensive prompt was crucial for quickly scaffolding the entire project, defining the initial modules (`my_app`, `orchestrator`, `ai_client`, `pdf_parser`, `schemas`, `agents`), and outlining the core classes and their responsibilities, saving a significant amount of initial setup time.

2.  **Debugging `ValueError: OPENAI_API_KEY environment variable not set.`:**
    ```
    "I'm running a FastAPI application with `uvicorn my_app:app --reload` on Windows. My `ai_client.py` uses `os.getenv('OPENAI_API_KEY')`. I've set the environment variable in my command prompt using `set OPENAI_API_KEY=sk-YOUR_KEY`. However, I keep getting the `ValueError: OPENAI_API_KEY environment variable not set.` What could be wrong? Could it be my virtual environment, or how Windows handles `set` for subprocesses? Provide troubleshooting steps."
    ```
    *How it helped:* This prompt led to a deeper understanding of environment variable persistence across sessions and processes on Windows. It guided me to verify the variable using `echo %OPENAI_API_KEY%` and ultimately led to implementing the more robust `python-dotenv` solution in `my_app.py` to ensure the key was loaded reliably.

3.  **Refining Pydantic Schema for LLM Output and Orchestrator Adjustment:**
    ```
    "I need a Pydantic BaseModel to represent the final JSON output of my medical claim processor, matching this exact structure:
    ```json
    {
      "documents": [
        {
          "type": "bill",
          "hospital_name": "ABC Hospital",
          "total_amount": 12500,
          "date_of_service": "2024-04-10"
        },
        {
          "type": "discharge_summary",
          "patient_name": "John Doe",
          "diagnosis": "Fracture",
          "admission_date": "2024-04-01",
          "discharge_date": "2024-04-10"
        }
      ],
      "validation": {
        "missing_documents": [],
        "discrepancies": []
      },
      "claim_decision": {
        "status": "approved",
        "reason": "All required documents present and data is consistent"
      }
    }
    ```
    Generate the necessary Pydantic classes (`DocumentResult`, `ValidationResult`, `ClaimDecisionDetails`, `ClaimProcessingResponse`) and explain how `orchestrator.py` should be modified to construct an instance of `ClaimProcessingResponse` by processing individual documents and aggregating results."
    ```
    *How it helped:* This prompt directly provided the complex nested Pydantic schemas required to match the assignment's exact output format. It also gave crucial guidance on how to adapt the `orchestrator.py` logic to iterate through documents, populate `DocumentResult` for each, and then aggregate into the `validation` and `claim_decision` fields, ensuring the final output conformed to the specification.
