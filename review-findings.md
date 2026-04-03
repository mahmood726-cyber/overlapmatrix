# OverlapMatrix — Code Review Findings

**Reviewer:** Claude Opus 4.6 (1M context)
**Date:** 2026-04-03
**File:** overlap-matrix.html (2,052 lines)

## P0 — Critical (must fix)

### P0-1: CSV injection — `csvCell()` missing formula guard
**Line:** 718-722
**Issue:** The `csvCell()` function only handles commas, quotes, and newlines. It does NOT guard against CSV formula injection — cells starting with `=`, `+`, `@`, `\t`, `\r` can execute formulas in Excel/Sheets when the CSV is opened.
**Fix:** Prepend `'` to cells starting with `=+@\t\r` (per rules, NOT `-` which corrupts negative numbers).

### P0-2: Missing skip-nav link
**Issue:** No skip navigation link for keyboard/screen reader users. The sticky header means keyboard users must tab through all header buttons before reaching main content.
**Fix:** Add `<a href="#app-main" class="skip-nav">Skip to content</a>` before header, with CSS to position off-screen until focused.

## P1 — Important

### P1-1: No `aria-selected` keyboard navigation for tabs
**Line:** 869-885
**Issue:** Tab keyboard handler only supports Enter/Space. Arrow key navigation between tabs is not implemented (ARIA tabs pattern requires Left/Right arrow keys).

### P1-2: `exportHtmlReport()` uses string concatenation to avoid `</script>` but inconsistently
**Line:** 1759
**Issue:** Uses `'<' + '/p>'` and `'<' + '/body><' + '/html>'` which is correct. However, if future edits add script blocks to the report, the pattern must be maintained.

### P1-3: No `escHtml` on study data in `csvCell` export
**Issue:** Study names from user input flow into CSV without HTML escaping. While CSV is not HTML, the HTML report export does use `escHtml` correctly.

## P2 — Minor

### P2-1: Canvas charts not accessible
**Issue:** Canvas elements lack `aria-label` attributes describing their content.

### P2-2: No `<main>` landmark explicitly (uses class `app-main`)
**Issue:** The main content area uses `<main class="app-main">` which is correct, but there's no `role="main"` fallback for older browsers.

### P2-3: Dark mode state not persisted in `aria-pressed`
**Issue:** The dark mode toggle button lacks `aria-pressed` attribute.

## Summary

| Severity | Count |
|----------|-------|
| P0       | 2     |
| P1       | 3     |
| P2       | 3     |
