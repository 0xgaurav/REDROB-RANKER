import csv
import shutil
import time
from pathlib import Path

import gradio as gr

from src.scripts.run_pipeline import run_pipeline


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/output")

PREVIEW_HEADERS = ["Rank", "Candidate", "Score", "Reasoning"]
APP_THEME = gr.themes.Soft(
    primary_hue="cyan",
    secondary_hue="blue",
    neutral_hue="slate",
    radius_size="md",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
)

CUSTOM_CSS = """
:root { color-scheme: dark; }

body,
.gradio-container {
    min-height: 100vh;
    background: #090f1c !important;
    color: #e5edf8 !important;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif !important;
}

.gradio-container {
    max-width: none !important;
    padding: 0 !important;
}

.gradio-container .contain {
    max-width: none !important;
}

#app-shell {
    min-height: 100vh;
    background:
        radial-gradient(circle at 18% 0%, rgba(14, 165, 233, 0.10), transparent 28%),
        radial-gradient(circle at 82% 2%, rgba(124, 58, 237, 0.08), transparent 30%),
        linear-gradient(180deg, #08101f 0%, #09111f 100%);
}

.topbar {
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 52px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.13);
    background: rgba(8, 15, 28, 0.86);
}

.brand {
    display: flex;
    align-items: center;
    gap: 11px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: 0;
}

.brand-mark {
    width: 32px;
    height: 32px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    color: #ffffff;
    background: linear-gradient(135deg, #22d3ee 0%, #2563eb 100%);
    box-shadow: 0 10px 28px rgba(14, 165, 233, 0.24);
    font-size: 12px;
}

.brand-accent { color: #22d3ee; }

.nav-actions {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #8c9bb0;
    font-size: 13px;
}

.nav-icon,
.admin-dot {
    width: 26px;
    height: 26px;
    display: grid;
    place-items: center;
    border-radius: 999px;
}

.nav-icon {
    border: 1px solid transparent;
}

.admin-dot {
    color: #ffffff;
    background: linear-gradient(135deg, #0ea5e9, #2563eb);
    font-size: 12px;
}

.page {
    max-width: 1232px;
    margin: 0 auto;
    padding: 32px 24px 48px;
}

.hero {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: end;
    gap: 28px;
    margin-bottom: 32px;
}

.pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
}

.pill {
    display: inline-flex;
    align-items: center;
    min-height: 26px;
    padding: 0 12px;
    border-radius: 999px;
    border: 1px solid rgba(34, 211, 238, 0.34);
    background: rgba(8, 47, 73, 0.34);
    color: #22d3ee;
    font-size: 12px;
    font-weight: 700;
}

.pill.alt {
    border-color: rgba(167, 139, 250, 0.38);
    background: rgba(59, 7, 100, 0.22);
    color: #a78bfa;
}

.hero h1 {
    margin: 0;
    color: #ffffff;
    font-size: 24px;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: 0;
}

.hero p {
    margin: 7px 0 0;
    color: #94a3b8;
    font-size: 15px;
}

.workflow {
    min-height: 46px;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 20px;
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 16px;
    background: rgba(15, 23, 42, 0.60);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
    white-space: nowrap;
}

.workflow span {
    color: #cbd5e1;
    font-size: 13px;
    font-weight: 700;
}

.workflow b {
    color: #506176;
    font-weight: 700;
}

.workflow .cyan { color: #22d3ee; }
.workflow .violet { color: #a78bfa; }
.workflow .green { color: #10b981; }

.dashboard-grid {
    align-items: stretch !important;
    gap: 20px !important;
}

.dashboard-card {
    min-height: 466px;
    padding: 26px !important;
    border: 1px solid rgba(148, 163, 184, 0.16) !important;
    border-radius: 16px !important;
    background: rgba(15, 23, 42, 0.68) !important;
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.035),
        0 20px 50px rgba(0, 0, 0, 0.18);
}

.card-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 20px;
}

.card-title {
    margin: 0;
    color: #f8fafc;
    font-size: 15px;
    font-weight: 800;
}

.card-sub {
    margin: 4px 0 0;
    color: #8190a6;
    font-size: 13px;
}

.card-action {
    width: 32px;
    height: 32px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    color: #22d3ee;
    background: rgba(8, 145, 178, 0.18);
}

.upload-block {
    margin-bottom: 14px !important;
}

.upload-block label > span {
    color: #dbeafe !important;
    font-size: 14px !important;
    font-weight: 800 !important;
}

.upload-block [data-testid="file"],
.upload-block .file-preview {
    min-height: 96px !important;
    border: 1px dashed rgba(148, 163, 184, 0.28) !important;
    border-radius: 14px !important;
    background: rgba(15, 23, 42, 0.58) !important;
    transition: border-color 150ms ease, background 150ms ease;
}

.upload-block [data-testid="file"]:hover {
    border-color: rgba(34, 211, 238, 0.56) !important;
    background: rgba(8, 47, 73, 0.20) !important;
}

.upload-block .wrap,
.upload-block .file-preview {
    color: #94a3b8 !important;
}

#run-button {
    width: 100%;
    min-height: 44px;
    margin: 6px 0 4px;
    border: 0 !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #0891b2, #2563eb) !important;
    color: #ffffff !important;
    font-size: 14px !important;
    font-weight: 800 !important;
    box-shadow: 0 14px 28px rgba(37, 99, 235, 0.20);
}

#run-button:hover {
    filter: brightness(1.06);
}

#run-button:disabled {
    filter: grayscale(0.25) brightness(0.72);
    cursor: wait;
}

.status-panel,
.result-panel {
    margin-top: 16px;
    padding: 15px 16px;
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.58);
}

.status-line {
    display: flex;
    align-items: center;
    gap: 10px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: #64748b;
}

.status-dot.ready { background: #94a3b8; }
.status-dot.processing { background: #22d3ee; box-shadow: 0 0 0 4px rgba(34, 211, 238, 0.10); }
.status-dot.success { background: #10b981; box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.10); }
.status-dot.error { background: #ef4444; box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.10); }

.status-title {
    color: #f8fafc;
    font-size: 14px;
    font-weight: 800;
}

.status-text {
    margin: 6px 0 0 18px;
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.45;
}

.progress-head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 18px;
    margin-bottom: 10px;
}

.stage-label {
    color: #94a3b8;
    font-size: 13px;
}

.percent-label {
    color: #93c5fd;
    font-size: 12px;
    font-weight: 800;
}

.progress-track {
    height: 7px;
    overflow: hidden;
    border-radius: 999px;
    background: rgba(30, 41, 59, 0.95);
}

.progress-fill {
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #22d3ee, #2563eb, #8b5cf6);
    transition: width 220ms ease;
}

.result-copy {
    margin: 12px 0 0;
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.5;
}

.preview-table {
    margin-top: 18px !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

.preview-table table {
    background: rgba(15, 23, 42, 0.72) !important;
}

.preview-table th {
    color: #94a3b8 !important;
    background: rgba(15, 23, 42, 0.96) !important;
    font-size: 12px !important;
    font-weight: 800 !important;
}

.preview-table td {
    color: #cbd5e1 !important;
    border-color: rgba(148, 163, 184, 0.09) !important;
    font-size: 12px !important;
}

.download-file {
    margin-top: 14px !important;
}

.download-file label > span {
    color: #dbeafe !important;
    font-size: 13px !important;
    font-weight: 800 !important;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-top: 32px;
}

.stat-card {
    min-height: 126px;
    padding: 20px;
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 16px;
    background: rgba(15, 23, 42, 0.68);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
}

.stat-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.stat-icon {
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    border-radius: 13px;
    color: #22d3ee;
    background: rgba(8, 145, 178, 0.17);
    font-weight: 900;
}

.stat-card:nth-child(2) .stat-icon { color: #60a5fa; background: rgba(37, 99, 235, 0.16); }
.stat-card:nth-child(3) .stat-icon { color: #a78bfa; background: rgba(124, 58, 237, 0.16); }
.stat-card:nth-child(4) .stat-icon { color: #10b981; background: rgba(16, 185, 129, 0.14); }

.stat-dot {
    width: 6px;
    height: 6px;
    border-radius: 999px;
    background: #22d3ee;
    opacity: 0.65;
}

.stat-value {
    color: #ffffff;
    font-size: 26px;
    line-height: 1;
    font-weight: 900;
}

.stat-label {
    margin-top: 8px;
    color: #8190a6;
    font-size: 13px;
}

.stat-note {
    margin-top: 10px;
    color: #22d3ee;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 12px;
}

.footer {
    margin-top: 34px;
    color: #526176;
    font-size: 12px;
    text-align: center;
}

@media (max-width: 980px) {
    .topbar { padding: 0 24px; }
    .hero { grid-template-columns: 1fr; align-items: start; }
    .workflow { width: fit-content; max-width: 100%; overflow-x: auto; }
    .stats-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 720px) {
    .topbar { height: auto; padding: 12px 18px; align-items: flex-start; gap: 12px; }
    .nav-actions { gap: 8px; }
    .page { padding: 24px 14px 36px; }
    .dashboard-card { padding: 20px !important; min-height: auto; }
    .stats-grid { grid-template-columns: 1fr; }
}
"""


