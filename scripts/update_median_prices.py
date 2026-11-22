"""Update the median sale price chart and table in index.html."""

import csv
from collections import defaultdict
from html import escape
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]


def replace_rows(page, section, rows):
    start = f"<!-- Begin {section} rows -->\n"
    end = f"\n<!-- End {section} rows -->"
    before, content = page.split(start, 1)
    _, after = content.split(end, 1)
    return before + start + "\n".join(rows) + end + after


def main():
    prices = defaultdict(list)
    with (ROOT / "data/college_town_home_sales.csv").open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            price = int(row["sale_price"])
            if price >= 1000:
                prices[row["city"], row["state"]].append(price)

    # Integer sale prices yield medians in whole or half dollars. Round halves up.
    medians = sorted(
        (int(median(sales) + 0.5), city, state)
        for (city, state), sales in prices.items()
    )
    highest = medians[-1][0]
    chart_rows = []
    table_rows = []
    for price, city, state in medians:
        label = escape(f"{city}, {state}")
        dollars = f"${price:,}"
        width = price / highest
        chart_rows.append(
            f'<div class="row"><span>{label}</span><span class="track">'
            f'<i style="width:{width:.1%}"></i></span><strong>{dollars}</strong></div>'
        )
        table_rows.append(f"<tr><td>{label}</td><td>{dollars}</td></tr>")

    homepage = ROOT / "index.html"
    page = homepage.read_text(encoding="utf-8")
    page = replace_rows(page, "chart", chart_rows)
    page = replace_rows(page, "table", table_rows)
    homepage.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
