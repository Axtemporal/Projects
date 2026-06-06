# Barcode Generator & PDF Receipt

Generates EAN-13 barcodes and produces a formatted PDF receipt for retail products.

---

## What It Does

Takes a product name as input, looks up the corresponding EAN-13 barcode number, generates a barcode image, and embeds it into a formatted PDF receipt using FPDF2.

---

## How It Works

1. **Product selection** — the user types a product name; the script maps it to its EAN-13 barcode number
2. **Barcode generation** — creates a standard EAN-13 barcode image (`new_code1.png`) using `python-barcode` with PIL rendering
3. **PDF creation** — builds a formatted A4 PDF with:
   - Store header and item description
   - Embedded barcode image centered on the page
4. **Output** — saves the receipt as `testando.pdf`

---

## Product Catalog

| Product | EAN-13 |
|---------|--------|
| Biscoito Maltado da Vaquinha | 7896024760319 |
| Biscoito Maizena Piraquê | 7896024722324 |
| Biscoito de Polvilho Qualitá | 7895000318261 |
| Batata Palha Yoki | 7891095031122 |
| Sticksy Elma Chips | 7892840818029 |
| Torrada Wickbold | 7896066304359 |
| Vela Jardim Siciliano Phebo | 7896512953094 |
| Livro Microeconomia — Hal Varian | 9788535230185 |

---

## Technologies

| Package | Use |
|---------|-----|
| `python-barcode` | EAN-13 barcode image generation |
| `Pillow` | Image rendering for barcode |
| `fpdf2` | PDF creation and layout |

---

## How to Run

```bash
pip install fpdf2 python-barcode pillow
python "FPDF - Bar code reader 22.1.py"
```