def status_html(state: str, title: str, text: str) -> str:
    return f"""
    <div class="status-panel">
      <div class="status-line">
        <span class="status-dot {state}"></span>
        <span class="status-title">{title}</span>
      </div>
      <p class="status-text">{text}</p>
    </div>
    """


def progress_html(percent: int, stage: str, detail: str, state: str = "processing") -> str:
    bounded_percent = max(0, min(100, percent))
    return f"""
    <div class="result-panel">
      <div class="status-line">
        <span class="status-dot {state}"></span>
        <span class="status-title">{stage}</span>
      </div>
      <div class="progress-head">
        <span class="stage-label">Analysis Progress</span>
        <span class="percent-label">{bounded_percent}%</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill" style="width: {bounded_percent}%"></div>
      </div>
      <p class="result-copy">{detail}</p>
    </div>
    """


def completion_html(message: str) -> str:
    return f"""
    <div class="status-panel">
      <div class="status-line">
        <span class="status-dot success"></span>
        <span class="status-title">Completion Message</span>
      </div>
      <p class="status-text">{message}</p>
    </div>
    """


READY_STATUS = status_html(
    "ready",
    "Ready",
    "Upload both files to begin ranking.",
)
READY_RESULTS = progress_html(
    0,
    "Awaiting Analysis",
    "Upload a job description and candidate database, then run the AI ranking workflow.",
    "ready",
)
MISSING_RESULTS = progress_html(
    0,
    "Missing Files",
    "Please upload both required files before running the analysis.",
    "error",
)


