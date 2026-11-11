# Resume RAG Job Matching System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) based resume matching system that retrieves and ranks candidate resumes against job descriptions.

The system processes resumes, preserves important resume sections, generates semantic embeddings, stores them in a ChromaDB vector database, and retrieves candidates using semantic search.

Candidate ranking combines semantic similarity, explicit skill matching, experience requirements, and must-have filtering.

---

## Learning Objectives

This project demonstrates:

- Document processing and intelligent chunking
- Semantic embeddings
- Vector databases
- Semantic search
- Hybrid semantic and keyword matching
- Metadata extraction
- Candidate filtering and ranking
- Retrieval evaluation
- Performance measurement

---

## Technology Stack

- Python
- Sentence Transformers / Hugging Face
- ChromaDB
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook
- VS Code

Embedding model:

`all-MiniLM-L6-v2`

---

## Project Structure

```text
resume-rag-project/
│
├── job_descriptions/
│   ├── data_scientist.txt
│   ├── devops_engineer.txt
│   ├── java_developer.txt
│   ├── ml_engineer.txt
│   └── python_developer.txt
│
├── notebooks/
│   └── rag_experiments.ipynb
│
├── results/
│   ├── data_scientist_results.json
│   ├── devops_engineer_results.json
│   ├── java_developer_results.json
│   ├── ml_engineer_results.json
│   └── python_developer_results.json
│
├── resumes/
│   └── 30 synthetic resumes
│
├── fs_tools.py
├── generate_dataset.py
├── job_matcher.py
├── resume_rag.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## System Architecture

```text
Resume Files
     ↓
File System Tools
     ↓
Text Extraction
     ↓
Section Detection
     ↓
Section-Aware Chunking
     ↓
Metadata Extraction
     ↓
Sentence Transformer Embeddings
     ↓
ChromaDB Vector Database
     ↓
Semantic Retrieval
     ↓
Candidate Grouping
     ↓
Hybrid Matching
     ↓
Must-Have Filtering
     ↓
Candidate Ranking
     ↓
Top Matches
     ↓
