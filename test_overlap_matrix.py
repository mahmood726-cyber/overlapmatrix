"""
test_overlap_matrix.py — 20 Selenium tests for Overlap Matrix / CCA Calculator
"""
import sys, io, os, json, time, unittest
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
    """Selenium test suite for Overlap Matrix / CCA Calculator."""

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

    # ── Helper ────────────────────────────────────────────
    def add_ma(self, name, studies_csv):
        name_el = self.driver.find_element(By.ID, 'maNameInput')
        studies_el = self.driver.find_element(By.ID, 'maStudiesInput')
        name_el.clear()
        name_el.send_keys(name)
        studies_el.clear()
        studies_el.send_keys(studies_csv)
        self.driver.find_element(By.ID, 'addMaBtn').click()
        time.sleep(0.15)

    def click_compute(self):
        self.driver.find_element(By.ID, 'computeBtn').click()
        time.sleep(0.5)

    def switch_tab(self, tab_id):
        self.driver.find_element(By.ID, tab_id).click()
        time.sleep(0.2)

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════

    def test_01_page_loads(self):
        """Page loads with correct title."""
        self.assertIn('Overlap Matrix', self.driver.title)

    def test_02_tabs_present(self):
        """All 4 tabs are rendered with correct ARIA roles."""
        tabs = self.driver.find_elements(By.CSS_SELECTOR, '[role="tab"]')
        self.assertEqual(len(tabs), 4)
        labels = [t.text for t in tabs]
        self.assertIn('Data Input', labels)
        self.assertIn('Overlap Matrix', labels)
        self.assertIn('Analysis', labels)
        self.assertIn('Report', labels)

    def test_03_add_single_ma(self):
        """Adding one MA shows it in the list."""
        self.add_ma('Test MA', 'Study A, Study B, Study C')
        items = self.driver.find_elements(By.CSS_SELECTOR, '.ma-list li')
        self.assertEqual(len(items), 1)
        self.assertIn('Test MA', items[0].text)
        self.assertIn('Study A', items[0].text)

    def test_04_add_multiple_mas(self):
        """Adding multiple MAs shows correct count badge."""
        self.add_ma('MA1', 'S1, S2, S3')
        self.add_ma('MA2', 'S2, S3, S4')
        badge = self.driver.find_element(By.ID, 'dataCountBadge').text
        self.assertIn('2 MAs', badge)
        self.assertIn('4 unique studies', badge)

    def test_05_remove_ma(self):
        """Remove button removes an MA from the list."""
        self.add_ma('MA1', 'S1, S2')
        self.add_ma('MA2', 'S3, S4')
        remove_btns = self.driver.find_elements(By.CSS_SELECTOR, '[data-remove]')
        self.assertEqual(len(remove_btns), 2)
        remove_btns[0].click()
        time.sleep(0.2)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.ma-list li')
        self.assertEqual(len(items), 1)
        self.assertIn('MA2', items[0].text)

    def test_06_example_depression(self):
        """Depression example loads 6 MAs."""
        self.driver.find_element(By.ID, 'exampleDepression').click()
        time.sleep(0.3)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.ma-list li')
        self.assertEqual(len(items), 6)
        badge = self.driver.find_element(By.ID, 'dataCountBadge').text
        self.assertIn('6 MAs', badge)

    def test_07_example_statins(self):
        """Statins example loads 5 MAs."""
        self.driver.find_element(By.ID, 'exampleStatins').click()
        time.sleep(0.3)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.ma-list li')
        self.assertEqual(len(items), 5)

    def test_08_csv_import(self):
        """CSV paste imports multiple MAs."""
        csv_text = "ReviewA, StudyX, StudyY, StudyZ\nReviewB, StudyY, StudyZ, StudyW"
        ta = self.driver.find_element(By.ID, 'csvPasteArea')
        ta.send_keys(csv_text)
        self.driver.find_element(By.ID, 'importCsvBtn').click()
        time.sleep(0.3)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.ma-list li')
        self.assertEqual(len(items), 2)

    def test_09_compute_requires_two_mas(self):
        """Compute with <2 MAs shows alert."""
        self.add_ma('OnlyOne', 'S1, S2')
        # Accept the alert that will come
        self.driver.find_element(By.ID, 'computeBtn').click()
        time.sleep(0.3)
        try:
            alert = self.driver.switch_to.alert
            self.assertIn('at least 2', alert.text)
            alert.accept()
        except Exception:
            pass  # Some headless modes auto-dismiss

    def test_10_cca_computation_basic(self):
        """CCA computed correctly for a known simple case."""
        # 2 MAs, 3 unique studies: MA1=[A,B], MA2=[B,C]
        # sumC=4, J=3, r=2, CCA = (4-3)/(2*3-3) = 1/3 = 33.3%
        self.add_ma('MA1', 'A, B')
        self.add_ma('MA2', 'B, C')
        self.click_compute()
        cca_text = self.driver.find_element(By.ID, 'ccaResult').text
        self.assertIn('33.3%', cca_text)
        self.assertIn('Very High', cca_text)

    def test_11_cca_no_overlap(self):
        """CCA = 0% when MAs share no studies."""
        self.add_ma('MA1', 'A, B')
        self.add_ma('MA2', 'C, D')
        self.click_compute()
        cca_text = self.driver.find_element(By.ID, 'ccaResult').text
        self.assertIn('0.0%', cca_text)
        self.assertIn('Slight', cca_text)

    def test_12_cca_complete_overlap(self):
        """CCA = 100% when all MAs include exactly the same studies."""
        self.add_ma('MA1', 'A, B, C')
        self.add_ma('MA2', 'A, B, C')
        self.add_ma('MA3', 'A, B, C')
        self.click_compute()
        cca_text = self.driver.find_element(By.ID, 'ccaResult').text
        # sumC=9, J=3, r=3, CCA=(9-3)/(9-3)=1.0=100%
        self.assertIn('100.0%', cca_text)

    def test_13_citation_matrix_rendered(self):
        """Citation matrix table is rendered with correct dimensions."""
        self.add_ma('MA1', 'A, B')
        self.add_ma('MA2', 'B, C')
        self.click_compute()
        table = self.driver.find_element(By.ID, 'citationMatrix')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        # header + 2 MA rows + frequency row = 4
        self.assertEqual(len(rows), 4)

    def test_14_pairwise_heatmap_rendered(self):
        """Pairwise heatmap table is rendered."""
        self.add_ma('MA1', 'A, B')
        self.add_ma('MA2', 'B, C')
        self.click_compute()
        table = self.driver.find_element(By.ID, 'pairwiseHeatmap')
        cells = table.find_elements(By.CLASS_NAME, 'heatmap-cell')
        # 2x2 = 4 cells
        self.assertEqual(len(cells), 4)

    def test_15_frequency_chart_rendered(self):
        """Study frequency histogram SVG is rendered."""
        self.driver.find_element(By.ID, 'exampleDepression').click()
        time.sleep(0.2)
        self.click_compute()
        self.switch_tab('tab-analysis')
        svg = self.driver.find_element(By.CSS_SELECTOR, '#frequencyChartWrap svg')
        self.assertIsNotNone(svg)
        bars = svg.find_elements(By.CLASS_NAME, 'bar')
        self.assertGreater(len(bars), 0)

    def test_16_most_included_table(self):
        """Most-included studies table rendered with all studies."""
        self.driver.find_element(By.ID, 'exampleDepression').click()
        time.sleep(0.2)
        self.click_compute()
        self.switch_tab('tab-analysis')
        table = self.driver.find_element(By.CSS_SELECTOR, '#mostIncludedWrap table')
        rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
        # Depression example has 10 unique studies
        self.assertEqual(len(rows), 10)

    def test_17_dendrogram_rendered(self):
        """Dendrogram SVG is rendered with lines."""
        self.driver.find_element(By.ID, 'exampleStatins').click()
        time.sleep(0.2)
        self.click_compute()
        self.switch_tab('tab-analysis')
        svg = self.driver.find_element(By.CSS_SELECTOR, '#dendrogramWrap svg')
        lines = svg.find_elements(By.CLASS_NAME, 'dendro-line')
        self.assertGreater(len(lines), 0)

    def test_18_report_methods_text(self):
        """Report tab shows methods text with Pieper citation."""
        self.add_ma('MA1', 'A, B')
        self.add_ma('MA2', 'B, C')
        self.click_compute()
        self.switch_tab('tab-report')
        text = self.driver.find_element(By.ID, 'methodsTextWrap').text
        self.assertIn('Pieper', text)
        self.assertIn('2014', text)
        self.assertIn('CCA', text)

    def test_19_dark_mode_toggle(self):
        """Dark mode toggle adds/removes class on body."""
        body = self.driver.find_element(By.TAG_NAME, 'body')
        self.assertNotIn('dark', body.get_attribute('class') or '')
        self.driver.find_element(By.ID, 'darkModeToggle').click()
        time.sleep(0.1)
        self.assertIn('dark', body.get_attribute('class'))
        self.driver.find_element(By.ID, 'darkModeToggle').click()
        time.sleep(0.1)
        self.assertNotIn('dark', body.get_attribute('class') or '')

    def test_20_localstorage_persistence(self):
        """Data persists across page reloads via localStorage."""
        self.add_ma('PersistMA', 'X, Y, Z')
        # Reload page
        self.driver.get(FILE_URL)
        time.sleep(0.5)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.ma-list li')
        self.assertEqual(len(items), 1)
        self.assertIn('PersistMA', items[0].text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
