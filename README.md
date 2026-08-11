# Chinese-Grammar-Visualizer
# Production-Grade

An advanced, multi-tiered Natural Language Processing (NLP) application engineered to parse, analyze, and visualize grammatical dependency structures in Mandarin Chinese. This project shifts away from brittle, index-based string tokenization in favor of deterministic **Directed Acyclic Graph (DAG)** traversal over linguistic dependency trees.

## 🏛️ System Architecture & Design Patterns

The system is decoupled into isolated, single-responsibility operational layers to enforce strict **Separation of Concerns (SoC)** and maximize maintainability:

1. **Service / Pipeline Layer (`app.py` -> `NaturalLanguagePipeline`)**: Implements a Resource-Caching pattern to handle heavy deep learning transformations. It wraps SpaCy’s neural network pipeline (`zh_core_web_sm`) to isolate tokenization, part-of-speech (POS) tagging, and dependency syntax labeling.
2. **Algorithmic Parser Layer (`app.py` -> `SyntaxTreeAnalyzer`)**: Treats input sentences as an acyclic graph of grammatical dependencies. It executes targeted node-searching algorithms starting from the structural root vertex to isolate functional subject, verb, and object (SVO) kernels.
3. **Persistence Layer (`database.py`)**: Utilizes a relational SQLite data access engine. Transactions are safely executed via parameterized queries to eliminate SQL-injection vulnerabilities, while connection lifetimes are strictly managed through context managers.
4. **Presentation Layer (`app.py` -> `AppViewEngine`)**: A stateless view system that transforms machine-parsed dependency structures into dynamic HTML5/CSS3 components and asynchronously serves base64-encoded audio vectors without disk I/O leaks.

---

## 📊 Algorithmic Approach: Dependency Graph Traversal

Rather than processing words linearly from left to right, this engine maps out the entire hierarchical structure of the sentence. 

[ 抓 (Verb: ROOT) ]/           /             [ 猫 (nsubj) ]     [ 老鼠 (obj) ]|[ 一个 (nummod) ]
* **Root Extraction**: The algorithm scans the sentence's token graph to locate the primary kernel operator—the `ROOT` verb vertex.
* **Directed Search**: Using the `ROOT` node as the coordinate origin, the engine executes a directed local search down specific dependency edges (such as `nsubj`, `nsubj:pass`, and `obj`).
* **Phrase Aggregation**: When a target branch is hit, a sub-graph collection step is triggered to dynamically pull child modifiers (e.g., matching the number modifier `一个` with the noun `老鼠`), guaranteeing that full noun phrases are returned instead of isolated characters.

---

## 🛠️ Automated Testing & Robustness

Reliability is enforced through an automated suite written with Python’s native `unittest` framework (`test_analyzer.py`), following the **Arrange-Act-Assert (AAA)** pattern. The test suite guarantees predictable error bounds against anomalous inputs:
* **Standard Topologies**: Asserts correct mapping of traditional SVO sentences.
* **Anomalous Topologies**: Verifies safe fallbacks when sentences lack direct objects or direct arguments.
* **Boundary Conditions**: Prevents structural runtime faults when encountering completely blank or empty string streams.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.10+ installed on your system.

### 1. Clone & Setup Environment

```bash
git clone https://github.com
cd chinese-grammar-visualizer
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Dependencies & Language Models

```bash
pip install -r requirements.txt
python -m spacy download zh_core_web_sm
```

### 3. Run the Automated Test Suite

Ensure the codebase satisfies all strict boundary asserts before launching:

```bash
python -m unittest test_analyzer.py
```

### 4. Deploy the UI Framework

```bash
streamlit run app.py
```

---

## 📦 File Structure

```text
chinese-grammar-visualizer/
│
├── app.py              # Main application entry point, neural handlers, and UI engine
├── database.py         # Relational database pipeline & SQL log transaction layer
├── test_analyzer.py    # Automated Unit Test Suite verifying graph edge routing
└── requirements.txt    # Frozen environment dependency tree specifications
```
