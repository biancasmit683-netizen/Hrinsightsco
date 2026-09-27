"""Build the branded WhatsApp QR poster and auto-reply text.

Reads whatsapp/config.json and writes to whatsapp/output/:
  - whatsapp-qr-poster-a4.pdf   print-ready A4 poster
  - whatsapp-qr-poster-a4.png   same poster as an image (300 dpi)
  - whatsapp-qr.svg / .png      the QR code on its own
  - auto-reply.txt              greeting message to paste into WhatsApp Business

Requires: pip install segno playwright
"""

import html
import json
import os
import sys
import urllib.parse
from pathlib import Path

import segno

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"

NAVY = "#1F2A44"


def load_config():
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    number = "".join(ch for ch in cfg["whatsapp_number"] if ch.isdigit())
    if number.startswith("0"):
        sys.exit("whatsapp_number must be in international format (e.g. 27821234567), not start with 0.")
    cfg["whatsapp_number"] = number
    return cfg


def whatsapp_link(cfg):
    text = urllib.parse.quote(cfg["prefilled_message"])
    return f"https://wa.me/{cfg['whatsapp_number']}?text={text}"


def build_qr(link):
    # High error correction leaves room for the small brand badge in the centre.
    qr = segno.make(link, error="h", micro=False)
    qr.save(OUT / "whatsapp-qr.svg", scale=10, border=0, dark=NAVY, light=None, xmldecl=False, svgns=True, omitsize=True)
    qr.save(OUT / "whatsapp-qr.png", scale=20, border=4, dark=NAVY, light="#ffffff")
    return (OUT / "whatsapp-qr.svg").read_text(encoding="utf-8")


def build_auto_reply(cfg):
    lines = [
        "Hi there, thank you for contacting The HR Insights Co.",
        "",
        "We help organisations turn scattered HR data into clear, decision-ready insight.",
        "",
        "You can reach our team directly:",
        "",
    ]
    for person in cfg["staff"]:
        lines.append(f"*{person['name']}* - {person['role']}")
        if person.get("phone"):
            lines.append(f"Tel: {person['phone']}")
        if person.get("email"):
            lines.append(f"Email: {person['email']}")
        lines.append("")
    lines += [
        f"General enquiries: {cfg['general_email']}",
        f"Website: {cfg['website_url']}",
        "",
        "We'll get back to you as soon as possible.",
        "The HR Insights Co. - From noise to clarity",
    ]
    text = "\n".join(lines)
    (OUT / "auto-reply.txt").write_text(text + "\n", encoding="utf-8")
    return text


def build_poster_html(cfg, qr_svg):
    p = cfg["poster"]
    esc = html.escape
    headline = "<br>".join(esc(part) for part in p["headline"].split("\n"))
    template = (HERE / "poster_template.html").read_text(encoding="utf-8")
    replacements = {
        "{{EYEBROW}}": esc(p["eyebrow"]),
        "{{HEADLINE}}": headline,
        "{{SUBTEXT}}": esc(p["subtext"]),
        "{{CTA}}": esc(p["cta"]),
        "{{QR_SVG}}": qr_svg,
        "{{WEBSITE}}": esc(cfg["website_label"]),
        "{{EMAIL}}": esc(cfg["general_email"]),
        "{{FONT_URL}}": "../fonts/Inter-latin.woff2",
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    path = OUT / "whatsapp-qr-poster-a4.html"
    path.write_text(template, encoding="utf-8")
    return path


def render_poster(html_path):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        # Set CHROMIUM_PATH to use an existing Chromium instead of Playwright's download.
        exe = os.environ.get("CHROMIUM_PATH")
        browser = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        page = browser.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=3.125)
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.pdf(path=str(OUT / "whatsapp-qr-poster-a4.pdf"), format="A4", print_background=True,
                 margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        page.screenshot(path=str(OUT / "whatsapp-qr-poster-a4.png"), full_page=False)
        browser.close()


def main():
    OUT.mkdir(exist_ok=True)
    cfg = load_config()
    link = whatsapp_link(cfg)
    qr_svg = build_qr(link)
    build_auto_reply(cfg)
    html_path = build_poster_html(cfg, qr_svg)
    render_poster(html_path)
    print("WhatsApp link:", link)
    print("Written to:", OUT)


if __name__ == "__main__":
    main()
