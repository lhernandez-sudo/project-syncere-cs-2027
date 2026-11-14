"""Host Candy Court for browsers on the same local network."""

import argparse
import json
import random
import secrets
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import webbrowser
from threading import Lock

OPENING_GROUPS = (
    ("Reese's Cups", 'Kit Kat', 'Twizzlers', 'Red Vines'),
    ('Twix', 'Snickers', 'Ring Pop', 'Push Pop'),
    ('Starburst', 'Nerds Gummy Clusters', 'Smarties', 'SweeTarts'),
    ('Sour Patch Kids', 'Skittles', 'Runts', 'Gobstopper'),
    ("Peanut M&M's", 'Butterfinger', 'Pop Rocks', 'Fun Dip'),
    ('Swedish Fish', 'Haribo Goldbears', 'Pixy Stix', 'Bottle Caps'),
    ("Hershey's Milk Chocolate", 'Milky Way', 'Candy Corn', 'Candy Buttons'),
    ('Airheads', 'Laffy Taffy', 'Pez', 'Tootsie Pops'),
    ('Sour Punch Straws', 'Trolli Sour Brite Crawlers', 'Dum Dums', 'Blow Pop'),
    ('3 Musketeers', 'Baby Ruth', 'Tootsie Roll', 'Milk Duds'),
    ('Warheads', 'Toxic Waste', 'Junior Mints', 'York Peppermint Pattie'),
    ('Almond Joy', 'Mounds', 'Rolo', 'Caramello'),
    ('Mike and Ike', 'Hot Tamales', 'Heath', 'Skor'),
    ('Crunch', '100 Grand', 'Snow Caps', 'Whoppers'),
    ('Jolly Rancher', 'Life Savers Gummies', 'Ferrero Rocher', 'Lindt Lindor Truffles'),
    ('Take 5', 'Whatchamacallit', 'Kinder Bueno', "Hershey's Kisses"),
)
PROMPTS = (
    "Which candy should negotiate with aliens who only accept snacks?",
    "Which candy would a raccoon steal while making eye contact?",
    "Which candy needs its own wrestling entrance music?",
    "Which candy would you defend in court with zero evidence?",
    "Which candy could get elected mayor of a mall food court?",
    "Which candy would a ghost haunt a pantry for?",
    "Which candy deserves an emotional support backpack?",
    "Which candy gets the last seat on the escape pod?",
    "Which candy could talk a vending machine into giving refunds?",
    "Which candy should narrate a documentary about your lunch?",
    "Which candy starts a pyramid scheme in the snack aisle?",
    "Which candy could survive a spin cycle in your jeans?",
    "Which candy gets hired as the school mascot's stunt double?",
    "Which candy could beat a garden gnome in a staring contest?",
    "Which candy would a dragon demand as rent?",
    "Which candy do you sneak into the Moon cafeteria?",
    "Which winner would you rescue from a candy-eating Roomba?",
    "Which winner gets to DJ a wedding on Mars?",
    "Which winner should run a tiny airport for pigeons?",
    "Which winner could convince a goose to apologize?",
    "Which finalist gets the crown and a wildly unnecessary parade?",
)


class Tournament:
    def __init__(self):
        self.groups = list(OPENING_GROUPS)
        self.results = []
        self.votes = {}
        self.phase = "waiting"
        self.version = 0

    def snapshot(self, voter):
        index = min(len(self.results) - (self.phase == "result"), 20)
        choices = self.groups[index] if index < len(self.groups) else []
        return dict(index=index, version=self.version, choices=choices,
                    phase=self.phase, prompt=PROMPTS[index],
                    voted=self.votes.get(voter), total=len(self.votes),
                    results=self.results.copy())

    def advance(self):
        if self.phase == "open":
            if not self.votes:
                raise ValueError("At least one vote is needed to close this matchup.")
            choices = self.groups[len(self.results)]
            counts = [list(self.votes.values()).count(i) for i in range(4)]
            leaders = [i for i, count in enumerate(counts) if count == max(counts)]
            winner = choices[random.choice(leaders)]
            self.results.append(dict(winner=winner, counts=counts, choices=choices,
                                     tie=len(leaders) > 1))
            if len(self.results) in (16, 20):
                start = 0 if len(self.results) == 16 else 16
                winners = [r["winner"] for r in self.results[start:]]
                self.groups.extend(winners[i:i + 4] for i in range(0, len(winners), 4))
            self.phase = "finished" if len(self.results) == 21 else "result"
        elif self.phase in ("waiting", "result"):
            self.votes = {}
            self.phase = "open"
        else:
            raise ValueError("The tournament is complete.")
        self.version += 1

    def vote(self, voter, version, choice):
        if self.phase != "open" or version != self.version:
            raise ValueError("That vote has closed.")
        if type(choice) is not int or not 0 <= choice < 4:
            raise ValueError("Select one candy.")
        self.votes[voter] = choice


