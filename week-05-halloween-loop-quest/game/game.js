"use strict";

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

const ui = {
  lives: document.getElementById("lives"), coins: document.getElementById("coins"),
  keys: document.getElementById("keys"), deaths: document.getElementById("deaths"),
  world: document.getElementById("worldLabel"), start: document.getElementById("startScreen"),
  question: document.getElementById("questionPanel"), questionWorld: document.getElementById("questionWorld"),
  questionTitle: document.getElementById("questionTitle"), questionCode: document.getElementById("questionCode"),
  questionPrompt: document.getElementById("questionPrompt"), answers: document.getElementById("answers"),
  feedback: document.getElementById("feedback"), timerText: document.getElementById("timerText"),
  timerBar: document.getElementById("timerBar"), win: document.getElementById("winPanel"),
  finalScore: document.getElementById("finalScore"), restart: document.getElementById("restartButton"),
  sound: document.getElementById("soundButton"),
};

const W = canvas.width, H = canvas.height, GROUND_Y = 452;
const COURSE_END = 12600, QUESTION_SECONDS = 15;
const palette = {
  skyTop: "#120b35", skyBottom: "#423079", mist: "#786ba0", moon: "#fff1a8",
  white: "#fffdf2", black: "#110b18", red: "#e93642", redDark: "#8e1925",
  blue: "#2367c9", blueLight: "#55b8ff", skin: "#f4b276", brown: "#8e4828",
  dirt: "#6d321d", grass: "#57bd4d", grassLight: "#91e067", brick: "#c64d2b",
  brickDark: "#702018", orange: "#ff981f", gold: "#ffd43b", green: "#32a94d",
  greenDark: "#14652d", purple: "#7041a4", stone: "#777083", lava: "#ff4b1f",
};

let started = false, paused = false, asking = false, won = false, audioOn = true;
let cameraX = 0, lastTime = 0, activeQuestion = null, deadline = 0, deathTimer = 0;
const held = new Set();
const state = { lives: 3, coins: 0, cleared: 0, deaths: 0, checkpoint: 60 };
const player = { x: 60, y: 365, w: 36, h: 48, vx: 0, vy: 0, onGround: false, dead: false, frame: 0 };
const particles = [];

const subjects = [
  { name: "VARIABLES + LISTS", world: "1-1", color: "#59d65e" },
  { name: "IF CONDITIONS + LOGIC", world: "2-1", color: "#a96cff" },
  { name: "FOR LOOPS", world: "3-1", color: "#ffd43b" },
  { name: "WHILE LOOPS", world: "4-1", color: "#ff6a3d" },
  { name: "FUNCTIONS", world: "5-1", color: "#55c8ff" },
];

