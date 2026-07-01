import shutil
from pathlib import Path

import gradio as gr

from src.scripts.run_pipeline import run_pipeline


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/output")

CUSTOM_CSS = """
:root {
    color-scheme: dark;
}

body,
.gradio-container {
    background:
        radial-gradient(circle at 12% 16%, rgba(32, 211, 238, 0.20), transparent 30%),
        radial-gradient(circle at 88% 10%, rgba(119, 91, 255, 0.18), transparent 28%),
        linear-gradient(135deg, #070b16 0%, #0d1424 44%, #101827 100%) !important;
    color: #eef6ff !important;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

.gradio-container {
    max-width: 1180px !important;
    margin: 0 auto !important;
}

#app-shell {
    padding: 28px 18px 34px;
}

.hero-card,
.glass-card {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(148, 163, 184, 0.20) !important;
    border-radius: 28px !important;
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.54)) !important;
    box-shadow: 0 28px 90px rgba(0, 0, 0, 0.38), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(18px);
}

.hero-card {
    padding: 42px 34px 34px;
    margin-bottom: 22px;
}

.hero-card::before,
.glass-card::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(120deg, rgba(255, 255, 255, 0.11), transparent 36%, rgba(45, 212, 191, 0.08));
}

.hero-inner {
    position: relative;
    z-index: 1;
    text-align: center;
}

.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border: 1px solid rgba(56, 189, 248, 0.30);
    border-radius: 999px;
    background: rgba(14, 165, 233, 0.10);
    color: #a7f3ff;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0;
    margin-bottom: 18px;
}

.hero-title {
    margin: 0;
    color: #ffffff;
    font-size: clamp(42px, 7vw, 74px);
    line-height: 1.02;
    font-weight: 900;
    letter-spacing: 0;
}

.hero-subtitle {
    margin: 14px 0 0;
    color: #7dd3fc;
    font-size: clamp(20px, 2.7vw, 30px);
    line-height: 1.25;
    font-weight: 800;
    letter-spacing: 0;
}

.hero-description {
    max-width: 790px;
    margin: 18px auto 0;
    color: #cbd5e1;
    font-size: 17px;
    line-height: 1.75;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin-top: 30px;
}

.feature-card {
    min-height: 154px;
    padding: 20px;
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 22px;
    background: rgba(15, 23, 42, 0.56);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.07), 0 16px 40px rgba(0, 0, 0, 0.18);
    transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
}

.feature-card:hover {
    transform: translateY(-4px);
    border-color: rgba(125, 211, 252, 0.48);
    background: rgba(15, 23, 42, 0.76);
}

.feature-icon {
    display: grid;
    width: 42px;
    height: 42px;
    place-items: center;
    margin-bottom: 14px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.28), rgba(45, 212, 191, 0.18));
    font-size: 23px;
}

.feature-title {
    color: #f8fafc;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 8px;
}

.feature-text {
    color: #aebed0;
    font-size: 14px;
    line-height: 1.55;
}

.glass-card {
    padding: 26px !important;
}

.section-heading {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0 0 8px;
    color: #f8fafc;
    font-size: 24px;
    line-height: 1.2;
    font-weight: 850;
    letter-spacing: 0;
}

.section-copy {
    position: relative;
    z-index: 1;
    margin: 0 0 22px;
    color: #aebed0;
    font-size: 15px;
    line-height: 1.65;
}

.upload-grid {
    gap: 18px !important;
}

.file-input {
    position: relative;
    z-index: 1;
}

.file-input label {
    color: #e2e8f0 !important;
    font-size: 15px !important;
    font-weight: 800 !important;
}

.file-input,
.file-input > div,
.file-input .wrap {
    border-radius: 20px !important;
}

.file-input [data-testid="file"] {
    min-height: 154px !important;
    border: 1px dashed rgba(125, 211, 252, 0.34) !important;
    border-radius: 20px !important;
    background: rgba(2, 6, 23, 0.34) !important;
    transition: border-color 180ms ease, background 180ms ease, transform 180ms ease;
}

.file-input [data-testid="file"]:hover {
    transform: translateY(-2px);
    border-color: rgba(45, 212, 191, 0.68) !important;
    background: rgba(8, 47, 73, 0.25) !important;
}

.helper-text {
    position: relative;
    z-index: 1;
    margin-top: -8px;
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.45;
}

#run-button {
    position: relative;
    z-index: 1;
    width: 100%;
    min-height: 58px;
    margin-top: 10px;
    border: 0 !important;
    border-radius: 18px !important;
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 52%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 900 !important;
    box-shadow: 0 18px 42px rgba(37, 99, 235, 0.38), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
}

#run-button:hover {
    transform: translateY(-2px);
    filter: brightness(1.07);
    box-shadow: 0 24px 54px rgba(37, 99, 235, 0.48), inset 0 1px 0 rgba(255, 255, 255, 0.28) !important;
}

#run-button:disabled {
    transform: none;
    filter: saturate(0.75) brightness(0.86);
    cursor: wait;
}

.status-panel,
.results-panel {
    position: relative;
    z-index: 1;
    min-height: 116px;
    padding: 18px 18px 16px;
    border: 1px solid rgba(148, 163, 184, 0.17);
    border-radius: 20px;
    background: rgba(2, 6, 23, 0.34);
}

.status-panel p,
.results-panel p {
    margin: 0;
    color: #cbd5e1;
    font-size: 15px;
    line-height: 1.7;
}

.status-panel strong,
.results-panel strong {
    color: #ffffff;
}

.status-ready strong {
    color: #86efac;
}

.status-processing strong {
    color: #fde68a;
}

.status-error strong {
    color: #fca5a5;
}

.status-success strong {
    color: #5eead4;
}

.results-file {
    position: relative;
    z-index: 1;
    margin-top: 14px;
}

.results-file label {
    color: #e2e8f0 !important;
    font-weight: 800 !important;
}

.footer {
    margin-top: 22px;
    padding: 20px;
    text-align: center;
    color: #9fb0c4;
    font-size: 14px;
    line-height: 1.7;
}

.footer strong {
    color: #ffffff;
}

.footer span {
    display: inline-flex;
    margin: 5px 6px 0;
    padding: 5px 10px;
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.55);
    color: #cbd5e1;
}

@media (max-width: 900px) {
    #app-shell {
        padding: 18px 10px 26px;
    }

    .hero-card {
        padding: 32px 22px 26px;
        border-radius: 24px !important;
    }

    .feature-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 560px) {
    .hero-card,
    .glass-card {
        border-radius: 20px !important;
    }

    .feature-grid {
        grid-template-columns: 1fr;
    }

    .glass-card {
        padding: 20px !important;
    }
}
"""

