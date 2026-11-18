# Hotmail-Checker-Bot
**Version 2.0 — Fixed Edition**

A Python script to check Hotmail/Outlook accounts from a combo list (`email:password`), validate credentials, and search for specified keywords in the inbox. Runs checks concurrently using a thread pool and serves a local HTTP dashboard for real-time monitoring.

---

## 📜 Features

- ✅ **Account Validation** — Checks email/password combinations against Microsoft Live OAuth
- ✅ **2FA Detection** — Identifies accounts protected by two-factor authentication
- ✅ **Inbox Keyword Search** — Searches for specified keywords in email inbox (via Outlook API)
- ✅ **Concurrent Checking** — configurable thread count (default 10) using `ThreadPoolExecutor`
- ✅ **Local HTTP Dashboard** — real-time stats page at `http://localhost:8080/`
- ✅ **Result Files** — auto-generates `valid.txt`, `2fa.txt`, `Inbox_Hits.txt`
- ✅ **Credit/Signature Line** — customizable footer appended to all output files

---

## 🛠️ Installation

1. **Clone the repo** (or download the script):
   ```bash
   git clone https://github.com/AbubakarGSF/Hotmail-Checker-Bot.git
   cd Hotmail-Checker-Bot
   ```

2. **Install dependencies**:
   ```bash
   pip install requests colorama urllib3
   ```

3. **Run the script**:
   ```bash
   python Hotmail_inboxer.py
   ```

---

## ⚙️ Usage

### First-time run
1. The script will prompt you to **enable the inboxer** (search emails for keywords)
2. Enter **keywords** comma-separated (e.g., `netflix,spotify,paypal,steam`)
3. Enter the **combo file path** (format: `email:password` per line)
4. Enter **thread count** (default: 10)

### Output files created:
- `valid.txt` — Valid accounts with credit signature
- `2fa.txt` — Accounts requiring two-factor authentication
- `Inbox_Hits.txt` — Accounts with matching keywords in inbox
- `valid.txt`, `2fa.txt`, `Inbox_Hits.txt` all include the credit line: `| @evilmarkhors | https://t.me/+IGM63Xe1A-43ZTdk`

---

## 🔧 Configuration

Edit `Hotmail_inboxer.py` to customize:

| Variable | Description |
|----------|-------------|
| `OUTLOOK_CLIENT_ID` | Microsoft OAuth client ID (`9199bf20-a13f-4107-85dc-02114787ef48`) |
| `OUTLOOK_REDIRECT` | OAuth redirect URI |
| `OUTLOOK_SCOPE` | OAuth scope permissions |
| `keywords` | Keywords to search in inbox (set via runtime prompt or edit line 34) |
| `CREDIT_LINE` | Signature line appended to all output files (line 19) |
| `port` | Dashboard port (defaults to 8080, scans 8080–8099) |

---

## 📊 Dashboard

Visiting `http://localhost:8080/` in your browser shows:
- Progress bar with percentage checked
- Counts: Valid / 2FA / Bad / Inbox Hits
- Checked / Total ratio
- Elapsed time
- Active keywords display
- Download links for result files

---

## ⚠️ Disclaimer

- This tool is for **educational and testing purposes only**
- Uses `verify=False` — does not validate SSL certificates
- Microsoft OAuth flow may be subject to rate limits / changes
- Keep credentials secure; do not use real passwords for testing

---

## 👤 Credits

- **Original Author:** @Fatbusinessman | https://t.me/ChkLeak
- **Updated By:** @evilmarkhors | https://t.me/+IGM63Xe1A-43ZTdk

---

## 📜 Version History

| Version | Date | Changes |
|---------|------|---------|
| **2.0** | 2026-11-18 | Fixed inboxer: Added Outlook API v2.0 search, PKCE flow, keyword detection, HTML dashboard |
| **1.0** | — | Initial release (basic credential checker) |

---
# Hotmail-Checker-Bot
