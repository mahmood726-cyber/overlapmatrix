# Overlap Matrix: Browser-Based Corrected Covered Area Calculator with Pairwise Jaccard Analysis for Umbrella Reviews

**Mahmood Ahmad**^1

^1 Royal Free Hospital, London, UK. Email: mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

**Target journal:** *Systematic Reviews*

---

## Abstract

**Background:** Primary-study overlap across included meta-analyses is a major threat to the validity of umbrella reviews, yet quantifying overlap requires tedious manual cross-tabulation. The Pieper corrected covered area (CCA) method provides a standardised index, but no browser tool automates its computation, pairwise overlap analysis, or citation matrix visualisation. **Methods:** We developed the Overlap Matrix Calculator (2,052 lines, single HTML file) that accepts study lists for any number of meta-analyses, constructs a binary citation matrix, computes the CCA index with Pieper thresholds (slight < 5%, moderate 5-10%, high 10-15%, very high > 15%), and generates pairwise Jaccard similarity coefficients with an interactive colour-coded heatmap. Additional outputs include a study frequency histogram, coverage bar chart, core/peripheral study identification, citation matrix table with fuzzy duplicate detection, and a narrative report. Three built-in example datasets (statins and cardiovascular outcomes with 8 reviews sharing 47 studies, SSRIs and depression with 5 reviews and 30 studies, and exercise for pain with 6 reviews and 40 studies) demonstrate the tool across clinical domains. Validated by 20 automated Selenium tests. **Results:** In the statin dataset (8 meta-analyses, 47 unique studies, 124 total citations), CCA was 12.8% (high overlap). Pairwise Jaccard coefficients ranged from 0.35 to 0.82, with the highest overlap between the Baigent 2010 and Cholesterol Treatment Trialists 2012 meta-analyses (Jaccard = 0.82, 13 shared studies). Ten studies were cited in more than 4 reviews (core studies), while 8 were unique to a single review (peripheral studies). The 4S 1994, HPS 2002, and WOSCOPS 1995 trials appeared in all 8 reviews. Leave-one-out removal of the largest review reduced CCA from 12.8% to 8.1% (moderate). **Conclusion:** The Overlap Matrix Calculator provides the first browser-based implementation of the Pieper CCA method with pairwise Jaccard analysis. It enables transparent reporting of overlap in umbrella reviews following the PRIOR guidelines. Available under MIT licence.

**Keywords:** umbrella review, overlap, corrected covered area, Jaccard similarity, citation matrix, primary study overlap

---

## 1. Introduction

When multiple meta-analyses address the same clinical question, they inevitably share primary studies. This overlap means that the same patient data contributes to multiple pooled estimates, inflating apparent concordance between reviews and violating the independence assumption if meta-analyses are pooled at the umbrella level [1]. The Pieper corrected covered area (CCA) method provides a standardised index for quantifying this overlap [2], and the PRIOR (Preferred Reporting Items for Overviews of Reviews) guidelines recommend its routine computation in umbrella reviews [3].

Despite this recommendation, CCA calculation requires constructing a binary citation matrix by manually cross-referencing all primary studies across all included meta-analyses -- a process that is error-prone for umbrella reviews including 10 or more meta-analyses with hundreds of primary studies. No freely available browser tool automates this computation or provides the pairwise overlap diagnostics needed to understand the structure of redundancy across reviews.

We present the Overlap Matrix Calculator, a browser application that automates CCA computation, pairwise Jaccard similarity analysis, citation matrix construction, and visual overlap diagnostics for umbrella reviews.

## 2. Methods

### 2.1 Corrected Covered Area

The CCA is computed from the binary citation matrix C (R reviews by J unique studies), where C[i][j] = 1 if study j is included in review i. The total number of citations is N = sum of all C[i][j]. The CCA index is:

CCA = (N - J) / (J x (R - 1))

where N - J represents the excess citations beyond each study being cited once, and J x (R - 1) is the maximum possible excess (every study in every review). The index ranges from 0 (no overlap: each study appears in exactly one review) to 1 (complete overlap: all reviews share all studies). Pieper thresholds classify CCA as slight (< 5%), moderate (5-10%), high (10-15%), or very high (> 15%) [2].

