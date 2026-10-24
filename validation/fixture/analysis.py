def summarize_displacements(displacements, fps=50):
    """Prepare one-frame displacement samples for downstream analysis."""
    return [0.0 if value is None else value * fps for value in displacements]
