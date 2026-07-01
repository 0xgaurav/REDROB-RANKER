import shutil
from pathlib import Path

import gradio as gr

from src.scripts.run_pipeline import run_pipeline


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/output")


def rank_candidates(job_file, candidates_file):
    if job_file is None or candidates_file is None:
        return "Please upload both files.", None

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy(job_file, RAW_DIR / "job_description.docx")
    shutil.copy(candidates_file, RAW_DIR / "candidates.jsonl")

    try:
        run_pipeline()

        output_csv = OUTPUT_DIR / "submission.csv"

        if output_csv.exists():
            return "Ranking completed successfully!", str(output_csv)

        return "Pipeline finished but submission.csv was not generated.", None

    except Exception as e:
        return f"Error:\n{str(e)}", None


with gr.Blocks(title="REDROB-RANKER") as demo:

    gr.Markdown(
        """
        # REDROB-RANKER

        AI-powered candidate ranking system for the RedRob Hackathon.

        Upload:
        - Job Description (.docx)
        - Candidates (.jsonl)

        The pipeline will generate the submission CSV.
        """
    )

    jd = gr.File(
        label="Job Description (.docx)",
        file_types=[".docx"]
    )

    candidates = gr.File(
        label="Candidates (.jsonl)",
        file_types=[".jsonl"]
    )

    run_btn = gr.Button("Run Ranking")

    status = gr.Textbox(label="Status")

    csv = gr.File(label="Submission CSV")

    run_btn.click(
        rank_candidates,
        inputs=[jd, candidates],
        outputs=[status, csv]
    )

demo.launch()