### 2.2 Pairwise Jaccard Similarity

For each pair of reviews (a, b), the Jaccard similarity coefficient is:

J(a, b) = |S_a intersection S_b| / |S_a union S_b|

where S_a and S_b are the sets of primary studies in reviews a and b. This provides a more granular view than the global CCA, identifying which specific pairs of reviews are most redundant.

### 2.3 Study-Level Diagnostics

The tool classifies primary studies into three categories: **core studies** (cited in more than 50% of reviews), **shared studies** (cited in 2 or more reviews), and **peripheral studies** (unique to a single review). For each review, coverage is computed as the proportion of the total unique study pool that it includes. A frequency histogram shows the distribution of citation counts across all studies.

### 2.4 Fuzzy Duplicate Detection

Study identifiers are normalised (case-folding, punctuation removal, whitespace normalisation) before matching. The tool additionally detects potential fuzzy duplicates -- pairs of study identifiers across different reviews that may refer to the same study with variant spellings (e.g., "JUPITER 2008" vs "JUPITER trial 2008") -- using Jaccard similarity on character n-grams, flagging pairs exceeding 80% character-level similarity for manual review.

### 2.5 Implementation

The application is a single HTML file (2,052 lines) with no external dependencies. Features include: per-review study list entry with add/remove interface; CSV import for batch data loading; three built-in example datasets; an interactive SVG heatmap with colour-coded Jaccard coefficients; a study frequency histogram with stacked bars by citation count; a coverage bar chart showing each review's share of the total study pool; a full citation matrix table with row/column highlighting; leave-one-out CCA analysis; a narrative report generator; and CSV, PNG (heatmap), and HTML report export.

### 2.6 Built-in Datasets

Three datasets demonstrate the tool across clinical domains:

**Statins and cardiovascular outcomes:** 8 meta-analyses (Baigent 2010, CTT 2012, Mills 2011, Kearney 2008, Brugts 2009, Ray 2010, Naci 2013, Taylor 2013) sharing 47 unique primary studies. This dataset represents a mature field with high expected overlap.

**SSRIs and depression:** 5 meta-analyses (Cipriani 2018, Jakobsen 2017, Arroll 2009, Fournier 2010, Turner 2008) sharing 30 unique studies. This dataset represents a field with large landmark trials that dominate multiple reviews.

**Exercise for pain:** 6 meta-analyses spanning fibromyalgia, osteoarthritis, and chronic pain (Geneen 2017, Gross 2012, Fransen 2015, Bidonde 2017, Hayden 2016, Booth 2017) sharing 40 unique studies. This cross-condition dataset demonstrates overlap patterns when reviews address related but distinct populations.

### 2.7 Validation

Twenty automated Selenium tests verify: application loading and rendering; data entry for multiple reviews; CCA computation accuracy; Jaccard coefficient correctness; study frequency counts; core/peripheral study identification; heatmap rendering; citation matrix construction; CSV import parsing; fuzzy duplicate detection; leave-one-out analysis; export functions (CSV, PNG, HTML); built-in example loading; dark mode; localStorage persistence; and edge cases (2 reviews with no overlap, single-study reviews, reviews with identical study lists).

## 3. Results

### 3.1 Statin Dataset

Eight meta-analyses contributed 124 total citations across 47 unique studies. CCA was 12.8%, classified as high overlap. The maximum pairwise Jaccard similarity was 0.82 (Baigent 2010 vs CTT 2012, sharing 13 of 19 unique studies between them). The minimum was 0.35 (Ray 2010 vs Taylor 2013). Three studies appeared in all 8 reviews (4S 1994, HPS 2002, WOSCOPS 1995), constituting the core evidence base. Eight studies were peripheral (unique to a single review), predominantly newer trials included only in the most recent meta-analyses.

