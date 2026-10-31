"use strict";

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

const ui = {
  lives: document.getElementById("lives"),
  coins: document.getElementById("coins"),
  keys: document.getElementById("keys"),
  world: document.getElementById("worldLabel"),
  start: document.getElementById("startScreen"),
  question: document.getElementById("questionPanel"),
  questionWorld: document.getElementById("questionWorld"),
  questionTitle: document.getElementById("questionTitle"),
  questionCode: document.getElementById("questionCode"),
  questionPrompt: document.getElementById("questionPrompt"),
  answers: document.getElementById("answers"),
  feedback: document.getElementById("feedback"),
  win: document.getElementById("winPanel"),
  finalScore: document.getElementById("finalScore"),
  restart: document.getElementById("restartButton"),
  sound: document.getElementById("soundButton"),
};

const W = canvas.width;
const H = canvas.height;
const WORLD_WIDTH = 6500;
const GRAVITY = 0.72;
const keys = new Set();
let audioOn = true;
let started = false;
let paused = false;
let asking = false;
let won = false;
let cameraX = 0;
let lastTime = 0;

const palette = {
  sky: "#17103c", sky2: "#2b1b62", moon: "#fff2a8", cloud: "#d9d4ff",
  ground: "#6b351d", groundTop: "#54b948", brick: "#bd522b", mortar: "#742617",
  pipe: "#38ad4d", pipeDark: "#176c32", coin: "#ffd735", question: "#ff9f1c",
  marioRed: "#e63232", marioBlue: "#2874d0", skin: "#f2ad72", black: "#171018",
  boo: "#f5f3ff", purple: "#7b4aba", lava: "#ff5a1f", white: "#fff",
};

const state = { lives: 3, coins: 0, pythonKeys: 0, checkpoint: 80 };
const player = { x: 80, y: 360, w: 34, h: 46, vx: 0, vy: 0, onGround: false, invincible: 0, frame: 0 };

const ground = [
  { x: 0, y: 460, w: 1220, h: 80 }, { x: 1320, y: 460, w: 1180, h: 80 },
  { x: 2600, y: 460, w: 1050, h: 80 }, { x: 3750, y: 460, w: 1230, h: 80 },
  { x: 5100, y: 460, w: 1400, h: 80 },
];

const platforms = [
  { x: 270, y: 365, w: 150, h: 30, kind: "brick" }, { x: 510, y: 310, w: 180, h: 30, kind: "brick" },
  { x: 820, y: 360, w: 130, h: 30, kind: "question" }, { x: 1080, y: 330, w: 90, h: 130, kind: "pipe" },
  { x: 1370, y: 370, w: 170, h: 28, kind: "brick" }, { x: 1650, y: 300, w: 180, h: 28, kind: "question" },
  { x: 1930, y: 360, w: 120, h: 28, kind: "brick" }, { x: 2230, y: 320, w: 100, h: 140, kind: "pipe" },
  { x: 2680, y: 365, w: 200, h: 28, kind: "brick" }, { x: 2990, y: 295, w: 160, h: 28, kind: "question" },
  { x: 3370, y: 350, w: 160, h: 28, kind: "brick" }, { x: 3580, y: 300, w: 70, h: 160, kind: "pipe" },
  { x: 3830, y: 370, w: 160, h: 28, kind: "brick" }, { x: 4100, y: 310, w: 200, h: 28, kind: "question" },
  { x: 4440, y: 350, w: 130, h: 28, kind: "brick" }, { x: 4760, y: 300, w: 100, h: 160, kind: "pipe" },
  { x: 5160, y: 360, w: 180, h: 28, kind: "brick" }, { x: 5470, y: 300, w: 180, h: 28, kind: "question" },
  { x: 5770, y: 370, w: 150, h: 28, kind: "brick" }, { x: 6120, y: 320, w: 180, h: 28, kind: "castle" },
];

const coins = [350, 565, 625, 870, 1450, 1700, 1770, 2000, 2730, 2820, 3040, 3110, 3410, 3890, 4160, 4240, 4510, 5220, 5300, 5530, 5600, 5830].map((x, i) => ({ x, y: i % 3 === 0 ? 300 : 405, r: 11, taken: false, bob: i * .6 }));

const enemies = [620, 940, 1510, 1860, 2780, 3450, 3950, 4490, 5250, 5710].map((x, i) => ({ x, y: 420, w: 34, h: 32, vx: i % 2 ? 1.05 : -1.05, start: x - 90, end: x + 90, alive: true }));

