# WhatsApp QR poster and auto-reply

Branded A4 poster with a QR code. Scanning it opens WhatsApp with a chat to
**+27 82 670 9562** (The HR Insights Co. business number) and a message
already typed in. The visitor taps send, and WhatsApp Business replies
automatically with the team's contact details and the website link.

## Files

| File | What it is |
| --- | --- |
| `output/whatsapp-qr-poster-a4.pdf` | Print-ready A4 poster. Print at 100% / "Actual size". |
| `output/whatsapp-qr-poster-a4.png` | Same poster as a 300 dpi image (for email, social, screens). |
| `output/whatsapp-qr-flyer-a5.pdf` | Half-size (A5) flyer, for a print shop or A5 paper. |
| `output/whatsapp-qr-flyers-2up-a4.pdf` | Two A5 flyers on one landscape A4 sheet. Print on A4 and cut along the dashed line. |
| `output/whatsapp-qr.svg` / `.png` | The QR code on its own, for other material. |
| `output/auto-reply.txt` | The auto-reply text to paste into WhatsApp Business. |
| `config.json` | Number, pre-filled message, staff contacts, website, poster wording. |

## 1. Print the poster and flyers

Print every PDF at 100% / "Actual size", never "Fit to page".

- **Poster:** `output/whatsapp-qr-poster-a4.pdf` on A4.
- **Flyers on an office printer:** `output/whatsapp-qr-flyers-2up-a4.pdf` on
  A4 (landscape), then cut along the dashed line to get two A5 flyers.
- **Flyers from a print shop:** send them `output/whatsapp-qr-flyer-a5.pdf`.

Before printing a batch, scan a test print with an iPhone and an Android
phone to confirm it opens the right chat.

## 2. What happens when someone scans it

The QR code holds this link:

```
https://wa.me/27826709562?text=Hi%20HR%20Insights%20Co.%2C%20I%20would%20like%20to%20know%20more%20about%20your%20services.
```

The phone opens WhatsApp in a chat with the business number, with
*"Hi HR Insights Co., I would like to know more about your services."*
typed in. WhatsApp never sends a message on its own; the visitor has to tap
send, which is why the poster tells them to.

## 3. Set up the auto-reply (WhatsApp Business app)

The auto-reply uses WhatsApp Business's **Greeting message**. It's set up on
the phone that runs the business number. This can't be done from code.

1. Open **WhatsApp Business** on the phone with +27 82 670 9562.
2. Go to **Settings** (Android: ⋮ menu > Settings) > **Business tools** > **Greeting message**.
3. Turn on **Send greeting message**.
4. Tap the message and replace it with the text in `output/auto-reply.txt`.
   The `*asterisks*` show the staff names in **bold** in WhatsApp.
5. Under **Recipients**, choose **Everyone**.
6. Tap **Save**.

**What to expect:** WhatsApp sends the greeting when someone messages the
business for the first time, or after 14 days with no messages between you.
It doesn't reply to every message, so someone chatting with you regularly
won't keep getting it.

**Optional:** you can also set up **Business tools > Away message** for
after-hours enquiries, and add the website to **Business tools > Business
profile** so it shows on your profile.

## 4. Change the details and rebuild

Edit `config.json` (for example staff phone numbers, emails, poster wording or
the pre-filled message), then run:

```bash
pip install segno playwright
python3 whatsapp/build.py
```

If Playwright hasn't downloaded its own browser, point it at an installed
Chromium or Chrome instead:

```bash
CHROMIUM_PATH=/path/to/chrome python3 whatsapp/build.py
```

After rebuilding, paste the new `output/auto-reply.txt` into WhatsApp
Business again. If you change the number or pre-filled message, reprint the
poster, because the QR code changes too.

Keep the pre-filled message short. Every extra character makes the QR code
denser and harder to scan from a distance.

The Inter font in `fonts/` is bundled under the SIL Open Font License so the
poster renders the same on any machine.