JSON Results
```

---

## Part A — RAG System

### Document Processing

Resumes are loaded using the file-system tools implemented in Milestone 1.

Supported resume formats include:

- TXT
- PDF
- DOCX

The document processing pipeline identifies important resume sections such as:

- Professional Summary
- Skills
- Experience
- Education
- Projects
- Certifications

The resume is chunked while preserving these logical sections instead of splitting the document arbitrarily.

### Embeddings

The project uses the Sentence Transformers model:

`all-MiniLM-L6-v2`

Each resume chunk is converted into a semantic embedding.

### Vector Database

Embeddings are stored in ChromaDB along with metadata including:

- Candidate name
- Resume path
- Resume section
- Skills
- Years of experience
- Education

---

## Part B — Job Matching Engine

### Semantic Search

A job description is converted into an embedding using the same Sentence Transformer model.

ChromaDB retrieves semantically relevant resume chunks.

Retrieved chunks are grouped by candidate before candidate-level scoring.

### Hybrid Search

Candidate matching combines:

- Semantic similarity
- Explicit skill matching
- Experience matching

The scoring weights are:

```text
Semantic similarity: 60%
Skill matching:      25%
Experience:          15%
```

The final score is represented on a 0–100 scale.

### Must-Have Filtering

Required skills and minimum experience are extracted from the job description.

Candidates who do not satisfy mandatory requirements are excluded from the final qualified results.

The system also reports missing requirements to make rejection decisions explainable.

### Match Reasoning

Each candidate result includes reasoning describing:

- Matched skills
- Experience requirement status
- Missing must-have skills
- Overall requirement satisfaction

---

## Dataset

The project contains 30 diverse synthetic resumes covering roles including:

- Python Developer
- Java Developer
- Data Scientist
- Machine Learning Engineer
- DevOps Engineer
- Cloud Engineer
- Data Engineer
- Backend Developer
- Frontend Developer
- Full Stack Developer
- QA Automation Engineer
- Business Analyst
- Cybersecurity Engineer
- Database Engineer

The dataset is synthetic and intended only for experimentation and educational evaluation.

---

## Job Descriptions

Five job descriptions are included:

1. Python Developer
2. Data Scientist
3. DevOps Engineer
4. Java Developer
5. Machine Learning Engineer

---

## Installation

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Generate the Synthetic Dataset

Run:

```bash
python generate_dataset.py
```

This generates the synthetic resume dataset inside the `resumes` directory.

---

## Build the Vector Database

Run:

```bash
python resume_rag.py
```

This:

1. Reads all resumes.
2. Extracts resume sections.
3. Creates section-aware chunks.
4. Extracts candidate metadata.
5. Generates embeddings.
6. Stores the embeddings and metadata in ChromaDB.

---

## Run Job Matching

Example:

```bash
python job_matcher.py job_descriptions/python_developer.txt
```

Other examples:

```bash
python job_matcher.py job_descriptions/data_scientist.txt
python job_matcher.py job_descriptions/devops_engineer.txt
python job_matcher.py job_descriptions/java_developer.txt
python job_matcher.py job_descriptions/ml_engineer.txt
```

Results are saved under the `results` directory.

---

## Output Format

Example:

```json
{
  "job_description": "...",
  "top_matches": [
    {
      "candidate_name": "John Doe",
      "resume_path": "resumes/john_doe.txt",
      "match_score": 67.74,
      "matched_skills": [
        "Python",
        "FastAPI",
        "SQL",
        "AWS",
        "Docker"
      ],
      "relevant_excerpts": [
        "Relevant resume content..."
      ],
      "reasoning": "Candidate matches the required skills and experience."
    }
  ]
}
```

---

## Experimentation

The experimentation notebook is located at:

`notebooks/rag_experiments.ipynb`

The notebook evaluates:

- Candidate retrieval results
- Precision@10
- Recall@10
- Retrieval latency
- Average retrieval latency
- Performance across multiple job descriptions

It also includes visualizations for retrieval quality and latency.

---

## Evaluation Metrics

### Precision@10

Precision@10 measures the proportion of retrieved candidates that are relevant.

```text
Precision@10 =
Relevant Retrieved Candidates / Retrieved Candidates
```

### Recall@10

Recall@10 measures how many expected relevant candidates were successfully retrieved.

```text
Recall@10 =
Relevant Retrieved Candidates / Total Relevant Candidates
```

### Latency

Retrieval latency measures the time required to:

1. Generate the job-description embedding.
2. Query ChromaDB.
3. Retrieve relevant resume chunks.

Actual results are available in the executed Jupyter notebook.

---

## Key Features

- Section-aware resume chunking
- Local semantic embeddings
- Persistent ChromaDB vector storage
- Resume metadata extraction
- Semantic search
- Keyword skill matching
- Hybrid ranking
- Must-have requirement filtering
- Explainable candidate matching
- Top-K candidate retrieval
- JSON result generation
- Retrieval accuracy evaluation
- Latency measurement

---

## Limitations

- The evaluation dataset is synthetic.
- Metadata extraction assumes reasonably structured resume headings.
- Skill extraction uses a predefined technical-skill vocabulary.
- Complex real-world PDF and DOCX layouts may require stronger document parsing.
- The experimental implementation retrieves a broad chunk pool before candidate-level ranking and would require optimization for production-scale datasets.

---

## Future Improvements

Possible improvements include:

- LLM-based metadata extraction
- LLM-generated candidate reasoning
- Cross-encoder reranking
- Larger real-world evaluation datasets
- Improved PDF and DOCX parsing
- Dynamic skill extraction
- Optimized vector retrieval for large resume collections
- Web interface for uploading job descriptions and resumes

---

## Security

Sensitive configuration such as `.env` files is excluded from Git using `.gitignore`.

API keys and credentials should never be committed to source control.

---

## Conclusion

This project demonstrates an end-to-end resume retrieval and job matching workflow using semantic embeddings and a vector database.

It combines semantic retrieval with structured skill and experience checks to provide ranked and explainable candidate matches while also evaluating retrieval quality and performance.