const questions = [
  { x: 1120, world: "WORLD 1-1", title: "VARIABLES + LISTS", code: 'items = ["mushroom", "key"]\nitems.append("star")\nprint(len(items))', prompt: "What prints?", answers: ["2", "3", "star"], correct: 1, explanation: "append adds one item. The list length becomes 3." },
  { x: 2320, world: "WORLD 2-1", title: "IF CONDITIONS + LOGIC", code: "has_key = True\nboo_awake = False\nif has_key and not boo_awake:\n    print(\"GO!\")", prompt: "Does GO! print?", answers: ["Yes", "No", "Only in a loop"], correct: 0, explanation: "True and not False evaluates to True." },
  { x: 3520, world: "WORLD 3-1", title: "FOR LOOP", code: "total = 0\nfor coin in [2, 4, 6]:\n    total = total + coin", prompt: "What is total after the loop?", answers: ["6", "10", "12"], correct: 2, explanation: "The accumulator changes 0 → 2 → 6 → 12." },
  { x: 4720, world: "WORLD 4-1", title: "WHILE LOOP", code: 'pipe = "wrong"\nwhile pipe != "exit":\n    pipe = choose_pipe()', prompt: "When does the loop stop?", answers: ["After 3 turns", "When pipe is exit", "Never"], correct: 1, explanation: "The loop stops when pipe != exit becomes False." },
  { x: 5720, world: "WORLD 5-1", title: "FUNCTIONS", code: "def power(base, bonus):\n    return base + bonus\n\nresult = power(7, 5)", prompt: "What value is returned?", answers: ["5", "7", "12"], correct: 2, explanation: "The arguments 7 and 5 become parameters and return 12." },
];

function beep(frequency = 440, duration = .08, type = "square") {
  if (!audioOn) return;
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if (!AudioContext) return;
  const ac = beep.ac || (beep.ac = new AudioContext());
  const osc = ac.createOscillator();
  const gain = ac.createGain();
  osc.type = type; osc.frequency.value = frequency;
  gain.gain.setValueAtTime(.05, ac.currentTime);
  gain.gain.exponentialRampToValueAtTime(.001, ac.currentTime + duration);
  osc.connect(gain).connect(ac.destination); osc.start(); osc.stop(ac.currentTime + duration);
}

function resetGame() {
  Object.assign(state, { lives: 3, coins: 0, pythonKeys: 0, checkpoint: 80 });
  Object.assign(player, { x: 80, y: 360, vx: 0, vy: 0, invincible: 0 });
  coins.forEach(c => c.taken = false); enemies.forEach(e => e.alive = true);
  questions.forEach(q => q.passed = false);
  won = false; asking = false; started = true; paused = false;
  ui.win.hidden = true; ui.start.hidden = true; updateHud();
}

function updateHud() {
  ui.lives.textContent = `× ${state.lives}`;
  ui.coins.textContent = String(state.coins).padStart(2, "0");
  ui.keys.textContent = `${state.pythonKeys}/5`;
  const section = Math.min(5, Math.floor(player.x / 1200) + 1);
  ui.world.textContent = `${section}-1`;
}

function rectsTouch(a, b) { return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y; }

function respawn() {
  state.lives = Math.max(0, state.lives - 1);
  if (state.lives === 0) state.lives = 3;
  Object.assign(player, { x: state.checkpoint, y: 350, vx: 0, vy: 0, invincible: 90 });
  beep(130, .25, "sawtooth"); updateHud();
}

function openQuestion(q) {
  asking = true; paused = true;
  ui.questionWorld.textContent = `${q.world} • PYTHON GATE`;
  ui.questionTitle.textContent = q.title;
  ui.questionCode.textContent = q.code;
  ui.questionPrompt.textContent = q.prompt;
  ui.feedback.textContent = "Choose an answer to unlock the gate.";
  ui.answers.replaceChildren();
  q.answers.forEach((answer, index) => {
    const button = document.createElement("button");
    button.textContent = `${index + 1}. ${answer}`;
    button.addEventListener("click", () => answerQuestion(q, index, button));
    ui.answers.append(button);
  });
  ui.question.hidden = false;
}