def read_preview_rows(output_csv: Path) -> tuple[list[list[str]], list[float]]:
    rows: list[list[str]] = []
    scores: list[float] = []

    with output_csv.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            score_value = row.get("score", "")
            try:
                numeric_score = float(score_value)
                scores.append(numeric_score)
                score_label = f"{numeric_score:.2f}"
            except (TypeError, ValueError):
                score_label = score_value

            if len(rows) < 5:
                reasoning = row.get("reasoning", "")
                if len(reasoning) > 120:
                    reasoning = f"{reasoning[:117]}..."
                rows.append(
                    [
                        row.get("rank", ""),
                        row.get("candidate_id", ""),
                        score_label,
                        reasoning,
                    ]
                )

    return rows, scores


def seconds_label(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    remaining = int(seconds % 60)
    return f"{minutes}m {remaining}s"


def stats_html(row_count: int, scores: list[float], elapsed_seconds: float) -> str:
    average_score = (sum(scores) / len(scores) * 10) if scores else 0
    top_score = (max(scores) * 10) if scores else 0
    return f"""
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-top"><span class="stat-icon">#</span><span class="stat-dot"></span></div>
        <div class="stat-value">{row_count}</div>
        <div class="stat-label">Candidates Ranked</div>
        <div class="stat-note">top submission rows</div>
      </div>
      <div class="stat-card">
        <div class="stat-top"><span class="stat-icon">%</span><span class="stat-dot"></span></div>
        <div class="stat-value">{average_score:.1f}%</div>
        <div class="stat-label">Average Match Score</div>
        <div class="stat-note">submission average</div>
      </div>
      <div class="stat-card">
        <div class="stat-top"><span class="stat-icon">*</span><span class="stat-dot"></span></div>
        <div class="stat-value">{top_score:.1f}%</div>
        <div class="stat-label">Top Candidate Score</div>
        <div class="stat-note">highest ranked result</div>
      </div>
      <div class="stat-card">
        <div class="stat-top"><span class="stat-icon">t</span><span class="stat-dot"></span></div>
        <div class="stat-value">{seconds_label(elapsed_seconds)}</div>
        <div class="stat-label">Processing Time</div>
        <div class="stat-note">current run</div>
      </div>
    </div>
    """


def disable_controls():
    return (
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False, value="Running..."),
        gr.update(value="", visible=False),
        gr.update(value="", visible=False),
        gr.update(value=[], visible=False),
        gr.update(value=None, visible=False),
        gr.update(value="", visible=False),
        gr.update(value="", visible=False),
    )


