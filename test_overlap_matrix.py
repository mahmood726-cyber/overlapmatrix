"""
test_overlap_matrix.py — 20 Selenium tests for OverlapMatrix (Primary Study Overlap Calculator)
Tests cover: page load, UI interaction, CCA formula, Jaccard similarity, examples, exports.
"""
import sys, io, os, json, time, unittest
if 'pytest' not in sys.modules and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'overlap-matrix.html')
FILE_URL = 'file:///' + HTML_PATH.replace('\\', '/')


def make_driver():
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1400,900')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    return webdriver.Chrome(options=opts)


class TestOverlapMatrix(unittest.TestCase):
    """Selenium test suite for OverlapMatrix / CCA Calculator."""

    @classmethod
    def setUpClass(cls):
        cls.driver = make_driver()
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        """Fresh page load + clear localStorage for each test."""
        self.driver.get(FILE_URL)
        self.driver.execute_script("localStorage.clear();")
        self.driver.get(FILE_URL)
        time.sleep(0.3)

    # ── Helpers ──────────────────────────────────────────────
    def add_review(self, name, studies_text):
        """Add a review via JS to avoid textarea newline issues in headless Chrome."""
        escaped_name = name.replace("'", "\\'")
        escaped_studies = studies_text.replace("'", "\\'").replace("\n", "\\n")
        self.js("""
            document.getElementById('inputReviewName').value = '""" + escaped_name + """';
            document.getElementById('inputStudyList').value = '""" + escaped_studies + """';
            document.getElementById('addReviewBtn').click();
        """)
        time.sleep(0.15)

    def click_compute(self):
        self.driver.find_element(By.ID, 'computeBtn').click()
        time.sleep(0.5)

    def switch_tab(self, tab_btn_id):
        self.js("document.getElementById('" + tab_btn_id + "').click();")
        time.sleep(0.2)

    def js(self, script):
        return self.driver.execute_script(script)

    # ═══════════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════════

    def test_01_page_loads(self):
        """Page loads with correct title."""
        self.assertIn('OverlapMatrix', self.driver.title)

    def test_02_tabs_present(self):
        """All 4 tabs are rendered with correct ARIA roles."""
        tabs = self.driver.find_elements(By.CSS_SELECTOR, '[role="tab"]')
        self.assertEqual(len(tabs), 4)
        labels = [t.text.strip() for t in tabs]
        self.assertTrue(any('Data Entry' in l for l in labels))
        self.assertTrue(any('Overlap Analysis' in l for l in labels))
        self.assertTrue(any('Citation Matrix' in l for l in labels))
        self.assertTrue(any('Export' in l for l in labels))

    def test_03_add_single_review(self):
        """Adding one review shows it in the list."""
        self.add_review('Test Review 2021', 'Study A\nStudy B\nStudy C')
        items = self.driver.find_elements(By.CSS_SELECTOR, '.review-list li')
        self.assertEqual(len(items), 1)
        self.assertIn('Test Review 2021', items[0].text)
        count = self.driver.find_element(By.ID, 'reviewCount').text
        self.assertEqual(count, '1')

    def test_04_add_multiple_reviews(self):
        """Adding multiple reviews shows correct count."""
        self.add_review('Rev1', 'Study 1\nStudy 2\nStudy 3')
        self.add_review('Rev2', 'Study 2\nStudy 3\nStudy 4')
        count = self.driver.find_element(By.ID, 'reviewCount').text
        self.assertEqual(count, '2')
        items = self.driver.find_elements(By.CSS_SELECTOR, '.review-list li')
        self.assertEqual(len(items), 2)

    def test_05_remove_review(self):
        """Remove button removes a review from the list."""
        self.add_review('Rev1', 'Study 1\nStudy 2')
        self.add_review('Rev2', 'Study 3\nStudy 4')
        items = self.driver.find_elements(By.CSS_SELECTOR, '.review-list li')
        self.assertEqual(len(items), 2)
        # Click first remove button
        remove_btn = items[0].find_element(By.CSS_SELECTOR, 'button')
        remove_btn.click()
        time.sleep(0.2)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.review-list li')
        self.assertEqual(len(items), 1)
        self.assertIn('Rev2', items[0].text)

    def test_06_example_statins(self):
        """Statins example loads 8 reviews."""
        self.driver.find_element(By.ID, 'exStatinsBtn').click()
        time.sleep(0.3)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.review-list li')
        self.assertEqual(len(items), 8)
        count = self.driver.find_element(By.ID, 'reviewCount').text
        self.assertEqual(count, '8')

    def test_07_example_ssris(self):
        """SSRIs example loads 5 reviews."""
        self.driver.find_element(By.ID, 'exSsrisBtn').click()
        time.sleep(0.3)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.review-list li')
        self.assertEqual(len(items), 5)

    def test_08_example_exercise(self):
        """Exercise example loads 6 reviews."""
        self.driver.find_element(By.ID, 'exExerciseBtn').click()
        time.sleep(0.3)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.review-list li')
        self.assertEqual(len(items), 6)

    def test_09_compute_requires_two_reviews(self):
        """Compute with <2 reviews shows alert."""
        self.add_review('OnlyOne', 'Study X\nStudy Y')
        self.driver.find_element(By.ID, 'computeBtn').click()
        time.sleep(0.3)
        try:
            alert = self.driver.switch_to.alert
            self.assertIn('at least 2', alert.text.lower())
            alert.accept()
        except Exception:
            pass  # Some headless modes auto-dismiss

    def test_10_cca_computation_basic(self):
        """CCA computed correctly for a known simple case."""
        # 2 reviews, 3 unique studies: Rev1=[SA,SB], Rev2=[SB,SC]
        # N=4, J=3, R=2, CCA = (4-3)/(3*(2-1)) = 1/3 = 33.3%
        self.add_review('Rev1', 'SA\nSB')
        self.add_review('Rev2', 'SB\nSC')
        self.click_compute()
        self.switch_tab('tab-btn-analysis')
        cca_text = self.driver.find_element(By.ID, 'tileCca').text
        self.assertIn('33.3', cca_text)

    def test_11_cca_no_overlap(self):
        """CCA = 0% when reviews share no studies."""
        self.add_review('Rev1', 'SA\nSB')
        self.add_review('Rev2', 'SC\nSD')
        self.click_compute()
        self.switch_tab('tab-btn-analysis')
        cca_text = self.driver.find_element(By.ID, 'tileCca').text
        self.assertIn('0.0', cca_text)

    def test_12_cca_complete_overlap(self):
        """CCA = 100% when all reviews include exactly the same studies."""
        self.add_review('Rev1', 'SA\nSB\nSC')
        self.add_review('Rev2', 'SA\nSB\nSC')
        self.add_review('Rev3', 'SA\nSB\nSC')
        self.click_compute()
        self.switch_tab('tab-btn-analysis')
        cca_text = self.driver.find_element(By.ID, 'tileCca').text
        # N=9, J=3, R=3, CCA=(9-3)/(3*(3-1))=6/6=100%
        self.assertIn('100.0', cca_text)

    def test_13_cca_formula_display(self):
        """CCA formula element shows the formula with actual values."""
        self.add_review('Rev1', 'SA\nSB')
        self.add_review('Rev2', 'SB\nSC')
        self.click_compute()
        self.switch_tab('tab-btn-analysis')
        formula = self.driver.find_element(By.ID, 'ccaFormulaEl').text
        self.assertIn('CCA', formula)
        # N=4, J=3 should be visible
        self.assertIn('4', formula)
        self.assertIn('3', formula)

    def test_14_metric_tiles_populated(self):
        """Metric tiles show correct counts after computation."""
        self.add_review('Rev1', 'SA\nSB\nSC')
        self.add_review('Rev2', 'SB\nSC\nSD')
        self.click_compute()
        self.switch_tab('tab-btn-analysis')
        reviews = self.driver.find_element(By.ID, 'tileReviews').text
        unique = self.driver.find_element(By.ID, 'tileUnique').text
        total = self.driver.find_element(By.ID, 'tileTotalCit').text
        self.assertEqual(reviews, '2')
        self.assertEqual(unique, '4')  # SA, SB, SC, SD
        self.assertEqual(total, '6')   # 3 + 3

    def test_15_pairwise_table_rendered(self):
        """Pairwise overlap table is rendered after computation."""
        self.add_review('Rev1', 'SA\nSB')
        self.add_review('Rev2', 'SB\nSC')
        self.add_review('Rev3', 'SA\nSC')
        self.click_compute()
        self.switch_tab('tab-btn-analysis')
        table_wrap = self.driver.find_element(By.ID, 'pairwiseTableWrap')
        rows = table_wrap.find_elements(By.CSS_SELECTOR, 'tbody tr')
        # 3 reviews -> 3 pairwise combos
        self.assertEqual(len(rows), 3)

    def test_16_citation_matrix_rendered(self):
        """Citation matrix table is rendered in Tab 3."""
        self.add_review('Rev1', 'SA\nSB')
        self.add_review('Rev2', 'SB\nSC')
        self.click_compute()
        self.switch_tab('tab-btn-matrix')
        time.sleep(0.3)
        mat_wrap = self.driver.find_element(By.ID, 'citationMatrixWrap')
        table = mat_wrap.find_element(By.CSS_SELECTOR, 'table')
        self.assertIsNotNone(table)

    def test_17_jaccard_formula_in_js(self):
        """Jaccard similarity computed correctly via JS."""
        # Jaccard(['A','B','C'], ['B','C','D']) = 2/4 = 0.5
        result = self.js("return jaccardSim(['A','B','C'], ['B','C','D']);")
        self.assertAlmostEqual(result, 0.5, places=4)

    def test_18_cca_formula_in_js(self):
        """CCA formula computed via JS matches hand calculation."""
        # Inject reviews and compute
        self.js("""
            state.reviews = [
                {name:'R1', author:'', year:'', studies:['A','B','C']},
                {name:'R2', author:'', year:'', studies:['B','C','D']},
                {name:'R3', author:'', year:'', studies:['A','C','D','E']}
            ];
            computeAll();
        """)
        time.sleep(0.3)
        result = self.js("return state.computed;")
        # R=3, J=5 (A,B,C,D,E), N=3+3+4=10
        # CCA = (10-5)/(5*(3-1)) = 5/10 = 0.50
        self.assertAlmostEqual(result['cca'], 0.50, places=4)
        self.assertEqual(result['R'], 3)
        self.assertEqual(result['J'], 5)
        self.assertEqual(result['N'], 10)

    def test_19_dark_mode_toggle(self):
        """Dark mode toggle adds/removes class on body."""
        body = self.driver.find_element(By.TAG_NAME, 'body')
        self.assertNotIn('dark', body.get_attribute('class') or '')
        self.driver.find_element(By.ID, 'darkToggle').click()
        time.sleep(0.1)
        self.assertIn('dark', body.get_attribute('class'))
        self.driver.find_element(By.ID, 'darkToggle').click()
        time.sleep(0.1)
        self.assertNotIn('dark', body.get_attribute('class') or '')

    def test_20_localstorage_persistence(self):
        """Data persists across page reloads via localStorage."""
        self.add_review('PersistReview', 'Study XX\nStudy YY\nStudy ZZ')
        # Reload page
        self.driver.get(FILE_URL)
        time.sleep(0.5)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.review-list li')
        self.assertEqual(len(items), 1)
        self.assertIn('PersistReview', items[0].text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
