from playwright.sync_api import sync_playwright

SEEDS = range(82, 92)

def main():
    total_sum = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for seed in SEEDS:
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            print(f"Processing {url}")

            page.goto(url)
            page.wait_for_selector("table")
            page.wait_for_timeout(1500)

            table_sum = page.evaluate("""
                () => {
                    let total = 0;
                    document.querySelectorAll("td, th").forEach(c => {
                        const t = c.innerText.trim();
                        if (/^-?[0-9]+(\\.[0-9]+)?$/.test(t)) {
                            total += parseFloat(t);
                        }
                    });
                    return total;
                }
            """)

            print("Seed", seed, "=", table_sum)
            total_sum += table_sum

        browser.close()

    print("FINAL TOTAL =", total_sum)

if __name__ == "__main__":
    main()
