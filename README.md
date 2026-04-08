# Assignment A4 README

## 1. Pipeline stages
This project uses a two-stage sequential pipeline defined in `pipeline.py` and `crews.py`.

- **Stage 0 - Research Crew (`research_crew`)**: The `Researcher` agent takes the topic *Application of AI in healthcare* and generates a detailed research report with background, key applications, and major considerations.
- **Stage 1 - Analysis Crew (`analysis_crew`)**: The `Analyst` agent uses the Stage 0 result as input and produces a Markdown-style analysis with key-point summary, risk assessment, and feasibility recommendations.

Each completed stage passes its result to the next stage as `previous_result`.

## 2. How to run and resume after failure
Prepare the required dependencies and local `.env` file, then run:

```bash
python pipeline.py
```

The pipeline stores finished stage outputs in `checkpoint.json`.
If a failure happens, keep `checkpoint.json` and run the same command again:

```bash
python pipeline.py
```

When the program starts, it checks `checkpoint.json`, skips completed stages, and resumes from the first unfinished stage. For example, if `stage_0` already exists in the file, the next run continues from `stage_1`.

## 3. Challenges encountered and solution
A major problem during testing was that the terminal output kept appearing as garbled text, making the generated content difficult to read. The issue was caused by terminal encoding rather than pipeline logic.

The final solution was to run the script in **CMD** and force Python output to UTF-8 before execution:

```bash
set PYTHONIOENCODING=utf-8
python pipeline.py
```

After this change, the terminal output displayed correctly.
