#!/usr/bin/env python3
"""Run the experiment programs exactly as they are printed in the manual.

The program text lives in ``content.py`` as ``code["lines"]``.  This harness
writes those exact lines to a file and runs it, so the captured output is
guaranteed to come from the code the student sees.  Nothing here is retyped.

Usage:
    python3 run_experiments.py 03 05 12       # run specific experiments
    python3 run_experiments.py --list         # show which have runnable code
"""
import os
import subprocess
import sys

import content

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, "runs")
OUT = os.path.join(HERE, "captures")

# Experiment number -> the file name the program expects to be called.
PROGRAM_NAME = {
    "01": "gen_basics.py",
    "02": "gan_mnist.py",
    "03": "autoencoder_vae.py",
    "04": "transformer_demo.py",
    "05": "fairness_metrics.py",
    "06": "nlp_reviews.py",
    "07": "fashion_cnn_gan.py",
    "08": None,          # prompt-only experiment, no program
    "09": "gemini_sdk.py",
    "10": "agent_tools.py",
    "11": "finetune_lora.py",
    "12": "semantic_search.py",
    "13": "rag_medical.py",
    "14": "recruitment_fairness.py",
    "15": "app.py",      # plus test_app.py and monitor.py
}

# Experiment 15 prints three files separated by banner comments.
MULTI_FILE = {
    "15": [
        ("# --------------- app.py (a stub application under test) ---------------",
         "# --------------------- test_app.py (pytest suite) ---------------------",
         "app.py"),
        ("# --------------------- test_app.py (pytest suite) ---------------------",
         "# ------------------- monitor.py (monitoring report) -------------------",
         "test_app.py"),
        ("# ------------------- monitor.py (monitoring report) -------------------",
         None,
         "monitor.py"),
    ],
}


def split_multi(no, lines):
    """Split a multi-file program into its parts."""
    text = "\n".join(lines)
    parts = {}
    for start, end, name in MULTI_FILE[no]:
        i = text.index(start)
        j = len(text) if end is None else text.index(end)
        parts[name] = text[i:j].rstrip()
    return parts


def prepare(no):
    """Write the experiment's program(s) into runs/<no>/ and return the paths."""
    exp = next(e for e in content.EXPERIMENTS if e["no"] == no)
    code = exp.get("code")
    if not code:
        return None, "no program for this experiment"
    d = os.path.join(RUN, no)
    os.makedirs(d, exist_ok=True)

    if no in MULTI_FILE:
        for name, body in split_multi(no, code["lines"]).items():
            with open(os.path.join(d, name), "w") as f:
                f.write(body + "\n")
        return d, "multi-file"

    name = PROGRAM_NAME[no]
    with open(os.path.join(d, name), "w") as f:
        f.write("\n".join(code["lines"]) + "\n")
    return d, name


def run(no, timeout=1800):
    d, info = prepare(no)
    if d is None:
        print(f"exp {no}: {info}")
        return None
    os.makedirs(OUT, exist_ok=True)
    log = os.path.join(OUT, f"exp{no}.log")
    env = dict(os.environ)
    env["MPLBACKEND"] = "Agg"
    env["PYTHONUNBUFFERED"] = "1"
    env["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
    env["TRANSFORMERS_VERBOSITY"] = "error"
    env["TOKENIZERS_PARALLELISM"] = "false"
    # Cap BLAS/OpenMP threads: several torch runs at once overrun memory.
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                "NUMEXPR_NUM_THREADS"):
        env[var] = "2"

    if no == "15":
        # Run the pytest suite, then the monitoring script, into one log.
        cmds = [[sys.executable, "-m", "pytest", "-v", "test_app.py"],
                [sys.executable, "-u", "monitor.py"]]
    elif no in MULTI_FILE:
        cmds = [[sys.executable, "-c", "print('multi-file experiment')"]]
    else:
        cmds = [[sys.executable, "-u", PROGRAM_NAME[no]]]

    print(f"exp {no}: running {info} in {d}")
    rc = 0
    with open(log, "w") as f:
        for cmd in cmds:
            f.write("$ " + " ".join(cmd) + "\n")
            f.flush()
            p = subprocess.run(cmd, cwd=d, stdout=f, stderr=subprocess.STDOUT,
                               timeout=timeout, env=env)
            rc = rc or p.returncode
            f.write("\n")
    print(f"exp {no}: exit {rc}, log {log}")
    return log


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--list" in sys.argv:
        for e in content.EXPERIMENTS:
            has = "program" if e.get("code") else "no program"
            print(f"  {e['no']}  {has:12s} {e['title'][:56]}")
        sys.exit(0)
    if not args:
        print(__doc__)
        sys.exit(1)
    for no in args:
        try:
            run(no)
        except subprocess.TimeoutExpired:
            print(f"exp {no}: TIMEOUT")
