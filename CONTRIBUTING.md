# Contributing

## Setup

1. Fork the repository
2. Clone your fork
3. Copy `.env.example` to `.env`
4. Add your own local API keys to `.env`
5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the app locally:

```bash
python main.py
streamlit run streamlit_app.py
```

## Development Rules

- Do not commit `.env`
- Do not hardcode API keys or secrets
- Do not commit generated files from `data/runs`, `data/uploads`, or `data/outputs`
- Keep changes focused and small when possible
- Update the README if you change setup or user-facing behavior

## Suggested Contribution Areas

- LangGraph workflow improvements
- Better visualizations and chart interactions
- Streaming execution updates
- SQL and API data connectors
- Pinecone or retrieval-based memory
- UI and usability improvements
- Tests and documentation

## Pull Request Checklist

Before opening a PR, make sure:

- the app runs locally
- your changes do not expose secrets
- any new environment variables are added to `.env.example`
- relevant docs are updated
- the change is described clearly in the PR

## Issues

If you want to contribute but are unsure where to start:

- open an issue
- describe the problem or idea
- mention whether you want to work on it
