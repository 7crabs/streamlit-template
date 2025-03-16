# Streamlit Template

A modern template for building data analysis applications with Streamlit.

## Features

- Organized project structure for scalable applications
- Multi-page application support
- Type-checked with Pyright in strict mode
- Code quality tools (Ruff for linting and formatting)
- Git hooks via lefthook for pre-commit checks
- Python 3.13+ support

## Project Structure

```
streamlit-template/
├── src/                    # Source code directory
│   ├── pages/             # Streamlit multi-page app files
│   ├── components/        # Reusable components
│   └── utils/            # Utility functions
├── tests/                 # Test files
├── data/                  # Data files (if needed)
├── .streamlit/           # Streamlit configuration
│   └── config.toml      # Streamlit config file
├── main.py               # Main application
├── pyproject.toml        # Dependency management
├── lefthook.yml         # Git hooks configuration
├── .gitignore
└── README.md
```

## Setup

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) for package management
- [lefthook](https://lefthook.dev/) for git hooks

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/streamlit-template.git
   cd streamlit-template
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   uv sync
   ```

3. Install git hooks:
   ```bash
   lefthook install
   ```

## Development

### Running the application

```bash
streamlit run main.py
```

### Code Quality

- Format code:

  ```bash
  ruff format .
  ```

- Lint code:

  ```bash
  ruff check .
  ```

- Type check:
  ```bash
  pyright
  ```

### Testing

```bash
pytest
```

## Adding New Pages

1. Create a new file in `src/pages/` with the naming convention `<page_number>_<page_name>.py`
2. Implement your Streamlit page

Example:

```python
# src/pages/01_data_analysis.py
import streamlit as st

st.title("Data Analysis")
# Your page content here
```

## Deployment

### Local Deployment

For local deployment, simply run:

```bash
streamlit run main.py
```