const rawQuestions = [
  [
    ['coins = 7\ncoins = coins + 3\nprint(coins)', "What prints?", ["7", "10", "73"], 1, "coins changes from 7 to 10."],
    ['items = ["key", "star"]\nitems.append("mushroom")', "How many items are in the list?", ["2", "3", "4"], 1, "append adds one item, making 3."],
    ['name = "Mario"\nlives = 3', "Which variable stores text?", ["name", "lives", "Both"], 0, "name stores the string Mario."],
    ['pipes = [1, 2, 3, 4]\nprint(pipes[0])', "What prints?", ["0", "1", "4"], 1, "List indexes start at 0, so pipes[0] is 1."],
  ],
  [
    ['coins = 12\nif coins >= 10:\n    print("1-UP")', "Does 1-UP print?", ["Yes", "No", "Only in a loop"], 0, "12 is greater than or equal to 10."],
    ['has_key = True\nboo_awake = False\nif has_key and not boo_awake:\n    print("GO")', "Does GO print?", ["Yes", "No", "Error"], 0, "True and not False evaluates to True."],
    ['power = 2\nif power == 3:\n    print("Fire")\nelse:\n    print("Small")', "What prints?", ["Fire", "Small", "Nothing"], 1, "2 is not equal to 3, so else runs."],
    ['pipe = "red"\nif pipe == "green" or pipe == "red":\n    print("ENTER")', "Does ENTER print?", ["Yes", "No", "Only if green"], 0, "One side of an or expression is True."],
  ],
  [
    ['total = 0\nfor coin in [2, 4, 6]:\n    total = total + coin', "What is total?", ["6", "10", "12"], 2, "The accumulator changes 0 → 2 → 6 → 12."],
    ['for enemy in ["Boo", "Goomba"]:\n    print(enemy)', "How many times does print run?", ["1", "2", "3"], 1, "The loop runs once for each of 2 items."],
    ['count = 0\nfor number in range(4):\n    count += 1', "What is count?", ["3", "4", "5"], 1, "range(4) produces 0, 1, 2, 3: four iterations."],
    ['stars = []\nfor n in [1, 2, 3]:\n    stars.append(n * 2)', "What is stars?", ["[1, 2, 3]", "[2, 4, 6]", "6"], 1, "Each value is doubled before append."],
  ],
  [
    ['lives = 3\nwhile lives > 0:\n    lives -= 1', "When does the loop stop?", ["lives is 3", "lives is 1", "lives is 0"], 2, "The condition becomes False at 0."],
    ['pipe = "wrong"\nwhile pipe != "exit":\n    pipe = choose_pipe()', "What must eventually change?", ["pipe", "while", "Python"], 0, "pipe must become exit so the condition becomes False."],
    ['x = 1\nwhile x < 5:\n    x += 2', "What final value breaks the loop?", ["3", "5", "7"], 1, "x changes 1 → 3 → 5, then 5 < 5 is False."],
    ['running = True\nwhile running:\n    running = False', "How many iterations?", ["0", "1", "Forever"], 1, "It runs once, then running becomes False."],
  ],
  [
    ['def power(base, bonus):\n    return base + bonus\n\nresult = power(7, 5)', "What is returned?", ["5", "7", "12"], 2, "7 and 5 become parameters; return sends back 12."],
    ['def greet(name):\n    return "Hi " + name\n\nprint(greet("Luigi"))', "What prints?", ["Hi", "Luigi", "Hi Luigi"], 2, "The argument Luigi is joined to Hi."],
    ['def double(number):\n    return number * 2', "What is the parameter?", ["double", "number", "return"], 1, "number receives the argument when the function runs."],
    ['def jump():\n    print("Boing")\n\nvalue = jump()', "What is value without a return statement?", ["Boing", "0", "None"], 2, "print displays Boing, but the function returns None."],
  ],
];

const questions = [];
rawQuestions.forEach((group, subjectIndex) => group.forEach((q, questionIndex) => {
  questions.push({
    x: 900 + questions.length * 570, subjectIndex, questionIndex,
    code: q[0], prompt: q[1], answers: q[2], correct: q[3], explanation: q[4], passed: false,
  });
}));

const ground = [];
for (let x = 0; x < COURSE_END; x += 720) {
  // Each segment leaves an 80-pixel pit. Mario's TAS jump can clear that
  // distance; skipping a whole segment would create an impossible 800-pixel pit.
  ground.push({ x, y: GROUND_Y, w: 640, h: 88 });
}

const platforms = [];
for (let i = 0; i < 32; i++) {
  const x = 260 + i * 370;
  const kind = i % 7 === 5 ? "pipe" : i % 3 === 1 ? "question" : "brick";
  platforms.push({ x, y: kind === "pipe" ? 338 : 335 - (i % 3) * 45, w: kind === "pipe" ? 82 : 150, h: kind === "pipe" ? 114 : 30, kind });
}

const coins = Array.from({ length: 70 }, (_, i) => ({
  x: 270 + i * 165, y: 285 + (i % 4) * 28, r: 10, taken: false, phase: i * .7,
}));
const enemies = Array.from({ length: 24 }, (_, i) => ({
  x: 560 + i * 490, y: 418, w: 34, h: 34, alive: true, phase: i,
}));

