# Template validation

Validated 24 October 2026. This is an inactive template, not a deployed review service or CI gate.

## Structural checks

- Bundled `skill-creator/scripts/quick_validate.py`: **Skill is valid!**
- Parsed UI metadata; invocation policy and default skill reference are consistent.
- All six local Markdown links in the initial package resolved inside the package.
- No active `AGENTS.md` or `.agents` directory was created in the package. The default snippet is a text file; the skill is outside discovery locations.
- The validator needed PyYAML, which was placed in the workspace-local `.review-template-build/python` scratch folder. No review skill, global instructions or agent settings were installed or activated.

## Independent design audit

A fresh-context subagent read the guide, session snippet, skill, metadata, role prompts and report template. It reported no actionable design defects. Its audit covered scope and permissions, reviewer independence, prevention of recursive delegation, candidate identity, stale evidence, decision rules and the bounded loop.

This was a static review of instructions. It did not establish installation, discovery or runtime enforcement.

## Independent forward test

A separate fresh-context subagent used the skill in reviewer-only mode on the synthetic files in `fixture/`. It was given the raw request and candidate without the expected defects. It ran the supplied tests and its own direct probes, without editing the fixture.

Candidate `fixture/analysis.py` SHA-256:

`E0C40747746552A12E338058709D08F38ECC50E2F22747F0099A39F1DC95EF1E`

Observed results:

| Evidence | Result |
| --- | --- |
| Python 3.12.14, `-B -m unittest -v test_analysis.py`, fixture working directory | Both supplied tests passed |
| Independent probe of `[2.0, None, 0.0, -1.25]` at default frame rate | Returned `[100.0, 0.0, 0.0, -62.5]` |
| Same probe at `fps=25` | Returned `[50.0, 0.0, 0.0, -31.25]` |
| Empty input, slot order, sample count, measured zero and input non-mutation | Passed the independent checks |
| Fixture file hashes before and after review | Unchanged |

The reviewer identified two confirmed violations of the written requirements:

1. P1: multiplying displacement by frame rate changes the output from the required pixels/frame to pixels/second.
2. P2: converting `None` to zero loses the distinction between missing data and measured zero.

It recommended **CHANGES_REQUIRED**, explicitly identifying that the implementation-authored test encoded both wrong expectations. Both findings were grounded in execution and the request; no extra user decision was needed.

The synthetic code intentionally remains incorrect so this example can be repeated. It is a review fixture, not an analysis utility to use on research data.

## Limits

This validates package structure, an independent design audit and one reviewer-only behavior example. It does not validate the entire orchestration/repair loop, reviewer timeout recovery, all programming languages, live project integration, model diversity, automatic discovery, CI enforcement, production behavior or scientific validity. No empirical defect-detection rate or guarantee is claimed.