READY_STATUS = """
<div class="status-panel status-ready">
    <p><strong>🟢 Ready</strong></p>
    <p>Upload both files, then run the ranking pipeline.</p>
</div>
"""

READY_RESULTS = """
<div class="results-panel">
    <p><strong>Results will appear here</strong></p>
    <p>Your ranked CSV will be available after a successful run.</p>
</div>
"""


def rank_candidates(job_file, candidates_file, progress=gr.Progress(track_tqdm=True)):
    if job_file is None or candidates_file is None:
        progress(0, desc="Waiting for required files...")
        yield """
        <div class="status-panel status-error">
            <p><strong>🔴 Error</strong></p>
            <p>Please upload both the Job Description (.docx) and Candidate File (.jsonl).</p>
        </div>
        """, READY_RESULTS, None
        return

    progress(0.12, desc="Uploading files...")
    yield """
    <div class="status-panel status-processing">
        <p><strong>🟡 Processing...</strong></p>
        <p>Uploading files and preparing the workspace.</p>
    </div>
    """, """
    <div class="results-panel">
        <p><strong>Ranking in progress</strong></p>
        <p>The AI pipeline is preparing candidate scores.</p>
    </div>
    """, None

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy(job_file, RAW_DIR / "job_description.docx")
    shutil.copy(candidates_file, RAW_DIR / "candidates.jsonl")

    try:
        progress(0.38, desc="Running AI Pipeline...")
        yield """
        <div class="status-panel status-processing">
            <p><strong>🟡 Processing...</strong></p>
            <p>Running AI Pipeline and evaluating candidates.</p>
        </div>
        """, """
        <div class="results-panel">
            <p><strong>Generating rankings</strong></p>
            <p>Semantic ranking is underway. This can take a moment.</p>
        </div>
        """, None

        run_pipeline()

        progress(0.78, desc="Generating rankings...")
        output_csv = OUTPUT_DIR / "submission.csv"

        progress(0.92, desc="Preparing submission...")
        if output_csv.exists():
            progress(1.0, desc="Completed!")
            yield """
            <div class="status-panel status-success">
                <p><strong>✅ Ranking Completed Successfully</strong></p>
                <p>The Top 100 submission file is ready to download.</p>
            </div>
            """, """
            <div class="results-panel status-success">
                <p><strong>✅ Ranking completed</strong></p>
                <p>Download Submission CSV below.</p>
            </div>
            """, str(output_csv)
            return

        yield """
        <div class="status-panel status-error">
            <p><strong>🔴 Error</strong></p>
            <p>Pipeline finished but submission.csv was not generated.</p>
        </div>
        """, """
        <div class="results-panel">
            <p><strong>No CSV found</strong></p>
            <p>The expected output file was not created.</p>
        </div>
        """, None

    except Exception as e:
        yield f"""
        <div class="status-panel status-error">
            <p><strong>🔴 Error</strong></p>
            <p>{str(e)}</p>
        </div>
        """, """
        <div class="results-panel">
            <p><strong>Ranking failed</strong></p>
            <p>Please review the status message and try again.</p>
        </div>
        """, None