function beep(frequency = 440, duration = .08, type = "square") {
  if (!audioOn) return;
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if (!AudioContext) return;
  const ac = beep.ac || (beep.ac = new AudioContext());
  const osc = ac.createOscillator(), gain = ac.createGain();
  osc.type = type; osc.frequency.value = frequency;
  gain.gain.setValueAtTime(.045, ac.currentTime);
  gain.gain.exponentialRampToValueAtTime(.001, ac.currentTime + duration);
  osc.connect(gain).connect(ac.destination); osc.start(); osc.stop(ac.currentTime + duration);
}

function rectsTouch(a, b) { return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y; }
function block(x, y, w, h, fill) { ctx.fillStyle = fill; ctx.fillRect(Math.round(x), Math.round(y), w, h); }
function safeGroundPosition(targetX) {
  const current = ground.find(g => targetX >= g.x + 20 && targetX <= g.x + g.w - player.w - 20);
  if (current) return { x: targetX, y: current.y - player.h };
  const next = ground.find(g => g.x >= targetX);
  const fallback = next || ground[ground.length - 1];
  return { x: fallback.x + 30, y: fallback.y - player.h };
}
function placePlayerSafely(targetX) {
  const safe = safeGroundPosition(targetX);
  Object.assign(player, { x: safe.x, y: safe.y, vx: 0, vy: 0, onGround: true });
  return safe.x;
}
function updateHud() {
  ui.lives.textContent = `× ${state.lives}`; ui.coins.textContent = String(state.coins).padStart(2, "0");
  ui.keys.textContent = `${state.cleared}/20`; ui.deaths.textContent = String(state.deaths);
  ui.world.textContent = subjects[Math.min(4, Math.floor(state.cleared / 4))].world;
}

function resetGame() {
  Object.assign(state, { lives: 3, coins: 0, cleared: 0, deaths: 0, checkpoint: 60 });
  Object.assign(player, { x: 60, y: 365, vx: 0, vy: 0, onGround: false, dead: false, frame: 0 });
  questions.forEach(q => q.passed = false); coins.forEach(c => c.taken = false); enemies.forEach(e => e.alive = true);
  particles.length = 0; cameraX = 0; won = false; asking = false; paused = false; started = true;
  ui.start.hidden = true; ui.win.hidden = true; ui.question.hidden = true; updateHud();
}

function spawnParticles(x, y, color, count = 12) {
  for (let i = 0; i < count; i++) particles.push({ x, y, vx: (Math.random() - .5) * 7, vy: -Math.random() * 6, life: 38 + Math.random() * 24, color, size: 3 + Math.random() * 5 });
}

function openQuestion(q) {
  activeQuestion = q; asking = true; paused = true; deadline = performance.now() + QUESTION_SECONDS * 1000;
  const subject = subjects[q.subjectIndex];
  ui.question.className = "panel question-panel";
  ui.questionWorld.textContent = `WORLD ${subject.world} • ${q.questionIndex + 1}/4 • TAS INPUT`;
  ui.questionTitle.textContent = subject.name; ui.questionTitle.style.color = subject.color;
  ui.questionCode.textContent = q.code; ui.questionPrompt.textContent = q.prompt;
  ui.feedback.textContent = "Choose before the timer reaches zero."; ui.answers.replaceChildren();
  q.answers.forEach((answer, index) => {
    const button = document.createElement("button"); button.textContent = `${index + 1}. ${answer}`;
    button.addEventListener("click", () => answerQuestion(index, button)); ui.answers.append(button);
  });
  ui.question.hidden = false;
}

