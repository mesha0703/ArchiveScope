# ArchiveScope — README

A lightweight desktop application (Python + PySide6) to parse Sinumerik archives (.DSF, .ARC) and visualize/edit drive filter settings with instant Bode plots.
App language: German; (+ English coming soon)

![alt text](https://github.com/mesha0703/ArchiveScope/blob/main/gallery/example1.png?raw=true)
![alt text](https://github.com/mesha0703/ArchiveScope/blob/main/gallery/example2.png?raw=true)

## Highlights

- **Archive ingestion**: Load exported Sinumerik archives (`.ARC ASCII or .DSF`).
- **Domain model**: Archives → Drives → Controllers → Filters → Parameters (incl. bit-config parameters).
- **Interactive visualization**: Live Bode plots for low-pass / PT2 / notch filters; adaptation/option views where provided.
- **Parameter editing**: Change values via UI controls with min/max/step validation.
- **Compare & export**: Inspect differences and export updated settings back to an archive payload.
- **Ergonomic UI**: Drag-and-drop for files; clear separation of UI and domain logic.

## Requirements

- **Python**: 3.13.2 (recommended)
- **OS**: Windows or macOS (Intel/Apple Silicon)
- **Dependencies**: See `requirements.txt` (PySide6, numpy, matplotlib, etc.)

## Quick Start

1. **Create & activate a virtual environment (only if you want to run python script)**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app**
    ```
    python ArchiveScope/main.py
    ```

## Using the App

1. **Open an archive**: Drag & drop into the main window or use `File → Open…`.
2. **Explore**: Select a drive → controller → filter.
3. **Tune**: Adjust parameters; Bode plot updates immediately.
4. **Export**: Save modified settings via `File → Export…` (non-destructive; original files remain unchanged). (function coming soon)

## Project Structure

- `ArchiveScope/ui/…` — Qt widgets (e.g., archive surface, filter editor, Bode plot widget)
- `ArchiveScope/domain/…` — Archive, Drive, Controller, Filter, Parameter, BitConfig, etc.
- `ArchiveScope/config.py` — Parameter/label configuration and mappings
- `ArchiveScope/main.py` — Application bootstrap

*(Actual paths may vary slightly; see repository.)*

## Troubleshooting

- **Qt platform plugin errors** (e.g., “could not load xcb/cocoa”):
  Ensure you’re running from the activated venv and that PySide6 is fully installed:
  ```bash
  pip install --upgrade --force-reinstall PySide6
  ```

- **Dark mode / unreadable hover text on Windows**:
  If system dark mode causes poor contrast, disable OS dark mode or force a light Qt palette in app settings (a simple stylesheet can be applied in `main.py`).

- **Matplotlib backend issues**:
  Confirm matplotlib is installed from `requirements.txt` and no conflicting backends are forced by environment variables.

## Data & Privacy

The app works offline. Archives are parsed locally; exports create new files without altering originals.

## Contributing

- Use clear, typed APIs in the domain layer.
- Follow Python best practices (PEP 8) and keep UI logic decoupled from parsing/visualization.
- Please open issues/PRs with reproducible steps and sample archives (redacted if needed).

## License

See `LICENSE` in the repository (or clarify with the project owner if absent).

## TL;DR

Create venv → `pip install -r requirements.txt` → run `python ArchiveScope/main.py` → drop a Sinumerik archive → tune filters with live Bode plots → export.