def enable_controls():
    return (
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True, value="Run AI Ranking"),
    )


def rank_candidates(job_file, candidates_file, progress=gr.Progress(track_tqdm=True)):
    if job_file is None or candidates_file is None:
        progress(0, desc="Waiting for required files")
        yield (
            gr.update(
                value=status_html(
                    "error",
                    "Missing Files",
                    "Please upload both the Job Description (.docx) and Candidate Database (.jsonl).",
                ),
                visible=True,
            ),
            gr.update(value=MISSING_RESULTS, visible=True),
            gr.update(value=[], visible=False),
            gr.update(value=None, visible=False),
            gr.update(value="", visible=False),
            gr.update(value="", visible=False),
        )
        return

    stages = [
        (8, "Uploading Files", "Copying uploaded files into the existing pipeline input paths."),
        (16, "Parsing Job Description", "Preparing the job description for AI analysis."),
        (25, "Loading Candidate Database", "Reading the candidate database for ranking."),
        (34, "Extracting Candidate Features", "Building candidate feature signals."),
        (45, "Generating Embeddings", "Preparing semantic representations."),
        (58, "Running Semantic Matching", "Comparing candidate profiles against the job description."),
        (70, "Computing Scores", "Combining match, quality, and consistency signals."),
        (82, "Ranking Candidates", "Selecting the strongest matches for the final submission."),
    ]

    started_at = time.perf_counter()

    for percent, stage, detail in stages[:1]:
        progress(percent / 100, desc=f"{stage}...")
        yield (
            gr.update(value="", visible=False),
            gr.update(value="", visible=False),
            gr.update(value=[], visible=False),
            gr.update(value=None, visible=False),
            gr.update(value="", visible=False),
            gr.update(value="", visible=False),
        )
        time.sleep(0.12)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy(job_file, RAW_DIR / "job_description.docx")
    shutil.copy(candidates_file, RAW_DIR / "candidates.jsonl")

    try:
        for percent, stage, detail in stages[1:]:
            progress(percent / 100, desc=f"{stage}...")
            yield (
                gr.update(value="", visible=False),
                gr.update(value="", visible=False),
                gr.update(value=[], visible=False),
                gr.update(value=None, visible=False),
                gr.update(value="", visible=False),
                gr.update(value="", visible=False),
            )
            time.sleep(0.12)

        run_pipeline()

        final_stages = [
            (90, "Selecting Top 100", "Finalizing the ranked candidate shortlist."),
            (96, "Generating submission.csv", "Writing the CSV output file."),
            (100, "Completed", "Ranking complete. Preview and download are ready."),
        ]

        for percent, stage, detail in final_stages[:-1]:
            progress(percent / 100, desc=f"{stage}...")
            yield (
                gr.update(value="", visible=False),
                gr.update(value="", visible=False),
                gr.update(value=[], visible=False),
                gr.update(value=None, visible=False),
                gr.update(value="", visible=False),
                gr.update(value="", visible=False),
            )
            time.sleep(0.12)

        output_csv = OUTPUT_DIR / "submission.csv"
        if output_csv.exists():
            preview_rows, scores = read_preview_rows(output_csv)
            elapsed_seconds = time.perf_counter() - started_at
            progress(1.0, desc="Completed")
            yield (
                gr.update(
                    value=status_html("success", "Completed", "Top 100 submission file is ready to download."),
                    visible=True,
                ),
                gr.update(value=progress_html(100, "Completed", "Analysis finished successfully.", "success"), visible=True),
                gr.update(value=preview_rows, visible=True),
                gr.update(value=str(output_csv), visible=True),
                gr.update(
                    value=completion_html("Download the generated CSV or review the top 5 preview below."),
                    visible=True,
                ),
                gr.update(
                    value=stats_html(len(scores), scores, elapsed_seconds),
                    visible=True,
                ),
            )
            return

        yield (
            gr.update(
                value=status_html("error", "No Output Produced", "Pipeline finished but submission.csv was not generated."),
                visible=True,
            ),
            gr.update(value=progress_html(100, "Output Missing", "The expected CSV file was not created.", "error"), visible=True),
            gr.update(value=[], visible=False),
            gr.update(value=None, visible=False),
            gr.update(value="", visible=False),
            gr.update(value="", visible=False),
        )

    except Exception as e:
        yield (
            gr.update(value=status_html("error", "Pipeline Error", str(e)), visible=True),
            gr.update(value=progress_html(100, "Ranking Failed", "Please review the error and try again.", "error"), visible=True),
            gr.update(value=[], visible=False),
            gr.update(value=None, visible=False),
            gr.update(value="", visible=False),
            gr.update(value="", visible=False),
        )