function answerQuestion(index, button) {
  if (!asking || player.dead || activeQuestion.passed) return;
  if (index !== activeQuestion.correct) {
    button.classList.add("wrong"); killMario("MISINPUT! Wrong answer."); return;
  }
  button.classList.add("correct"); activeQuestion.passed = true; state.cleared += 1; state.coins += 10;
  // Resume before the cleared gate. This gives the TAS enough runway to
  // evaluate the next pit or enemy instead of teleporting onto level geometry.
  state.checkpoint = placePlayerSafely(activeQuestion.x - 180); ui.question.classList.add("success");
  ui.feedback.textContent = `FRAME PERFECT! ${activeQuestion.explanation}`;
  spawnParticles(player.x, player.y, subjects[activeQuestion.subjectIndex].color, 25);
  beep(760, .09); setTimeout(() => beep(1020, .18), 100); updateHud();
  setTimeout(() => { ui.question.hidden = true; asking = false; paused = false; activeQuestion = null; }, 1200);
}

function killMario(reason) {
  if (player.dead) return;
  player.dead = true; asking = false; paused = false; deathTimer = 85;
  state.deaths += 1; state.lives -= 1; if (state.lives <= 0) state.lives = 3;
  player.vx = 0; player.vy = -13; ui.question.classList.add("danger"); ui.feedback.textContent = `${reason} Mario dies and the TAS retries.`;
  beep(150, .42, "sawtooth"); updateHud();
  setTimeout(() => { ui.question.hidden = true; }, 650);
}

function respawn() {
  placePlayerSafely(Math.max(60, state.checkpoint - 120));
  player.dead = false;
  cameraX = Math.max(0, player.x - W * .35); activeQuestion = null; asking = false; paused = false;
}

function nextObstacleDistance() {
  let nearest = Infinity;
  for (const p of platforms) if (p.x > player.x + player.w && p.x - player.x < nearest) nearest = p.x - player.x;
  for (const e of enemies) if (e.alive && e.x > player.x + player.w && e.x - player.x < nearest) nearest = e.x - player.x;
  for (const g of ground) {
    const edge = g.x + g.w;
    if (player.x >= g.x && player.x < edge && edge - player.x < nearest) {
      const nextGround = ground.find(n => n.x >= edge);
      if (!nextGround || nextGround.x > edge + 20) nearest = edge - player.x;
    }
  }
  return nearest;
}

function updateParticles() {
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i]; p.x += p.vx; p.y += p.vy; p.vy += .22; p.life -= 1;
    if (p.life <= 0) particles.splice(i, 1);
  }
}

function update() {
  updateParticles();
  if (!started || won) return;
  if (asking) {
    const left = Math.max(0, (deadline - performance.now()) / 1000);
    ui.timerText.textContent = left.toFixed(1); ui.timerBar.style.transform = `scaleX(${left / QUESTION_SECONDS})`;
    if (left <= 5) ui.question.classList.add("danger");
    if (left <= 0) killMario("TIMEOUT! No answer received.");
    return;
  }
  if (paused && !player.dead) return;

  if (player.dead) {
    player.y += player.vy; player.vy += .65; player.frame += .2; deathTimer -= 1;
    if (deathTimer <= 0) respawn();
    cameraX += ((player.x - W * .35) - cameraX) * .05; return;
  }

  const speed = 5.1 + Math.min(1.7, state.cleared * .07);
  player.vx += (speed - player.vx) * .08;
  const obstacle = nextObstacleDistance();
  if (player.onGround && obstacle < 105) { player.vy = -13.3; player.onGround = false; beep(390, .06); }
  player.vy += .72; player.vy = Math.min(16, player.vy);
  const previousY = player.y; player.x += player.vx; player.y += player.vy; player.onGround = false;

  for (const solid of ground.concat(platforms)) {
    if (!rectsTouch(player, solid)) continue;
    if (previousY + player.h <= solid.y + 12 && player.vy >= 0) {
      player.y = solid.y - player.h; player.vy = 0; player.onGround = true;
    } else if (previousY >= solid.y + solid.h - 8 && player.vy < 0) {
      player.y = solid.y + solid.h; player.vy = 1;
      if (solid.kind === "question") { state.coins += 1; spawnParticles(player.x, player.y, palette.gold, 8); beep(720, .06); }
    }
  }
  if (player.y > H + 70) { killMario("MISINPUT! Mario missed the platform."); return; }

  coins.forEach(c => {
    c.phase += .06;
    if (!c.taken && Math.hypot(player.x + 18 - c.x, player.y + 24 - c.y) < 32) {
      c.taken = true; state.coins += 1; spawnParticles(c.x, c.y, palette.gold, 7); beep(900, .05);
    }
  });
  enemies.forEach(e => {
    if (!e.alive) return; e.y = 418 + Math.sin(performance.now() / 350 + e.phase) * 2;
    if (rectsTouch(player, e)) {
      if (player.vy > 2 && player.y + player.h - e.y < 22) { e.alive = false; player.vy = -8; state.coins += 2; spawnParticles(e.x, e.y, "#a8623c", 14); beep(250, .07); }
      else killMario("MISINPUT! Mario touched a Goomba.");
    }
  });

  for (const q of questions) {
    if (!q.passed && player.x + player.w >= q.x - 24) { player.x = q.x - player.w - 24; player.vx = 0; openQuestion(q); break; }
  }
  if (player.x > 12320 && state.cleared === 20) {
    won = true; paused = true; ui.finalScore.textContent = `COINS ${state.coins} • MISINPUTS ${state.deaths} • QUESTIONS 20/20`;
    ui.win.hidden = false; beep(523, .1); setTimeout(() => beep(659, .1), 120); setTimeout(() => beep(784, .28), 240);
  }
  cameraX += ((player.x - W * .31) - cameraX) * .085; cameraX = Math.max(0, Math.min(COURSE_END - W, cameraX));
  player.frame += speed * .08; updateHud();
}