function answerQuestion(q, index, button) {
  if (q.passed) return;
  if (index !== q.correct) {
    button.classList.add("wrong");
    ui.feedback.textContent = "A Goomba stole that answer. Trace the code and try again.";
    beep(170, .18, "sawtooth"); return;
  }
  button.classList.add("correct");
  q.passed = true; state.pythonKeys += 1; state.coins += 10; state.checkpoint = q.x + 70;
  ui.feedback.textContent = `PYTHON KEY FOUND! ${q.explanation}`;
  beep(760, .1); setTimeout(() => beep(980, .16), 100);
  updateHud();
  setTimeout(() => { ui.question.hidden = true; asking = false; paused = false; }, 1400);
}

function update(dt) {
  if (!started || paused || won) return;
  const speed = 4.5;
  const left = keys.has("ArrowLeft") || keys.has("a");
  const right = keys.has("ArrowRight") || keys.has("d");
  player.vx += (right - left) * .75;
  player.vx *= .82; player.vx = Math.max(-speed, Math.min(speed, player.vx));
  const jump = keys.has("ArrowUp") || keys.has("w") || keys.has(" ");
  if (jump && player.onGround) { player.vy = -13.2; player.onGround = false; beep(390, .08); }
  player.vy += GRAVITY; player.vy = Math.min(player.vy, 16);

  const previousY = player.y;
  player.x += player.vx; player.x = Math.max(0, Math.min(WORLD_WIDTH - player.w, player.x));
  player.y += player.vy; player.onGround = false;
  const solids = ground.concat(platforms);
  for (const solid of solids) {
    if (!rectsTouch(player, solid)) continue;
    if (previousY + player.h <= solid.y + 10 && player.vy >= 0) {
      player.y = solid.y - player.h; player.vy = 0; player.onGround = true;
    } else if (previousY >= solid.y + solid.h - 8 && player.vy < 0) {
      player.y = solid.y + solid.h; player.vy = 1;
      if (solid.kind === "question") { state.coins += 1; beep(700, .08); updateHud(); }
    } else if (player.x < solid.x) player.x = solid.x - player.w;
    else player.x = solid.x + solid.w;
  }

  if (player.y > H + 80) respawn();
  if (player.invincible > 0) player.invincible -= 1;

  for (const coin of coins) {
    coin.bob += .06;
    if (!coin.taken && Math.hypot(player.x + player.w / 2 - coin.x, player.y + player.h / 2 - coin.y) < 34) {
      coin.taken = true; state.coins += 1; beep(880, .07); updateHud();
    }
  }

  for (const enemy of enemies) {
    if (!enemy.alive) continue;
    enemy.x += enemy.vx; if (enemy.x < enemy.start || enemy.x > enemy.end) enemy.vx *= -1;
    if (rectsTouch(player, enemy)) {
      if (player.vy > 2 && player.y + player.h - enemy.y < 20) {
        enemy.alive = false; player.vy = -8; state.coins += 2; beep(260, .08); updateHud();
      } else if (player.invincible <= 0) respawn();
    }
  }

  for (const q of questions) {
    if (!q.passed && player.x + player.w > q.x - 28) { player.x = q.x - player.w - 28; player.vx = 0; openQuestion(q); break; }
  }

  if (player.x > 6230 && state.pythonKeys === 5) {
    won = true; paused = true; ui.finalScore.textContent = `COINS: ${state.coins} • LIVES: ${state.lives} • PYTHON KEYS: 5/5`;
    ui.win.hidden = false; beep(523, .12); setTimeout(() => beep(659, .12), 140); setTimeout(() => beep(784, .3), 280);
  }

  cameraX += ((player.x - W * .36) - cameraX) * .08;
  cameraX = Math.max(0, Math.min(WORLD_WIDTH - W, cameraX));
  player.frame += Math.abs(player.vx) * .08;
}

function drawPixelRect(x, y, w, h, fill) { ctx.fillStyle = fill; ctx.fillRect(Math.round(x), Math.round(y), w, h); }