with gr.Blocks(
    title="REDROB-RANKER",
    theme=gr.themes.Soft(
        primary_hue="cyan",
        secondary_hue="blue",
        neutral_hue="slate",
        radius_size="lg",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    ),
    css=CUSTOM_CSS,
) as demo:

    with gr.Column(elem_id="app-shell"):
        gr.HTML(
            """
            <section class="hero-card">
                <div class="hero-inner">
                    <div class="hero-kicker">AI Hackathon Demo</div>
                    <h1 class="hero-title">🤖 REDROB-RANKER</h1>
                    <p class="hero-subtitle">AI-Powered Candidate Ranking System</p>
                    <p class="hero-description">
                        Upload a Job Description and Candidate Database.
                        Our AI pipeline evaluates every candidate and produces the Top 100 ranked submissions.
                    </p>
                    <div class="feature-grid">
                        <div class="feature-card">
                            <div class="feature-icon">📄</div>
                            <div class="feature-title">DOCX Parsing</div>
                            <div class="feature-text">Reads the uploaded Job Description</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">👥</div>
                            <div class="feature-title">Candidate Analysis</div>
                            <div class="feature-text">Processes JSONL candidate database</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">🧠</div>
                            <div class="feature-title">AI Ranking</div>
                            <div class="feature-text">Runs semantic ranking pipeline</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">📊</div>
                            <div class="feature-title">CSV Export</div>
                            <div class="feature-text">Generates submission.csv automatically</div>
                        </div>
                    </div>
                </div>
            </section>
            """
        )

        with gr.Row(equal_height=False):
            with gr.Column(scale=7):
                with gr.Group(elem_classes=["glass-card"]):
                    gr.HTML(
                        """
                        <h2 class="section-heading">📤 Upload Files</h2>
                        <p class="section-copy">
                            Add the job description and candidate database to start the ranking workflow.
                        </p>
                        """
                    )

                    with gr.Row(elem_classes=["upload-grid"]):
                        with gr.Column():
                            jd = gr.File(
                                label="📄 Job Description (.docx)",
                                file_types=[".docx"],
                                elem_classes=["file-input"],
                            )
                            gr.HTML(
                                """
                                <p class="helper-text">
                                    Supported format:<br>
                                    Microsoft Word (.docx)
                                </p>
                                """
                            )

                        with gr.Column():
                            candidates = gr.File(
                                label="👥 Candidate File (.jsonl)",
                                file_types=[".jsonl"],
                                elem_classes=["file-input"],
                            )
                            gr.HTML(
                                """
                                <p class="helper-text">
                                    Supported format:<br>
                                    JSON Lines (.jsonl)
                                </p>
                                """
                            )

                    run_btn = gr.Button(
                        "🚀 Run AI Ranking",
                        elem_id="run-button",
                        variant="primary",
                    )

                    status = gr.HTML(value=READY_STATUS)

            with gr.Column(scale=5):
                with gr.Group(elem_classes=["glass-card"]):
                    gr.HTML(
                        """
                        <h2 class="section-heading">📊 Results</h2>
                        <p class="section-copy">
                            Download the generated submission file when ranking is complete.
                        </p>
                        """
                    )
                    result_message = gr.HTML(value=READY_RESULTS)
                    csv = gr.File(
                        label="Download Submission CSV",
                        elem_classes=["results-file"],
                    )

        gr.HTML(
            """
            <footer class="footer">
                <strong>Built for the RedRob AI Hackathon</strong><br>
                Powered by
                <span>Gradio</span>
                <span>Python</span>
                <span>AI Candidate Ranking Pipeline</span>
                <span>GitHub Ready</span>
            </footer>
            """
        )

    run_event = run_btn.click(
        lambda: gr.update(interactive=False, value="⏳ Running AI Ranking..."),
        inputs=None,
        outputs=run_btn,
        queue=False,
    )

    run_event.then(
        rank_candidates,
        inputs=[jd, candidates],
        outputs=[status, result_message, csv],
    ).then(
        lambda: gr.update(interactive=True, value="🚀 Run AI Ranking"),
        inputs=None,
        outputs=run_btn,
        queue=False,
    )

demo.launch()