function drawBackground() {
  const gradient = ctx.createLinearGradient(0, 0, 0, H);
  gradient.addColorStop(0, palette.skyTop); gradient.addColorStop(.68, palette.skyBottom); gradient.addColorStop(1, "#19132f");
  ctx.fillStyle = gradient; ctx.fillRect(0, 0, W, H);
  const moonX = 795 - cameraX * .018;
  ctx.fillStyle = palette.moon; ctx.beginPath(); ctx.arc(moonX, 86, 57, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = palette.skyTop; ctx.beginPath(); ctx.arc(moonX + 22, 70, 52, 0, Math.PI * 2); ctx.fill();
  for (let i = 0; i < 48; i++) {
    const x = ((i * 149 - cameraX * .06) % (W + 60) + W + 60) % (W + 60) - 30;
    const pulse = 1 + Math.sin(performance.now() / 420 + i) * .7;
    block(x, 24 + (i * 71) % 250, pulse + 1, pulse + 1, i % 4 ? palette.white : palette.gold);
  }
  for (let i = -1; i < 10; i++) {
    const x = i * 330 - (cameraX * .12 % 330), base = 452;
    ctx.fillStyle = i % 2 ? "#292052" : "#33265f";
    ctx.beginPath(); ctx.moveTo(x, base); ctx.quadraticCurveTo(x + 150, 205 - (i % 3) * 25, x + 330, base); ctx.fill();
    block(x + 105, 315, 12, 28, "#18132f"); block(x + 133, 295, 10, 48, "#18132f");
  }
  ctx.fillStyle = "rgba(200,190,255,.09)";
  for (let i = 0; i < 4; i++) ctx.fillRect(0, 365 + i * 22 + Math.sin(performance.now()/700+i)*5, W, 12);
}

function drawGround(g) {
  const x = g.x - cameraX; if (x > W || x + g.w < 0) return;
  block(x, g.y, g.w, g.h, palette.dirt); block(x, g.y, g.w, 9, palette.grassLight); block(x, g.y + 9, g.w, 13, palette.grass);
  for (let bx = 0; bx < g.w; bx += 32) {
    block(x + bx, g.y + 28 + (bx % 64), 16, 9, "#8d492a"); block(x + bx + 16, g.y + 52 - (bx % 32), 16, 9, "#542617");
  }
}

function drawPlatform(p) {
  const x = p.x - cameraX; if (x > W || x + p.w < 0) return;
  if (p.kind === "pipe") {
    block(x + 12, p.y, p.w - 24, p.h, palette.green); block(x, p.y, p.w, 28, palette.green);
    block(x + 10, p.y + 5, 9, p.h - 5, "#8ce56f"); block(x + p.w - 24, p.y + 5, 12, p.h - 5, palette.greenDark);
    block(x, p.y + 24, p.w, 6, "#0d5424"); return;
  }
  const fill = p.kind === "question" ? palette.orange : palette.brick;
  block(x, p.y, p.w, p.h, fill); block(x, p.y + p.h - 6, p.w, 6, palette.brickDark);
  for (let bx = 0; bx < p.w; bx += 30) {
    block(x + bx, p.y, 3, p.h, palette.brickDark); block(x + bx + 4, p.y + 4, 20, 3, "rgba(255,255,255,.25)");
    if (p.kind === "question") { ctx.fillStyle = palette.white; ctx.font = "bold 20px monospace"; ctx.fillText("?", x + bx + 8, p.y + 22); }
  }
}

function drawMario() {
  const x = Math.round(player.x - cameraX), y = Math.round(player.y), run = Math.floor(player.frame) % 2;
  ctx.save(); ctx.translate(x, 0); if (player.dead) ctx.rotate((85 - deathTimer) * .08);
  block(6, y, 23, 6, palette.red); block(11, y - 5, 15, 6, palette.red); block(3, y + 6, 29, 6, palette.redDark);
  block(8, y + 7, 21, 15, palette.skin); block(24, y + 10, 9, 7, palette.skin); block(18, y + 8, 4, 5, palette.black);
  block(8, y + 17, 18, 5, palette.brown); block(4, y + 22, 28, 5, palette.red);
  block(8, y + 25, 21, 14, palette.blue); block(11, y + 23, 5, 12, palette.blueLight); block(23, y + 23, 5, 12, palette.blueLight);
  block(2, y + 25 + run * 2, 8, 12, palette.skin); block(29, y + 25 + (1-run)*2, 7, 12, palette.skin);
  block(7, y + 39 - run*2, 11, 8, palette.brown); block(22, y + 39 - (1-run)*2, 12, 8, palette.brown);
  ctx.restore();
}

function drawGoomba(e) {
  if (!e.alive) return; const x = e.x - cameraX; if (x < -50 || x > W + 50) return;
  block(x + 5, e.y, 24, 7, "#7e3d24"); block(x, e.y + 7, 34, 19, "#a65b37");
  block(x + 6, e.y + 12, 7, 7, palette.white); block(x + 21, e.y + 12, 7, 7, palette.white);
  block(x + 9, e.y + 13, 4, 5, palette.black); block(x + 21, e.y + 13, 4, 5, palette.black);
  block(x + 3, e.y + 26, 13, 7, palette.black); block(x + 20, e.y + 26, 13, 7, palette.black);
}

function drawBoo(worldX, y, scale = 1) {
  const x = worldX - cameraX; if (x < -80 || x > W + 80) return;
  ctx.fillStyle = palette.white; ctx.beginPath(); ctx.arc(x, y, 24*scale, Math.PI, 0); ctx.lineTo(x+24*scale,y+22*scale); ctx.lineTo(x+10*scale,y+15*scale); ctx.lineTo(x,y+23*scale); ctx.lineTo(x-12*scale,y+15*scale); ctx.lineTo(x-24*scale,y+22*scale); ctx.closePath(); ctx.fill();
  block(x-12*scale,y-6*scale,5*scale,8*scale,palette.black); block(x+7*scale,y-6*scale,5*scale,8*scale,palette.black); block(x-3*scale,y+8*scale,14*scale,5*scale,palette.red);
}

function drawGate(q) {
  if (q.passed) return; const x = q.x - cameraX; if (x < -100 || x > W + 100) return;
  const color = subjects[q.subjectIndex].color;
  block(x-28, 205, 70, 247, "#5c566b"); block(x-35, 192, 84, 25, "#8b8498");
  block(x-12, 255, 38, 197, palette.black); block(x-7, 280, 28, 120, "#2d2540");
  block(x-30, 192, 74, 5, color); ctx.fillStyle = color; ctx.font = "bold 15px monospace"; ctx.fillText(`${q.questionIndex+1}/4`, x-8, 242);
  block(x-18, 316, 50, 6, color); block(x+4, 300, 6, 40, color);
}

function drawDecorations() {
  for (let x = 420; x < COURSE_END; x += 760) {
    const px = x - cameraX; if (px < -80 || px > W + 80) continue;
    block(px, 425, 36, 27, "#f07a20"); block(px+13,417,9,10,palette.green);
    block(px+7,433,6,6,palette.black); block(px+24,433,6,6,palette.black); block(px+13,443,10,4,palette.black);
  }
  for (let x = 1350; x < COURSE_END; x += 980) drawBoo(x, 170 + Math.sin(performance.now()/550+x)*24, .9);
  const castleX = 12270 - cameraX;
  if (castleX < W + 400) {
    block(castleX, 175, 310, 277, "#5f596d"); block(castleX+25,110,78,342,"#767083"); block(castleX+205,90,78,362,"#767083");
    block(castleX+110,295,92,157,palette.black); block(castleX+50,240,42,55,"#211b2e"); block(castleX+220,220,42,55,"#211b2e");
    for(let i=0;i<6;i++) block(castleX+i*55,155,34,28,"#8b8498");
    ctx.fillStyle=palette.red; ctx.beginPath();ctx.moveTo(castleX+65,110);ctx.lineTo(castleX+160,135);ctx.lineTo(castleX+65,160);ctx.fill();
  }
}

function drawParticles() { particles.forEach(p => block(p.x-cameraX,p.y,p.size,p.size,p.color)); }

function draw() {
  drawBackground(); drawDecorations(); ground.forEach(drawGround); platforms.forEach(drawPlatform);
  coins.forEach(c => { if(c.taken)return; const x=c.x-cameraX;if(x<-30||x>W+30)return;const y=c.y+Math.sin(c.phase)*6;block(x-7,y-13,14,26,palette.gold);block(x-2,y-9,4,18,"#fff5a4"); });
  questions.forEach(drawGate); enemies.forEach(drawGoomba); drawParticles(); drawMario();
  if (started && !asking && !won) {
    ctx.fillStyle="rgba(10,6,28,.82)";ctx.fillRect(14,14,260,32);ctx.fillStyle=palette.green;ctx.font="bold 15px monospace";ctx.fillText("TAS AUTO-RUN • INPUT LOCKED",27,36);
  }
  if (paused && !asking && started && !won && !player.dead) {ctx.fillStyle="rgba(0,0,0,.58)";ctx.fillRect(0,0,W,H);ctx.fillStyle=palette.white;ctx.font="bold 42px monospace";ctx.fillText("PAUSED",W/2-85,H/2);}
}

function loop(timestamp) { lastTime=timestamp; update(); draw(); requestAnimationFrame(loop); }
window.addEventListener("keydown", event => {
  const key=event.key.length===1?event.key.toLowerCase():event.key;
  if(!started&&event.key==="Enter")resetGame();
  if(key==="p"&&started&&!asking&&!won&&!player.dead)paused=!paused;
  if(asking&&["1","2","3"].includes(key))ui.answers.children[Number(key)-1]?.click();
  held.add(key);
});
window.addEventListener("keyup",event=>held.delete(event.key.length===1?event.key.toLowerCase():event.key));
ui.restart.addEventListener("click",resetGame);
ui.sound.addEventListener("click",()=>{audioOn=!audioOn;ui.sound.textContent=`SOUND: ${audioOn?"ON":"OFF"}`;});
updateHud();requestAnimationFrame(loop);
