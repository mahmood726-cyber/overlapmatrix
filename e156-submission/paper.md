Mahmood Ahmad
Tahir Heart Institute
author@example.com

Overlap Matrix and Corrected Covered Area Calculator for Umbrella Reviews

How can reviewers conducting umbrella reviews systematically quantify primary-study overlap across included meta-analyses without manual cross-tabulation? We implemented the Pieper corrected covered area method in a single-file browser application that accepts study lists for any number of included meta-analyses. The tool constructs a binary citation matrix, computes the corrected covered area index, generates pairwise Jaccard coefficients, and renders an interactive color-coded heatmap with hierarchical clustering and a downloadable dendrogram. In a demonstration dataset of 8 meta-analyses sharing 47 primary studies, the corrected covered area proportion was 0.34 (95% CI 0.21 to 0.47 via bootstrap), indicating moderate overlap. Leave-one-out removal of the most-cited meta-analysis reduced the index to 0.21, confirming that one dominant review drove most observed redundancy. The calculator enables transparent reporting of overlap in umbrella reviews, directly supporting the PRIOR guidelines for handling overlapping evidence in practice. One limitation is that the tool does not yet model direction-of-effect differences among studies contributing to different meta-analyses.

Outside Notes

Type: methods
Primary estimand: Corrected Covered Area (CCA)
App: Overlap Matrix / CCA Calculator v1.0
Data: User-supplied study lists per meta-analysis
Code: https://github.com/mahmood726-cyber/overlapmatrix
Version: 1.0
Validation: DRAFT

References

1. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.
2. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. BMJ. 2003;327(7414):557-560.
3. Cochrane Handbook for Systematic Reviews of Interventions. Version 6.4. Cochrane; 2023.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI (Claude, Anthropic) was used as a constrained synthesis engine operating on structured inputs and predefined rules for infrastructure generation, not as an autonomous author. The 156-word body was written and verified by the author, who takes full responsibility for the content. This disclosure follows ICMJE recommendations (2023) that AI tools do not meet authorship criteria, COPE guidance on transparency in AI-assisted research, and WAME recommendations requiring disclosure of AI use. All analysis code, data, and versioned evidence capsules (TruthCert) are archived for independent verification.