with gr.Blocks(
    title="REDROB-RANKER",
    theme=APP_THEME,
    css=CUSTOM_CSS,
) as demo:
    with gr.Column(elem_id="app-shell"):
        gr.HTML(
            """
            <div class="topbar">
              <div class="brand">
                <div class="brand-mark">R</div>
                <div>REDROB-<span class="brand-accent">RANKER</span></div>
              </div>
              <div class="nav-actions">
                <span class="nav-icon" title="Theme">&#9788;</span>
                <span class="nav-icon" title="Settings">&#9881;</span>
                <span class="admin-dot" title="Admin">A</span>
                <strong>Admin</strong>
              </div>
            </div>
            """
        )

        with gr.Column(elem_classes=["page"]):
            gr.HTML(
                """
                <section class="hero">
                  <div>
                    <div class="pills">
                      <span class="pill">v2.4.1 - Production</span>
                      <span class="pill alt">GPT-4o Powered</span>
                    </div>
                    <h1>REDROB-RANKER</h1>
                    <p>AI-Powered Candidate Ranking System - automated shortlisting at scale</p>
                  </div>
                  <div class="workflow" aria-label="Workflow">
                    <span class="cyan">Upload</span><b>&rsaquo;</b>
                    <span class="cyan">AI Analysis</span><b>&rsaquo;</b>
                    <span class="violet">Ranking</span><b>&rsaquo;</b>
                    <span class="green">Download</span>
                  </div>
                </section>
                """
            )

            with gr.Row(equal_height=True, elem_classes=["dashboard-grid"]):
                with gr.Column(scale=1, elem_classes=["dashboard-card"]):
                    gr.HTML(
                        """
                        <div class="card-head">
                          <div>
                            <h2 class="card-title">Upload Files</h2>
                            <p class="card-sub">Provide your JD and candidate data</p>
                          </div>
                          <div class="card-action">&#8593;</div>
                        </div>
                        """
                    )
                    jd = gr.File(
                        label="Job Description",
                        file_types=[".docx"],
                        elem_classes=["upload-block"],
                    )
                    candidates = gr.File(
                        label="Candidate Database",
                        file_types=[".jsonl"],
                        elem_classes=["upload-block"],
                    )
                    run_btn = gr.Button("Run AI Ranking", elem_id="run-button", variant="primary")
                    upload_status = gr.HTML(value=READY_STATUS)

                with gr.Column(scale=1, elem_classes=["dashboard-card"]):
                    gr.HTML(
                        """
                        <div class="card-head">
                          <div>
                            <h2 class="card-title">Results</h2>
                            <p class="card-sub">Awaiting analysis</p>
                          </div>
                        </div>
                        """
                    )
                    progress_panel = gr.HTML(value=READY_RESULTS)
                    preview = gr.Dataframe(
                        value=[],
                        headers=PREVIEW_HEADERS,
                        datatype=["str", "str", "str", "str"],
                        label="Top 5 Preview",
                        interactive=False,
                        visible=False,
                        wrap=True,
                        max_height=240,
                        elem_classes=["preview-table"],
                    )
                    csv_output = gr.File(
                        label="Download CSV",
                        visible=False,
                        elem_classes=["download-file"],
                    )
                    completion_message = gr.HTML(value="", visible=False)

            stats_panel = gr.HTML(value="", visible=False)

            gr.HTML('<div class="footer">REDROB-RANKER candidate ranking dashboard</div>')

    run_event = run_btn.click(
        disable_controls,
        inputs=None,
        outputs=[
            jd,
            candidates,
            run_btn,
            upload_status,
            progress_panel,
            preview,
            csv_output,
            completion_message,
            stats_panel,
        ],
        queue=False,
    )
    run_event.then(
        rank_candidates,
        inputs=[jd, candidates],
        outputs=[
            upload_status,
            progress_panel,
            preview,
            csv_output,
            completion_message,
            stats_panel,
        ],
    ).then(
        enable_controls,
        inputs=None,
        outputs=[jd, candidates, run_btn],
        queue=False,
    )

demo.launch()