def local_address():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
            probe.connect(("192.0.2.1", 80))
            return probe.getsockname()[0]
    except OSError:
        return "127.0.0.1"


PAGE = r'''<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Candy Court</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: #241532; color: #fff4df; font: 16px system-ui, sans-serif; }
  main { max-width: 960px; margin: auto; padding: clamp(18px, 5vw, 64px); }
  header { border-bottom: 2px solid #b985ef; padding-bottom: 18px; }
  h1, h2 { font-family: Georgia, serif; line-height: 1.08; margin: .25em 0; }
  h1 { font-size: clamp(44px, 8vw, 94px); letter-spacing: -.04em; }
  h2 { font-size: clamp(26px, 5vw, 48px); }
  a { color: #ffe694; overflow-wrap: anywhere; }
  #progress { color: #e1bdff; font-weight: 700; margin-top: 27px; }
  #choices { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin: 24px 0; }
  .choice, button { border: 0; border-radius: 12px; padding: 14px; font: inherit; font-weight: 750; }
  .choice { display: flex; align-items: center; justify-content: space-between; gap: 8px; min-height: 66px; background: #4a315f; color: #fff4df; overflow-wrap: anywhere; text-align: left; }
  button { cursor: pointer; background: #ffe694; color: #241532; }
  button:disabled { cursor: default; opacity: .75; }
  .chosen { outline: 3px solid #ffe694; outline-offset: -3px; }
  .winner { background: #b5f4cd; color: #241532; }
  #status, #message { min-height: 1.5em; }
  #message { color: #ffb7ab; }
  details { margin-top: 28px; }
  summary { cursor: pointer; }
  li { padding: 4px; }
  @media (max-width: 480px) { #choices { grid-template-columns: 1fr; } }
</style>
<main>
  <header>
    <h1>The Candy Court</h1>
    <div id="join" hidden>Students join at <a id="joinLink"></a></div>
  </header>
  <p id="progress"></p>
  <h2 id="prompt">Connecting…</h2>
  <div id="choices"></div>
  <p id="status" role="status"></p>
  <button id="advance" hidden></button>
  <p id="message" role="alert"></p>
  <details id="history" hidden><summary>Bracket results</summary><ol id="results"></ol></details>
</main>
<script>
  const host = /*HOST*/null;
  const byId = id => document.getElementById(id);
  const advance = byId('advance');
  let state;
  let pending = false;
  if (host) {
    byId('join').hidden = false;
    byId('joinLink').href = host.join;
    byId('joinLink').textContent = host.join;
  }

  function render(next) {
    if (state && next.version < state.version) return;
    const change = !state || state.version !== next.version || state.voted !== next.voted;
    state = next;
    const result = state.phase === 'result' || state.phase === 'finished';
    const last = result ? state.results.at(-1) : null;
    if (change) {
      const round = state.index < 16 ? 'Round 1' : state.index < 20 ? 'Round 2' : 'Final';
      byId('progress').textContent = round + ' · Match ' + (state.index + 1) + ' of 21';
      byId('prompt').textContent = state.phase === 'waiting' ? 'The court is about to convene'
        : last ? last.winner + (state.phase === 'finished' ? ' takes the crown!' : ' advances!') : state.prompt;
      byId('choices').replaceChildren(...(state.phase === 'waiting' ? [] : state.choices).map((candy, index) => {
        const canVote = !host && state.phase === 'open';
        const tile = document.createElement(canVote ? 'button' : 'div');
        tile.className = 'choice';
        if (canVote) {
          tile.setAttribute('aria-pressed', String(state.voted === index));
          tile.onclick = () => submit('/vote', index);
          if (state.voted === index) tile.classList.add('chosen');
        }
        tile.textContent = candy;
        if (last) {
          if (candy === last.winner) tile.classList.add('winner');
          const count = document.createElement('span');
          count.textContent = last.counts[index] + ' votes';
          tile.append(count);
        }
        return tile;
      }));
      byId('history').hidden = !state.results.length;
      byId('results').replaceChildren(...state.results.map(match => {
        const item = document.createElement('li');
        item.textContent = match.choices.join(' / ') + ' → ' + match.winner;
        return item;
      }));
    }
    const status = state.phase === 'waiting' ? 'Waiting for the host to start the first vote.'
      : last ? (last.tie ? 'Tie broken by a random draw.' : '')
      : host ? state.total + ' votes in' : state.voted == null ? 'Pick one candy.' : 'Vote counted. You can change your pick until voting closes.';
    if (byId('status').textContent !== status) byId('status').textContent = status;
    advance.hidden = !host || state.phase === 'finished';
    advance.disabled = pending || (state.phase === 'open' && !state.total);
    advance.textContent = state.phase === 'open' ? 'Close vote and reveal winner'
      : state.phase === 'waiting' ? 'Open the first vote' : 'Open next vote';
  }

  async function submit(path, choice) {
    if (pending) return;
    pending = true;
    advance.disabled = true;
    try {
      const response = await fetch(path, {
        method: 'POST',
        headers: {'Content-Type': 'application/json', ...(host ? {'X-Host-Key': host.key} : {})},
        body: JSON.stringify({version: state.version, choice})
      });
      const data = await response.json();
      if (!response.ok) throw Error(data.error);
      byId('message').textContent = '';
      render(data);
    } catch (error) {
      byId('message').textContent = error.message;
    } finally {
      pending = false;
      advance.disabled = state.phase === 'open' && !state.total;
    }
  }

  async function refresh() {
    try {
      const response = await fetch('/state');
      if (!response.ok) throw Error('Disconnected');
      const next = await response.json();
      if (!pending) render(next);
      if (byId('message').textContent === 'Reconnecting…') byId('message').textContent = '';
    } catch {
      byId('message').textContent = 'Reconnecting…';
    } finally {
      setTimeout(refresh, 750);
    }
  }
  advance.onclick = () => submit('/advance');
  refresh();
</script>
</html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--join-host", default=None,
                        help="Override the address shown on the host screen.")
    parser.add_argument("--no-browser", action="store_true",
                        help="Print the host link without opening a browser.")
    args = parser.parse_args()
    join = f"http://{args.join_host or local_address()}:{args.port}/"
    game = Tournament()
    lock = Lock()
    host_key = secrets.token_urlsafe(24)
    page = PAGE.encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def send(self, content, kind, status=200, cookie=None):
            self.send_response(status)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            if cookie:
                self.send_header("Set-Cookie", f"candy_voter={cookie}; Path=/; HttpOnly; SameSite=Strict")
            self.end_headers()
            self.wfile.write(content)

        def respond(self, data, status=200, cookie=None):
            self.send(json.dumps(data).encode(), "application/json", status, cookie)

        def voter(self):
            for value in self.headers.get("Cookie", "").split(";"):
                name, _, token = value.strip().partition("=")
                if name == "candy_voter" and len(token) == 32:
                    return token
            return None

        def do_GET(self):
            if self.path in ("/", "/host"):
                if self.path == "/host" and self.client_address[0] != "127.0.0.1":
                    self.respond({"error": "Open the host page on the server computer."}, 403)
                    return
                data = {"key": host_key, "join": join} if self.path == "/host" else None
                content = page.replace(b"/*HOST*/null", json.dumps(data).replace("<", "\\u003c").encode())
                self.send(content, "text/html; charset=utf-8")
            elif self.path == "/state":
                voter = self.voter()
                with lock:
                    state = game.snapshot(voter)
                self.respond(state, cookie=None if voter else secrets.token_hex(16))
            else:
                self.respond({"error": "Page not found."}, 404)

        def do_POST(self):
            if self.path == "/advance" and (
                self.client_address[0] != "127.0.0.1"
                or self.headers.get("X-Host-Key") != host_key
            ):
                self.respond({"error": "Host access required."}, 403)
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 1024:
                    raise ValueError("Invalid request.")
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError("Invalid request.")
                with lock:
                    if self.path == "/advance":
                        if data.get("version") != game.version:
                            raise ValueError("The matchup has already changed.")
                        game.advance()
                    elif self.path == "/vote" and self.voter():
                        game.vote(self.voter(), data.get("version"), data.get("choice"))
                    else:
                        raise ValueError("Open the voting page to join.")
                    state = game.snapshot(self.voter())
                self.respond(state)
            except (ValueError, UnicodeDecodeError) as error:
                self.respond({"error": str(error)}, 400)

        def log_message(self, *_):
            pass

    with ThreadingHTTPServer(("0.0.0.0", args.port), Handler) as server:
        host_url = f"http://127.0.0.1:{args.port}/host"
        print(f"Host: {host_url}", flush=True)
        print(f"Students: {join}", flush=True)
        if not args.no_browser:
            webbrowser.open(host_url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