function drawBackground() {
  const gradient = ctx.createLinearGradient(0, 0, 0, H);
  gradient.addColorStop(0, palette.sky); gradient.addColorStop(1, palette.sky2);
  ctx.fillStyle = gradient; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = palette.moon; ctx.beginPath(); ctx.arc(780 - cameraX * .04, 95, 55, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = palette.sky; ctx.beginPath(); ctx.arc(800 - cameraX * .04, 80, 48, 0, Math.PI * 2); ctx.fill();
  for (let i = 0; i < 34; i++) {
    const sx = ((i * 173 - cameraX * .08) % (W + 80) + W + 80) % (W + 80) - 40;
    drawPixelRect(sx, 35 + (i * 67) % 220, 3, 3, i % 3 ? "#fff" : "#ffd33d");
  }
  for (let i = 0; i < 10; i++) {
    const x = i * 720 - cameraX * .22;
    ctx.fillStyle = i % 2 ? "#241851" : "#302066";
    ctx.beginPath(); ctx.moveTo(x, 460); ctx.lineTo(x + 280, 170); ctx.lineTo(x + 560, 460); ctx.fill();
  }
}

function drawGroundBlock(s) {
  const x = s.x - cameraX; if (x > W || x + s.w < 0) return;
  drawPixelRect(x, s.y, s.w, s.h, palette.ground);
  drawPixelRect(x, s.y, s.w, 14, palette.groundTop);
  for (let bx = x; bx < x + s.w; bx += 38) drawPixelRect(bx, s.y + 26, 4, 4, "#9a5633");
}

function drawPlatform(p) {
  const x = p.x - cameraX; if (x > W || x + p.w < 0) return;
  if (p.kind === "pipe") {
    drawPixelRect(x + 12, p.y, p.w - 24, p.h, palette.pipe);
    drawPixelRect(x, p.y, p.w, 28, palette.pipe); drawPixelRect(x + 12, p.y + 6, 10, p.h - 6, "#76dc68");
    drawPixelRect(x + p.w - 24, p.y + 6, 12, p.h - 6, palette.pipeDark); return;
  }
  const fill = p.kind === "question" ? palette.question : p.kind === "castle" ? "#77718d" : palette.brick;
  drawPixelRect(x, p.y, p.w, p.h, fill); drawPixelRect(x, p.y + p.h - 6, p.w, 6, palette.mortar);
  for (let bx = 0; bx < p.w; bx += 38) {
    drawPixelRect(x + bx, p.y, 4, p.h, palette.mortar);
    if (p.kind === "question") { ctx.fillStyle = "#fff"; ctx.font = "bold 22px monospace"; ctx.fillText("?", x + bx + 10, p.y + 23); }
  }
}

function drawMario() {
  if (player.invincible > 0 && Math.floor(player.invincible / 4) % 2) return;
  const x = Math.round(player.x - cameraX), y = Math.round(player.y);
  const flip = player.vx < -.1;
  ctx.save(); if (flip) { ctx.translate(x + player.w, 0); ctx.scale(-1, 1); } else ctx.translate(x, 0);
  drawPixelRect(5, y, 23, 7, palette.marioRed); drawPixelRect(10, y - 4, 14, 5, palette.marioRed);
  drawPixelRect(7, y + 7, 21, 14, palette.skin); drawPixelRect(22, y + 10, 8, 7, palette.skin);
  drawPixelRect(18, y + 8, 4, 4, palette.black); drawPixelRect(5, y + 17, 20, 5, "#6b2b18");
  drawPixelRect(7, y + 22, 22, 16, palette.marioBlue); drawPixelRect(4, y + 23, 7, 13, palette.marioRed); drawPixelRect(28, y + 23, 6, 13, palette.marioRed);
  drawPixelRect(8, y + 38, 9, 8, palette.black); drawPixelRect(22, y + 38, 10, 8, palette.black);
  ctx.restore();
}

function drawEnemy(e) {
  const x = e.x - cameraX; if (x < -50 || x > W + 50 || !e.alive) return;
  drawPixelRect(x + 5, e.y, 24, 7, "#8b4a2d"); drawPixelRect(x, e.y + 7, 34, 18, "#a85d36");
  drawPixelRect(x + 7, e.y + 12, 5, 6, palette.white); drawPixelRect(x + 22, e.y + 12, 5, 6, palette.white);
  drawPixelRect(x + 3, e.y + 25, 12, 7, palette.black); drawPixelRect(x + 20, e.y + 25, 12, 7, palette.black);
}

function drawBoo(x, y, scale = 1) {
  x -= cameraX;
  ctx.fillStyle = palette.boo; ctx.beginPath(); ctx.arc(x, y, 24 * scale, Math.PI, 0); ctx.lineTo(x + 24 * scale, y + 22 * scale); ctx.lineTo(x, y + 14 * scale); ctx.lineTo(x - 24 * scale, y + 22 * scale); ctx.closePath(); ctx.fill();
  drawPixelRect(x - 12 * scale, y - 5 * scale, 5 * scale, 8 * scale, palette.black); drawPixelRect(x + 7 * scale, y - 5 * scale, 5 * scale, 8 * scale, palette.black);
  drawPixelRect(x - 5 * scale, y + 9 * scale, 14 * scale, 4 * scale, palette.marioRed);
}

function drawGate(q) {
  if (q.passed) return;
  const x = q.x - cameraX; if (x < -100 || x > W + 100) return;
  drawPixelRect(x - 20, 210, 58, 250, "#675d78"); drawPixelRect(x - 27, 200, 72, 24, "#8d849d");
  drawPixelRect(x - 8, 270, 34, 190, "#261c39");
  ctx.fillStyle = palette.gold || "#ffd735"; ctx.font = "bold 18px monospace"; ctx.fillText("PY", x - 3, 252);
}

function drawDecorations() {
  for (let x = 420; x < WORLD_WIDTH; x += 780) {
    const px = x - cameraX; if (px > -100 && px < W + 100) {
      drawPixelRect(px, 432, 34, 28, "#ed7c22"); drawPixelRect(px + 12, 424, 8, 10, "#3a8c43");
      drawPixelRect(px + 8, 440, 5, 5, palette.black); drawPixelRect(px + 22, 440, 5, 5, palette.black);
    }
  }
  for (let x = 1500; x < WORLD_WIDTH; x += 1100) drawBoo(x, 170 + (x % 90), .85);
  const castleX = 6160 - cameraX;
  if (castleX < W + 400) {
    drawPixelRect(castleX, 190, 280, 270, "#665e75"); drawPixelRect(castleX + 30, 130, 70, 330, "#777080"); drawPixelRect(castleX + 185, 110, 70, 350, "#777080");
    drawPixelRect(castleX + 100, 310, 85, 150, "#171018");
    for (let i = 0; i < 5; i++) drawPixelRect(castleX + i * 58, 175, 34, 28, "#8e8599");
    ctx.fillStyle = palette.marioRed; ctx.beginPath(); ctx.moveTo(castleX + 65, 130); ctx.lineTo(castleX + 145, 150); ctx.lineTo(castleX + 65, 170); ctx.fill();
  }
}

function draw() {
  drawBackground(); drawDecorations(); ground.forEach(drawGroundBlock); platforms.forEach(drawPlatform);
  for (const coin of coins) {
    if (coin.taken) continue; const x = coin.x - cameraX; if (x < -30 || x > W + 30) continue;
    const y = coin.y + Math.sin(coin.bob) * 6; drawPixelRect(x - 7, y - 13, 14, 26, palette.coin); drawPixelRect(x - 3, y - 9, 4, 18, "#fff39a");
  }
  questions.forEach(drawGate); enemies.forEach(drawEnemy); drawMario();
  if (paused && !asking && started && !won) { ctx.fillStyle = "rgba(0,0,0,.55)"; ctx.fillRect(0,0,W,H); ctx.fillStyle = "#fff"; ctx.font = "bold 42px monospace"; ctx.fillText("PAUSED", W/2-85, H/2); }
}

function loop(timestamp) {
  const dt = Math.min(2, (timestamp - lastTime) / 16.67 || 1); lastTime = timestamp;
  update(dt); draw(); requestAnimationFrame(loop);
}

window.addEventListener("keydown", event => {
  const key = event.key.length === 1 ? event.key.toLowerCase() : event.key;
  if (["ArrowLeft", "ArrowRight", "ArrowUp", " "].includes(key)) event.preventDefault();
  if (!started && event.key === "Enter") resetGame();
  if (key === "p" && started && !asking && !won) paused = !paused;
  if (asking && ["1", "2", "3"].includes(key)) ui.answers.children[Number(key) - 1]?.click();
  keys.add(key);
});
window.addEventListener("keyup", event => keys.delete(event.key.length === 1 ? event.key.toLowerCase() : event.key));
ui.restart.addEventListener("click", resetGame);
ui.sound.addEventListener("click", () => { audioOn = !audioOn; ui.sound.textContent = `SOUND: ${audioOn ? "ON" : "OFF"}`; });

updateHud(); requestAnimationFrame(loop);