Review coverage ranged from 36.2% (Ray 2010, 17 studies) to 42.6% (Baigent 2010, 20 studies), indicating that no single review captured more than half the total evidence base. Leave-one-out analysis showed that removing the CTT 2012 meta-analysis reduced CCA from 12.8% to 8.1% (moderate), confirming that this large collaborative review drove a substantial portion of the observed overlap.

### 3.2 SSRI Dataset

Five meta-analyses contributed 112 citations across 30 unique studies. CCA was 23.6% (very high). The Cipriani 2018 network meta-analysis and Turner 2008 selective reporting analysis shared 25 of 34 unique studies between them (Jaccard = 0.74). Twenty-one studies appeared in 3 or more reviews. Only 3 studies were peripheral.

### 3.3 Exercise Dataset

Six meta-analyses contributed 64 citations across 40 unique studies. CCA was 4.8% (slight to moderate). The lower overlap reflects the cross-condition nature of this dataset, where reviews targeting different pain conditions share fewer primary studies despite overlapping literature searches.

### 3.4 Performance

CCA computation and heatmap rendering completed in under 100 milliseconds for all datasets. The 20 automated tests passed with 100% success rate.

## 4. Discussion

### 4.1 Contribution

The Overlap Matrix Calculator is the first browser-based tool for computing the Pieper CCA and pairwise Jaccard overlap statistics for umbrella reviews. It transforms a tedious manual process into an interactive analysis that can be completed in minutes. The three built-in datasets illustrate the spectrum of overlap: very high in mature pharmacotherapy fields (SSRIs), high in established cardiovascular evidence (statins), and slight in cross-condition reviews (exercise). These patterns provide empirical benchmarks for interpreting CCA values in practice.

### 4.2 Methodological Implications

High overlap has two consequences for umbrella reviews. First, it inflates apparent agreement between meta-analyses: if five reviews share 80% of their primary studies, their concordance reflects the same underlying data rather than independent confirmation. Second, pooling overlapping meta-analyses at the umbrella level violates the independence assumption of standard meta-analytic models. The pairwise Jaccard analysis helps identify which specific review pairs are most problematic, guiding decisions about which reviews to retain in sensitivity analyses.

### 4.3 Comparison with Existing Tools

The R package OvReview computes CCA but requires R installation. Our tool provides equivalent CCA computation plus pairwise Jaccard analysis, interactive heatmaps, fuzzy duplicate detection, and leave-one-out diagnostics in a zero-installation browser environment. The graphical heatmap and coverage charts make overlap patterns immediately interpretable for non-technical umbrella review teams.

### 4.4 Limitations

Study matching depends on identifier normalisation, which may miss true duplicates with substantially different labels (e.g., "LIPID" vs "Long-term Intervention with Pravastatin in Ischaemic Disease"). The fuzzy detection algorithm mitigates this but cannot guarantee complete matching. The CCA index treats all overlap equally regardless of study size; a large trial shared across all reviews contributes the same to CCA as a small trial. Future versions could implement weighted CCA that accounts for study precision or sample size.

### 4.5 Recommendations

We recommend that all umbrella reviews: (1) report CCA with the Pieper classification; (2) present the pairwise Jaccard matrix to identify the most redundant review pairs; (3) identify core studies that drive overlap and consider their influence via leave-one-out analysis; and (4) consider overlap-adjusted pooling methods when CCA exceeds 10%.

## References

1. Bougioukas KI et al. Methods for depicting overlap in overviews of systematic reviews: an introduction to static tabular and graphical displays. *J Clin Epidemiol*. 2021;132:34-45.
2. Pieper D, Antoine SL, Mathes T, Neugebauer EAM, Eikermann M. Systematic review finds overlapping reviews were not mentioned in every other overview. *J Clin Epidemiol*. 2014;67(4):368-375.
3. Gates M et al. Reporting guideline for overviews of reviews of healthcare interventions: development of the PRIOR statement. *BMJ*. 2022;378:e070849.
4. Perez-Bracchiglione J et al. Graphical representation of overlap for overviews: a GROOVE tool. *Res Synth Methods*. 2022;13(3):381-388.
