import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = PROJECT_ROOT / "examples" / "example_data" / "cyp_substrates_demo.csv"


def test_cli_analyze_generates_summary_outputs(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "cypchemspace.cli",
            "analyze",
            str(EXAMPLE),
            "--out-dir",
            str(tmp_path),
            "--n-bits",
            "128",
            "--k",
            "3",
            "--n-permutations",
            "19",
            "--random-state",
            "11",
            "--embedding-method",
            "pca",
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "embedding.csv").exists()
    assert (tmp_path / "summary.csv").exists()
    assert (tmp_path / "cypchemspace_umap.png").exists()
