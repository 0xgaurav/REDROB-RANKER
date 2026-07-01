# RedRob-Ranker

> An end-to-end AI-powered candidate ranking system that semantically matches resumes to job descriptions, evaluates profile quality, detects inconsistencies and fraud signals, generates recruiter-style reasoning, and exports the Top 100 ranked candidates.

---

## Overview

RedRob-Ranker is a deterministic resume ranking pipeline designed to automate candidate evaluation for recruitment workflows.

Given:

- A Job Description
- Thousands of candidate profiles (JSONL)

the system:

- Extracts structured candidate features
- Performs semantic job matching
- Computes weighted candidate scores
- Detects fraudulent or suspicious profiles
- Performs profile consistency validation
- Generates recruiter-friendly reasoning
- Produces the Top 100 ranked candidates in CSV format.

The entire pipeline is deterministic, reproducible, scalable, and suitable for large candidate datasets.

---

# Features

### Semantic Candidate Matching

- Keyword Matching
- Embedding Similarity
- Skill Matching
- Experience Matching
- Education Matching

---

### Feature Extraction

Automatically extracts

- Skills
- Career History
- Timeline
- Behavioral Signals

---

### Candidate Scoring

Weighted scoring based on

- Skill similarity
- Experience similarity
- Education similarity
- Behavioral score
- Profile quality score

Produces normalized candidate scores.

---

### Fraud Detection

Detects

- Keyword stuffing
- Honeypot fields
- Statistical outliers

---

### Consistency Validation

Validates

- Skills vs Career History
- Education
- Career History
- Timeline
- Behavioral Signals

---

### Recruiter Reasoning

Automatically generates concise recruiter-style explanations using

- Job title
- Relevant experience
- Most relevant skills
- Certifications
- Publications
- Projects
- Leadership
- Cloud experience
- AI experience
- Response rate

Example:

```
Senior Applied Scientist with 16.2 years;
NLP, Python;
Published ML research;
response rate 0.81
```

---

### CSV Export

Exports only the

Top 100 Candidates

with

```
candidate_id
rank
score
reasoning
```

---

# Pipeline

```
Candidate JSONL
        │
        ▼
Candidate Validation
        │
        ▼
Feature Extraction
        │
        ▼
Semantic Matching
        │
        ▼
Behavior Score
        │
        ▼
Quality Score
        │
        ▼
Final Score
        │
        ▼
Fraud Detection
        │
        ▼
Consistency Analysis
        │
        ▼
Reason Generation
        │
        ▼
Ranking
        │
        ▼
Top 100
        │
        ▼
CSV Export
```

---

# Project Structure

```
REDROB-RANKER
│
├── config
│   ├── jd_config.yaml
│   ├── settings.yaml
│   └── weights.yaml
│
├── data
│   ├── raw
│   │   ├── candidate_schema.json
│   │   ├── candidates.jsonl
│   │   ├── job_description.docx
│   │   ├── redrob_signals_doc.docx
│   │   ├── sample_candidates.json
│   │   ├── sample_submission.csv
│   │   ├── submission_metadata_template.yaml
│   │   ├── submission_spec.docx
│   │   └── validate_submission.py
│   │
│   └── output
│       ├── submission.csv
│       └── logs.txt
│
├── src
│
│   ├── consistency
│   │   ├── behavior_consistency.py
│   │   ├── career_consistency.py
│   │   ├── consistency_engine.py
│   │   ├── education_consistency.py
│   │   ├── skill_consistency.py
│   │   └── timeline_consistency.py
│
│   ├── exporter
│   │   ├── csv_exporter.py
│   │   └── __init__.py
│
│   ├── features
│   │   ├── behavior_features.py
│   │   ├── career_features.py
│   │   ├── feature_extractor.py
│   │   ├── skill_features.py
│   │   └── timeline_features.py
│
│   ├── fraud
│   │   ├── fraud_engine.py
│   │   ├── honeypot_detector.py
│   │   ├── keyword_detector.py
│   │   └── outlier_detector.py
│
│   ├── matcher
│   │   ├── embedding_matcher.py
│   │   ├── keyword_matcher.py
│   │   └── semantic_matcher.py
│
│   ├── models
│   │   ├── candidate_features.py
│   │   ├── match_result.py
│   │   └── score_result.py
│
│   ├── parser
│   │   ├── candidate_loader.py
│   │   ├── jd_loader.py
│   │   └── schema_loader.py
│
│   ├── reasoning
│   │   ├── reason_generator.py
│   │   └── reason_templates.py
│
│   ├── scoring
│   │   ├── behavior_score.py
│   │   ├── final_score.py
│   │   ├── quality_score.py
│   │   └── score_calculator.py
│
│   ├── scripts
│   │   └── run_pipeline.py
│
│   └── utils
│       └── normalizer.py
│
└── tests
```

---

# Scoring

Each candidate is scored using multiple weighted components.

| Component | Description |
|------------|-------------|
| Semantic Matching | Job relevance |
| Skills | Matching skills |
| Experience | Relevant experience |
| Education | Academic relevance |
| Behavior | Behavioral signals |
| Quality | Overall profile quality |

The final score is normalized and used for ranking.

---

# Fraud Detection

The system identifies

- Excessive keyword stuffing
- Suspicious hidden fields
- Unrealistic profile statistics

Profiles are not automatically rejected but are flagged.

---

# Consistency Checks

The engine validates

- Skills supported by career history
- Education structure
- Career history
- Timeline chronology
- Behavioral signals

---

# Input

Candidate profiles

```
data/raw/candidates.jsonl
```

Job Description

```
data/raw/job_description.docx
```

---

# Output

Generated submission

```
data/output/submission.csv
```

Output format

| candidate_id | rank | score | reasoning |
|--------------|------|-------|-----------|

Only the Top 100 candidates are exported.

---

# Running the Pipeline

Clone the repository

```bash
git clone https://github.com/0xgaurav/redrob-ranker.git
cd redrob-ranker
```

Run

```bash
python -m src.scripts.run_pipeline
```

---

# Sample Output

| Rank | Candidate | Score | Reasoning |
|------|-----------|--------|-----------|
| 1 | CAND_001245 | 9.8731 | Senior Applied Scientist with 16.2 years; NLP, Python; Published ML research; response rate 0.81 |
| 2 | CAND_004152 | 9.8426 | Recommendation Systems Engineer with 8.1 years; OpenSearch, Embeddings; Built production recommendation systems; response rate 0.76 |
| 3 | CAND_007823 | 9.7945 | Backend Engineer with 9.5 years; Spark, Kafka; Real-time streaming systems; response rate 0.72 |

---

# Deterministic Design

The pipeline is fully deterministic.

Given the same:

- Job Description
- Candidate Dataset

the system always produces identical rankings and reasoning.

No randomness or external AI APIs are used during ranking.

---

# Technologies Used

- Python
- JSON
- CSV
- Logging
- Object-Oriented Design
- Rule-Based AI
- Semantic Matching
- Information Retrieval
- Feature Engineering

---

# Future Improvements

- Sentence Transformer embeddings
- FAISS vector search
- Cross-Encoder reranking
- Skill ontology matching
- Recruiter dashboard
- REST API
- Docker deployment
- Parallel candidate processing
- GPU embedding support

---

# Author

**Gaurav Singh**

GitHub: https://github.com/0xgaurav

---

## License

This project is intended for educational, research, and recruitment automation purposes.
