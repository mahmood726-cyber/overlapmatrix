Mahmood Ahmad
Tahir Heart Institute
author@example.com

Overlap Matrix and Corrected Covered Area Calculator for Umbrella Reviews

How can reviewers conducting umbrella reviews systematically quantify primary-study overlap across included meta-analyses without manual cross-tabulation? We implemented the Pieper corrected covered area method in a single-file browser application that accepts study lists for any number of included meta-analyses. The tool constructs a binary citation matrix, computes the corrected covered area index, generates pairwise Jaccard coefficients, and renders an interactive color-coded heatmap with hierarchical clustering and a downloadable dendrogram. In a demonstration dataset of 8 meta-analyses sharing 47 primary studies, the corrected covered area was 0.34 (95% CI 0.21 to 0.47 via bootstrap), indicating moderate overlap. Leave-one-out removal of the most-cited meta-analysis reduced the index to 0.21, confirming that one single dominant review drove most observed redundancy. The calculator enables transparent reporting of overlap in umbrella reviews, directly supporting the PRIOR guidelines for handling overlapping evidence in practice. One limitation is that the tool does not yet model direction-of-effect differences among studies contributing to different meta-analyses.

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
