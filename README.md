# Chinese Grammar Visualizer

**A Python NLP application for parsing, analyzing, and visualizing grammatical dependency structures in Mandarin Chinese.**

Chinese Grammar Visualizer uses **spaCy dependency parsing** and graph-based traversal to transform Chinese sentences into interpretable grammatical structures. Instead of relying on positional or index-based tokenization, the application navigates dependency relationships to identify grammatical components such as subjects, predicates, objects, and modifiers.

## ✨ Features

* **Dependency Parsing** — Uses spaCy's `zh_core_web_sm` model to tokenize Chinese text and identify POS tags and dependency relationships.
* **Graph-Based Syntax Analysis** — Represents grammatical dependencies as a directed graph and traverses the structure from the sentence root.
* **SVO Extraction** — Identifies subject, verb, and object relationships from dependency edges such as `nsubj`, `nsubj:pass`, and `obj`.
* **Phrase Aggregation** — Recursively collects dependent modifiers to reconstruct complete grammatical phrases rather than isolated tokens.
* **Interactive Visualization** — Provides a Streamlit interface for exploring parsed sentence structures.
* **Persistent Storage** — Stores application data using SQLite with parameterized queries and managed database connections.
* **Automated Testing** — Includes unit tests covering standard sentence structures, missing arguments, and empty-input edge cases.

---

## 🧠 How It Works

The application processes a Chinese sentence through several stages:

```text
Chinese Sentence
       │
       ▼
┌─────────────────────┐
│ spaCy NLP Pipeline  │
│ Tokenization + POS  │
│ Dependency Parsing  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Dependency Graph    │
│                     │
│ ROOT → Subject      │
│     → Object        │
│     → Modifiers     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Syntax Tree Analyzer│
│ Graph Traversal     │
│ Phrase Aggregation  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Streamlit Interface │
│ Visualization       │
└─────────────────────┘
```

### Example

For a sentence such as:

```text
猫抓一只老鼠
```

the dependency structure can be conceptually represented as:

```text
              ROOT
               │
              抓
             /  \
        nsubj     obj
          │         │
         猫        老鼠
                    │
                  nummod
                    │
                   一只
```

The analyzer starts from the `ROOT` node and follows relevant dependency edges to identify grammatical relationships.

Rather than assuming that grammatical roles occur at fixed token positions, the parser uses the dependency structure itself to determine relationships.

---

## 🏗️ Architecture

The application is organized into separate components with clear responsibilities.

### 1. NLP Pipeline

**`app.py → NaturalLanguagePipeline`**

Handles linguistic preprocessing and model inference using spaCy.

Responsibilities include:

* Chinese tokenization
* Part-of-speech tagging
* Dependency parsing
* NLP model loading and resource management

### 2. Syntax Tree Analyzer

**`app.py → SyntaxTreeAnalyzer`**

Performs graph-based analysis over the dependency structure.

The analyzer:

1. Locates the sentence `ROOT`
2. Traverses relevant dependency edges
3. Identifies grammatical roles
4. Collects dependent modifiers
5. Constructs interpretable grammatical structures

### 3. Persistence Layer

**`database.py`**

Provides SQLite-based persistence.

The database layer uses:

* Parameterized SQL queries
* Context-managed connections
* Explicit transaction handling

This keeps database operations separate from NLP and presentation logic.

### 4. Presentation Layer

**`app.py → AppViewEngine`**

Provides the Streamlit interface and converts analyzed structures into interactive visual outputs.

---

## 🔍 Algorithmic Approach

The core of the project is **dependency graph traversal**.

A dependency parse can be viewed as a directed graph in which:

* **Nodes** represent tokens
* **Edges** represent grammatical dependencies
* **ROOT** identifies the central predicate of the sentence

The analyzer uses the root as the starting point and searches through specific dependency relationships.

For example:

```text
ROOT
 │
 ├── nsubj
 │
 └── obj
      │
      └── nummod
```

When an object is identified, the analyzer recursively examines its dependent nodes to reconstruct the complete phrase.

This approach makes the parser less dependent on word order and fixed token positions and allows grammatical structures to be represented explicitly.

---

## 🧪 Testing

The project includes an automated test suite using Python's built-in `unittest` framework.

```bash
python -m unittest test_analyzer.py
```

Tests cover:

* Standard subject-verb-object structures
* Sentences without direct objects
* Missing grammatical arguments
* Empty or blank input
* Dependency traversal edge cases

The tests follow an **Arrange–Act–Assert** structure to keep individual behaviors isolated and reproducible.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* pip
* spaCy

### 1. Clone the repository

```bash
git clone https://github.com/rainwangxjtu/chinese-grammar-visualizer.git
cd chinese-grammar-visualizer
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the Chinese language model

```bash
python -m spacy download zh_core_web_sm
```

### 5. Run the tests

```bash
python -m unittest test_analyzer.py
```

### 6. Launch the application

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```text
chinese-grammar-visualizer/
│
├── app.py
│   ├── NaturalLanguagePipeline
│   ├── SyntaxTreeAnalyzer
│   └── AppViewEngine
│
├── database.py
│   └── SQLite persistence layer
│
├── test_analyzer.py
│   └── Automated unit tests
│
├── requirements.txt
│   └── Python dependencies
│
└── README.md
```

---

## 🛠️ Technology Stack

| Category            | Technology                |
| ------------------- | ------------------------- |
| Language            | Python                    |
| NLP                 | spaCy                     |
| Chinese Model       | `zh_core_web_sm`          |
| Interface           | Streamlit                 |
| Database            | SQLite                    |
| Testing             | `unittest`                |
| Data Representation | Dependency graphs / trees |
| Version Control     | Git / GitHub              |

---

## 🎯 Project Motivation

Chinese grammatical structures can be difficult to represent using linear text alone. This project explores how **NLP dependency parsing and graph algorithms** can transform linguistic structures into computational representations that are easier to inspect and visualize.

The project sits at the intersection of:

* Natural Language Processing
* Computational Linguistics
* Graph Algorithms
* Software Engineering
* Language Education

The broader goal is to make linguistic structure more **computationally explicit, interpretable, and accessible**.

---

## 🔮 Future Development

Potential extensions include:

* Interactive dependency-tree visualization
* More comprehensive Chinese dependency patterns
* Automatic grammatical feature extraction
* Support for compound and complex sentences
* Sentence-level grammatical diagnostics
* Larger-scale corpus analysis
* Integration with neural NLP models
* Web-based deployment

---

## 👤 Author

**Yuqi Wang**

Assistant Professor (Language and Linguistics), Defense Language Institute

Interests include **Natural Language Processing, Computational Linguistics, Language Intelligence, and AI-assisted Language Learning**.
