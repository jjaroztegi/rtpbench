from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
# the stacks' files (compose.yaml, Dockerfile, corpus, targets): an installed rtpbench carries
# them in its package; a checkout keeps them at its root, as the image does the corpus (/app)
ROOT = PACKAGE if (PACKAGE / "compose.yaml").exists() else PACKAGE.parents[1]
