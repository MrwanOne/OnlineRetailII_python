# Online Retail II — Simple Python Project Template

A deliberately simple starter kit for the Advanced Python Programming course project. It follows the course brief: objective, business questions, dataset description/source, data exploration and cleaning, Python analysis, optional models, evaluation, plots, and expected results.

## Dataset
Official UCI source: https://archive.ics.uci.edu/dataset/502/online+retail+ii

Download the dataset from UCI and put the downloaded Excel file in `data/raw/`. Do not commit the dataset to GitHub. Check the exact filename and column names after downloading.

## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
1. Place the downloaded file under `data/raw/`.
2. Open `notebooks/01_project_analysis.ipynb` in Jupyter.
3. Run cells from top to bottom.
4. Save charts in `outputs/` and write findings in `docs/REPORT_TEMPLATE.md`.

## Simple team workflow
- Use one shared GitHub repository.
- Assign data audit/cleaning, sales analysis/plots, and customer analysis/report as separate tasks.
- Agree on filtering rules before comparing results.
- Work in separate notebooks or files and review changes before merging.
- Never upload raw dataset, `.venv`, or generated data to GitHub.

## Course checklist
- [ ] Project objective
- [ ] Business question
- [ ] Detailed dataset description
- [ ] Official source link
- [ ] Data exploration and cleaning
- [ ] Python analysis steps
- [ ] Model(s), if used
- [ ] Evaluation
- [ ] Graphical outputs
- [ ] Expected results based on actual analysis
