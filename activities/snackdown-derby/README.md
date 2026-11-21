# Snackdown Derby

A five-minute classroom icebreaker for four teams: **Cheesy, Juicy,
Crispy, and Spicy**. Students get a team ticket on arrival, then cheer for their
snack during an automatic stadium race with three ridiculous cartoon battles.

## Run

From this folder:

```powershell
python snackdown_derby.py
```

From the repository root:

```powershell
python activities/snackdown-derby/snackdown_derby.py
```

Use `py -3` instead of `python` if needed on Windows. The launcher uses only
Python's standard library and opens a self-contained HTML file in your browser.
No server, installation, internet, or student devices are needed.

## Before students arrive

1. Click **Print 18 tickets**. The sheet fits 18 black-and-white tickets on one
   US Letter page. Cut along the dashed borders and shuffle the paper tickets.
2. Hand one ticket to each student. Team sizes are 5, 5, 4, and 4.
3. Project the game. Press **F** for fullscreen.
4. Click **LET THE NONSENSE BEGIN** when everyone is ready. That click also
   enables the original synthesized music.

The 5:00 show includes an introduction, four laps, three snack battles, seven sabotage moments, and
a winner celebration. The live track pauses for each battle. Playful knockouts
launch cartoon snacks through the air. Battle results and the race champion
are random; winning a fight does not guarantee winning the race. Sabotage
actually slows the target and boosts the attacker, while the final winner still
has equal odds. Each character has a ridiculous weapon: a cheddar ray gun, pulp
laser sword, cryo-fryer, or thunder plunger. Banana peels, freeze rays, portals,
and falling anvils interrupt the race. The original 128 BPM pop soundtrack has
a repeating melody, four-chord progression, bass, claps, drums, and delay. Every team
has an equal 25% chance of winning the race, independent of ticket counts.

## Host controls

- **Space / Pause:** pause or resume the entire show, including music timing.
- **M / Music:** toggle the original music and goofy effects.
- **F / Fullscreen:** enter or exit fullscreen.
- **New race:** after the show, return to the lobby and draw a new random result.
- **Shuffle ticket teams:** changes ticket numbering before you print. Keep the
  printed sheet once distributed; race resets preserve the ticket team allocation.

The default is five minutes. You can choose any duration from 3 to 5 minutes:

```powershell
python snackdown_derby.py --duration 180
python snackdown_derby.py --duration 300
```

The launcher also supports `--output show.html --no-browser` to export the
standalone show. Refreshing or opening that HTML draws a fresh winner.
Keep this activity separate from the PiCar-X simulation.
