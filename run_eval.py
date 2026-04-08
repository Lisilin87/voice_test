from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INTEGRATED_DIR = ROOT / "integrated_voice_eval"
VOICE_TEST_DIR = ROOT / "voice_test"


def main() -> int:
    command = [
        sys.executable,
        str(INTEGRATED_DIR / "run_eval.py"),
        "--test-case-file",
        str(VOICE_TEST_DIR / "eval_cases.csv"),
        "--audio-input-dir",
        str(VOICE_TEST_DIR / "voice_input_file"),
        "--pre-wav-path",
        str(VOICE_TEST_DIR / "output_recording.wav"),
        "--result-file",
        str(VOICE_TEST_DIR / "eval_results.csv"),
        "--sheet",
        "Sheet2",
    ]
    return subprocess.call(command, cwd=str(INTEGRATED_DIR))


if __name__ == "__main__":
    raise SystemExit(main())
