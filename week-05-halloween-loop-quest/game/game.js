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
const COURSE_END = 12600, QUESTION_SECONDS = 20;
const TEST_MODE = new URLSearchParams(window.location.search).has("autotest");
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
let musicTimer = null, musicStep = 0, bossTimer = 0, deathStyle = "bonk", deathReason = "";
let transitionTimer = 0, transitionFromWorld = 0;
let transitionGroundY = 365, fireballCooldown = 0;
let autoJump = null;
const held = new Set();
const state = { lives: 3, coins: 0, cleared: 0, deaths: 0, checkpoint: 60 };
const player = { x: 60, y: 365, w: 36, h: 48, vx: 0, vy: 0, onGround: false, dead: false, frame: 0, form: "small" };
const particles = [];
const fireballs = [];
const boss = { x: 11910, y: 354, w: 96, h: 98, defeated: false };

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
    ['count = 0\nfor number in [4, 8, 12, 16]:\n    count += 1', "What is count?", ["3", "4", "5"], 1, "The list contains four values, so the loop runs four times."],
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
const enemies = Array.from({ length: 44 }, (_, i) => ({
  x: 500 + i * 270, y: 418, w: 34, h: 34, alive: true, phase: i,
  kind: i % 7 === 3 ? "koopa" : i % 11 === 6 ? "spiny" : "goomba",
}));

function beep(frequency = 440, duration = .08, type = "square", volume = .045, delay = 0) {
  if (!audioOn) return;
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if (!AudioContext) return;
  const ac = beep.ac || (beep.ac = new AudioContext());
  if (ac.state === "suspended") ac.resume();
  const osc = ac.createOscillator(), gain = ac.createGain();
  osc.type = type; osc.frequency.value = frequency;
  const start = ac.currentTime + delay;
  gain.gain.setValueAtTime(volume, start);
  gain.gain.exponentialRampToValueAtTime(.001, start + duration);
  osc.connect(gain).connect(ac.destination); osc.start(start); osc.stop(start + duration);
}

function wobble(startFrequency, endFrequency, duration = .2, type = "sawtooth", volume = .03, delay = 0) {
  if (!audioOn) return;
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if (!AudioContext) return;
  const ac = beep.ac || (beep.ac = new AudioContext());
  if (ac.state === "suspended") ac.resume();
  const osc = ac.createOscillator(), gain = ac.createGain();
  const start = ac.currentTime + delay;
  osc.type = type;
  osc.frequency.setValueAtTime(startFrequency, start);
  osc.frequency.exponentialRampToValueAtTime(Math.max(20, endFrequency), start + duration);
  gain.gain.setValueAtTime(volume, start);
  gain.gain.exponentialRampToValueAtTime(.001, start + duration);
  osc.connect(gain).connect(ac.destination); osc.start(start); osc.stop(start + duration);
}

// Five original chiptune themes. The soundtrack changes with each Python world
// and continues under the question panel so the quiz keeps its game-show energy.
const musicWorlds = [
  { lead: [659,784,988,784,659,523,587,659,698,880,1047,880,698,587,659,698], bass: [131,196,147,220] },
  { lead: [440,523,659,622,523,440,392,415,440,554,698,659,554,466,415,392], bass: [110,165,123,185] },
  { lead: [523,659,784,1047,988,784,659,587,659,784,880,784,698,659,587,523], bass: [131,196,175,220] },
  { lead: [330,392,466,554,523,466,392,349,330,415,494,587,554,494,415,370], bass: [82,123,92,139] },
  { lead: [262,311,392,466,392,311,277,330,262,349,415,494,415,349,311,277], bass: [65,98,73,110] },
];
function startMusic() {
  if (musicTimer || TEST_MODE) return;
  musicTimer = setInterval(() => {
    if (!audioOn || won || !started) return;
    const worldIndex = Math.min(4, Math.floor(state.cleared / 4));
    const theme = musicWorlds[worldIndex];
    const step = musicStep++;
    const note = theme.lead[step % theme.lead.length];
    const bassNote = theme.bass[Math.floor(step / 4) % theme.bass.length];
    // Lead melody, quiet bass, offbeat sparkle, and deliberately silly interruptions.
    const cartoonNote = step % 13 === 12 ? note * 1.07 : note;
    beep(cartoonNote, .11, step % 4 === 3 ? "triangle" : "square", asking ? .018 : .026);
    if (step % 2 === 0) beep(bassNote, .22, "triangle", asking ? .012 : .019);
    if (step % 4 === 2) beep(note * 2, .035, "sine", .009, .055);
    beep(step % 4 === 0 ? 74 : 96, .025, "square", .006);
    if (step % 16 === 7) wobble(note * 1.7, note * .55, .19, "square", asking ? .009 : .017);
    if (step % 32 === 23) {
      beep(1175, .045, "square", .018); beep(880, .045, "square", .018, .055);
      beep(1319, .07, "square", .018, .11);
    }
  }, 132);
}

function playDeathJingle() {
  // Original fake victory fanfare that loses control and falls down the stairs.
  const sparkle = [659, 784, 988, 1175, 1047, 831, 622, 466];
  const bass = [165, 196, 220, 139];
  sparkle.forEach((note, index) => {
    const crookedNote = index > 4 ? note * (index % 2 ? .93 : 1.06) : note;
    beep(crookedNote, .12, index % 2 ? "square" : "triangle", .055, index * .105);
    if (index % 2 === 0) beep(bass[index / 2], .19, "sawtooth", .025, index * .105);
  });
  // Slide whistle, two clown honks, a tiny squeak, and the final tuba collapse.
  wobble(1200, 95, .62, "sine", .065, .78);
  wobble(180, 420, .16, "square", .05, .92);
  wobble(170, 390, .16, "square", .05, 1.10);
  beep(1568, .055, "square", .045, 1.29);
  beep(74, .18, "sawtooth", .08, 1.37);
  wobble(110, 42, .62, "sawtooth", .075, 1.48);
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
  Object.assign(player, { x: 60, y: 365, vx: 0, vy: 0, onGround: false, dead: false, frame: 0, form: "small" });
  questions.forEach(q => q.passed = false); coins.forEach(c => c.taken = false); enemies.forEach(e => e.alive = true);
  boss.defeated = false; bossTimer = 0;
  particles.length = 0; fireballs.length = 0; autoJump = null; cameraX = 0; won = false; asking = false; paused = false; transitionTimer = 0; started = true;
  startMusic();
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
  // Hidden smoke-test mode lets us verify every gate without changing class play.
  if (TEST_MODE) setTimeout(() => answerQuestion(q.correct, ui.answers.children[q.correct]), 20);
}

function answerQuestion(index, button) {
  if (!asking || player.dead || activeQuestion.passed) return;
  if (index !== activeQuestion.correct) {
    button.classList.add("wrong"); killMario("MISINPUT! Wrong answer."); return;
  }
  // Stop the countdown immediately. Previously, a last-second correct answer
  // could time out during its 1.2-second success message and play a fake death.
  asking = false;
  button.classList.add("correct"); activeQuestion.passed = true; state.cleared += 1; state.coins += 10;
  // A correct answer is always a win. Resume beyond the cleared gate on solid
  // ground so a success can never look like a pit death or enemy collision.
  autoJump = null;
  state.checkpoint = placePlayerSafely(activeQuestion.x + 90); ui.question.classList.add("success");
  ui.feedback.textContent = `FRAME PERFECT! ${activeQuestion.explanation}`;
  spawnParticles(player.x, player.y, subjects[activeQuestion.subjectIndex].color, 25);
  beep(760, .09); setTimeout(() => beep(1020, .18), 100); updateHud();
  const worldClear = state.cleared % 4 === 0 && state.cleared < 20;
  setTimeout(() => {
    ui.question.hidden = true; asking = false; activeQuestion = null;
    if (worldClear) startWorldTransition(); else paused = false;
  }, TEST_MODE ? 20 : 1200);
}

function startWorldTransition() {
  transitionFromWorld = Math.max(0, Math.floor(state.cleared / 4) - 1);
  transitionTimer = TEST_MODE ? 1 : 240;
  transitionGroundY = player.y;
  player.vx = 0; player.vy = 0; player.onGround = false;
  fireballs.length = 0; fireballCooldown = 0;
  paused = false;
  spawnParticles(player.x, player.y, palette.gold, 55);
  beep(523, .1, "square", .05); beep(659, .1, "square", .05, .11); beep(784, .2, "square", .05, .22);
}

function killMario(reason) {
  if (player.dead) return;
  player.dead = true; asking = false; paused = false; deathTimer = 150; deathReason = reason;
  state.deaths += 1; state.lives -= 1; if (state.lives <= 0) state.lives = 3;
  deathStyle = reason.startsWith("TIMEOUT") ? "timeout" : ["bonk", "bug", "yeet"][state.deaths % 3];
  player.vx = 0; player.vy = -13; ui.question.classList.add("danger"); ui.feedback.textContent = `${reason} Mario dies and the TAS retries.`;
  playDeathJingle();
  if (deathStyle === "timeout") beep(880, .055, "square", .04, .02);
  updateHud();
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

function nextPitDistance() {
  const feetX = player.x + player.w / 2;
  const floor = ground.find(g => feetX >= g.x && feetX <= g.x + g.w);
  return floor ? floor.x + floor.w - (player.x + player.w) : Infinity;
}

function nextGroundAfterPlayer() {
  return ground.find(g => g.x > player.x + player.w);
}

function hasFloorUnderPlayer() {
  const leftFoot = player.x + 6, rightFoot = player.x + player.w - 6;
  return ground.some(g => rightFoot >= g.x && leftFoot <= g.x + g.w);
}

function updateParticles() {
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i]; p.x += p.vx; p.y += p.vy; p.vy += .22; p.life -= 1;
    if (p.life <= 0) particles.splice(i, 1);
  }
}

function launchFireball() {
  fireballs.push({ x: player.x + player.w, y: player.y + 22, vx: 10.5, vy: -2.8, life: 95, spin: 0 });
  beep(520, .05, "square", .035); wobble(760, 390, .1, "sine", .025);
}

function updateFireballs() {
  for (let i = fireballs.length - 1; i >= 0; i--) {
    const ball = fireballs[i]; ball.x += ball.vx; ball.y += ball.vy; ball.vy += .18; ball.spin += .35; ball.life -= 1;
    if (ball.y > GROUND_Y - 12) ball.vy = -4.8;
    for (const enemy of enemies) {
      if (!enemy.alive || Math.abs(ball.x - (enemy.x + enemy.w / 2)) > 28 || Math.abs(ball.y - (enemy.y + enemy.h / 2)) > 28) continue;
      enemy.alive = false; ball.life = 0; state.coins += 2;
      spawnParticles(enemy.x + 16, enemy.y + 14, palette.orange, 28); beep(180, .06, "square", .035);
      break;
    }
    if (ball.life <= 0) fireballs.splice(i, 1);
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
  if (transitionTimer > 0) {
    const transitionElapsed = 240 - transitionTimer;
    // Keep advancing through the same open world, but do not fly past the
    // first gate of the next concept while the class is watching the cutscene.
    player.x += 1.4;
    if (transitionElapsed > 55 && transitionElapsed < 145) {
      player.form = "fire";
      player.y = transitionGroundY - Math.sin((transitionElapsed - 55) / 90 * Math.PI) * 38;
      fireballCooldown -= 1;
      if (transitionElapsed > 70 && fireballCooldown <= 0) { launchFireball(); fireballCooldown = 22; }
    }
    if (transitionElapsed >= 145) {
      player.form = "tanooki";
      const flight = Math.min(1, (transitionElapsed - 145) / 55);
      const landing = Math.max(0, (transitionElapsed - 215) / 25);
      player.y = transitionGroundY - Math.sin(flight * Math.PI / 2) * 215 + landing * 215;
      player.frame += .7;
    }
    updateFireballs();
    cameraX += ((player.x - W * .31) - cameraX) * .07;
    transitionTimer -= 1;
    if (transitionTimer === 0) {
      placePlayerSafely(player.x + 30);
      state.checkpoint = player.x;
      player.form = "tanooki";
      spawnParticles(player.x, player.y, palette.gold, 40);
      beep(784, .08); beep(988, .08, "square", .05, .09); beep(1319, .22, "square", .05, .18);
    }
    updateHud();
    return;
  }
  if (paused && !player.dead) return;

  if (player.dead) {
    player.y += player.vy; player.vy += .65; player.frame += .2; deathTimer -= 1;
    if (deathTimer <= 0) respawn();
    cameraX += ((player.x - W * .35) - cameraX) * .05; return;
  }

  updateFireballs();

  const speed = TEST_MODE ? 36 : 7.4 + Math.min(2.1, state.cleared * .09);
  player.vx += (speed - player.vx) * .14;
  const obstacle = nextObstacleDistance();
  const pit = nextPitDistance();
  if (player.onGround && pit < 175) {
    const landing = nextGroundAfterPlayer();
    if (landing) {
      autoJump = {
        startX: player.x,
        startY: player.y,
        targetX: landing.x + 54,
        targetY: landing.y - player.h,
        progress: 0,
      };
      player.onGround = false;
      spawnParticles(player.x+8, player.y+player.h, palette.white, 16);
      spawnParticles(player.x+18, player.y+player.h, palette.gold, 10); beep(440, .07);
    }
  } else if (player.onGround && obstacle < 125) {
    player.vy = -15.4; player.onGround = false;
    spawnParticles(player.x+8, player.y+player.h, palette.white, 12);
    spawnParticles(player.x+18, player.y+player.h, palette.gold, 8); beep(390, .06);
  }
  if (autoJump) {
    const jumpDistance = autoJump.targetX - autoJump.startX;
    autoJump.progress = Math.min(1, autoJump.progress + speed / jumpDistance);
    const t = autoJump.progress;
    player.x = autoJump.startX + jumpDistance * t;
    player.y = autoJump.startY + (autoJump.targetY - autoJump.startY) * t - Math.sin(t * Math.PI) * 145;
    player.vx = speed; player.vy = 0; player.onGround = false;
    if (t >= 1) {
      player.x = autoJump.targetX; player.y = autoJump.targetY;
      player.vy = 0; player.onGround = true; autoJump = null;
      spawnParticles(player.x + 12, player.y + player.h, palette.white, 12); beep(620, .05);
    }
  } else {
    player.vy += .68; player.vy = Math.min(16, player.vy);
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
  }
  // The auto-run should never look like a wrong-answer death. If a dropped
  // browser frame misses a pit jump, Tanooki Mario performs an instant air save
  // at platform height instead of falling through the bottom of the scene.
  if (!autoJump && !hasFloorUnderPlayer() && player.y > GROUND_Y - player.h - 6) {
    const landing = nextGroundAfterPlayer();
    if (landing) placePlayerSafely(landing.x + 54);
    player.vx = speed; player.vy = 0;
    player.form = "tanooki";
    spawnParticles(player.x, player.y + player.h, palette.gold, 24);
    beep(988, .06, "square", .04); beep(1319, .09, "square", .035, .06);
  }

  coins.forEach(c => {
    c.phase += .06;
    if (!c.taken && Math.hypot(player.x + 18 - c.x, player.y + 24 - c.y) < 32) {
      c.taken = true; state.coins += 1; spawnParticles(c.x, c.y, palette.gold, 7); beep(900, .05);
    }
  });
  enemies.forEach(e => {
    if (!e.alive) return; e.y = 418 + Math.sin(performance.now() / 350 + e.phase) * 2;
    if (rectsTouch(player, e)) {
      // TAS movement is frame-perfect: every Goomba contact becomes a stomp.
      e.alive = false; player.vy = -8; state.coins += 2;
      spawnParticles(e.x, e.y, e.kind === "koopa" ? "#73d34f" : "#ff9b45", 22); beep(250, .07);
    }
  });

  // The final TAS set piece: after all concepts are cleared, Mario performs
  // a scripted, frame-perfect leap over Bowser and knocks him into the lava.
  if (!boss.defeated && state.cleared === 20 && player.x > boss.x - 180) {
    boss.defeated = true; bossTimer = 80; player.vy = -16; state.coins += 50;
    spawnParticles(boss.x + 45, boss.y + 30, palette.orange, 60);
    spawnParticles(boss.x + 45, boss.y + 30, palette.gold, 40);
    beep(196, .22, "sawtooth"); setTimeout(() => beep(98, .4, "sawtooth"), 180);
  }
  if (bossTimer > 0) bossTimer--;

  for (const q of questions) {
    if (!q.passed && player.x + player.w >= q.x - 24) { player.x = q.x - player.w - 24; player.vx = 0; openQuestion(q); break; }
  }
  if (player.x > 12320 && state.cleared === 20 && boss.defeated) {
    won = true; paused = true; ui.finalScore.textContent = `COINS ${state.coins} • MISINPUTS ${state.deaths} • QUESTIONS 20/20`;
    ui.win.hidden = false; beep(523, .1); setTimeout(() => beep(659, .1), 120); setTimeout(() => beep(784, .28), 240);
  }
  cameraX += ((player.x - W * .31) - cameraX) * .085; cameraX = Math.max(0, Math.min(COURSE_END - W, cameraX));
  player.frame += speed * .08; updateHud();
}

function drawBackground() {
  const transitionElapsed = transitionTimer > 0 ? 240 - transitionTimer : 240;
  const stage = transitionTimer > 0 && transitionElapsed < 165
    ? transitionFromWorld
    : Math.min(4, Math.floor(state.cleared / 4));
  const themes = [
    ["#071f4a", "#4388c7", "#18384e"], // moonlit hills
    ["#241047", "#8b3e9e", "#321b4d"], // haunted forest
    ["#06394a", "#21a8a4", "#174c43"], // underground crystal
    ["#4a1008", "#d64b18", "#3c1710"], // lava world
    ["#111222", "#4d536a", "#191927"], // Bowser castle
  ];
  const theme = themes[stage];
  const gradient = ctx.createLinearGradient(0, 0, 0, H);
  gradient.addColorStop(0, theme[0]); gradient.addColorStop(.68, theme[1]); gradient.addColorStop(1, theme[2]);
  ctx.fillStyle = gradient; ctx.fillRect(0, 0, W, H);
  const moonX = 795 - cameraX * .018;
  ctx.fillStyle = palette.moon; ctx.beginPath(); ctx.arc(moonX, 86, 57, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = theme[0]; ctx.beginPath(); ctx.arc(moonX + 22, 70, 52, 0, Math.PI * 2); ctx.fill();
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
  // Stage-specific silhouettes make each concept feel like a new world.
  if (stage === 1) for (let i=0;i<9;i++){const x=i*145-(cameraX*.18%145);block(x,205,18,247,"#171126");block(x-34,205,86,18,"#171126");}
  if (stage === 2) for (let i=0;i<11;i++){const x=i*120-(cameraX*.2%120);ctx.fillStyle=i%2?"#69e6db":"#b978ff";ctx.beginPath();ctx.moveTo(x,390);ctx.lineTo(x+18,260-(i%3)*35);ctx.lineTo(x+36,390);ctx.fill();}
  if (stage === 3) {ctx.fillStyle="rgba(255,90,20,.55)";ctx.fillRect(0,425,W,27);for(let i=0;i<12;i++)block(i*94-(cameraX*.25%94),410+Math.sin(i+performance.now()/180)*7,54,20,"#ffb11b");}
  if (stage === 4) for(let i=0;i<8;i++){const x=i*170-(cameraX*.12%170);block(x,250,110,202,"#0c0c14");block(x+16,215,18,35,"#0c0c14");block(x+72,195,18,55,"#0c0c14");}
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
  const transitionElapsed = transitionTimer > 0 ? 240 - transitionTimer : 0;
  const x = Math.round(player.x - cameraX), y = Math.round(player.y), run = Math.floor(player.frame) % 2;
  if (!player.onGround && !player.dead) {
    ctx.save(); ctx.globalAlpha=.38; ctx.fillStyle=palette.gold;
    for(let i=0;i<4;i++){ctx.beginPath();ctx.arc(x-10-i*11,y+28+i*3,7-i,0,Math.PI*2);ctx.fill();}
    ctx.restore();
  }
  ctx.save(); ctx.translate(x, 0); if (player.dead) ctx.rotate((150 - deathTimer) * .08);
  block(6, y, 23, 6, palette.red); block(11, y - 5, 15, 6, palette.red); block(3, y + 6, 29, 6, palette.redDark);
  block(8, y + 7, 21, 15, palette.skin); block(24, y + 10, 9, 7, palette.skin); block(18, y + 8, 4, 5, palette.black);
  block(8, y + 17, 18, 5, palette.brown); block(4, y + 22, 28, 5, palette.red);
  block(8, y + 25, 21, 14, palette.blue); block(11, y + 23, 5, 12, palette.blueLight); block(23, y + 23, 5, 12, palette.blueLight);
  if (player.form === "fire") {
    block(8, y + 25, 21, 14, palette.white); block(11, y + 23, 5, 12, palette.orange); block(23, y + 23, 5, 12, palette.orange);
  }
  block(2, y + 25 + run * 2, 8, 12, palette.skin); block(29, y + 25 + (1-run)*2, 7, 12, palette.skin);
  block(7, y + 39 - run*2, 11, 8, palette.brown); block(22, y + 39 - (1-run)*2, 12, 8, palette.brown);
  if (player.form === "tanooki" && !player.dead) {
    // Ears, mask, and a wagging striped tail turn Mario into a flying Tanooki.
    block(8, y - 11, 8, 9, "#8b572a"); block(23, y - 11, 8, 9, "#8b572a");
    block(7, y + 9, 24, 5, "#6d3a21"); block(18, y + 9, 4, 4, palette.white);
    const wag = Math.sin(player.frame * .7) * 8;
    block(31, y + 27, 15, 8, "#b97836"); block(42, y + 20 + wag, 12, 8, "#6d3a21");
    block(50, y + 14 + wag, 12, 7, "#b97836");
    if (transitionElapsed >= 145) {
      block(-3, y + 20, 11, 7, "#b97836"); block(29, y + 18, 13, 7, "#b97836");
    }
  }
  ctx.restore();
}

function drawFireballs() {
  for (const ball of fireballs) {
    const x = ball.x - cameraX, y = ball.y;
    ctx.save(); ctx.translate(x, y); ctx.rotate(ball.spin);
    ctx.fillStyle = palette.gold; ctx.beginPath(); ctx.arc(0, 0, 10, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = palette.orange; ctx.beginPath(); ctx.arc(2, -2, 6, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = palette.white; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(0, 0, 12, .4, 2.2); ctx.stroke();
    ctx.restore();
  }
}

function drawWorldTransition() {
  if (transitionTimer <= 0) return;
  const elapsed = 240 - transitionTimer;
  const nextWorld = subjects[Math.min(4, transitionFromWorld + 1)];
  const marioX = Math.round(player.x - cameraX) + 18;
  const marioY = Math.round(player.y) + 20;
  ctx.save();
  ctx.textAlign = "center";
  if (elapsed < 55) {
    // The block and flower move with Mario instead of replacing the world.
    const itemX = marioX + 95 - elapsed * 1.2;
    const flowerY = marioY - 105 + Math.sin(elapsed * .18) * 8;
    ctx.fillStyle = palette.orange; ctx.fillRect(itemX-25, marioY-42, 50, 44);
    ctx.fillStyle = palette.gold; ctx.font = "bold 32px monospace"; ctx.fillText("?", itemX, marioY-10);
    ctx.font = "47px sans-serif"; ctx.fillText("🌼", itemX, flowerY);
    ctx.fillStyle = palette.white; ctx.font = "bold 22px monospace"; ctx.fillText("FIRE FLOWER!", marioX+25, marioY-145);
  } else if (elapsed < 125) {
    const pulse = 34 + Math.sin(elapsed * .4) * 10;
    ctx.strokeStyle = palette.orange; ctx.lineWidth = 7; ctx.beginPath(); ctx.arc(marioX, marioY, pulse, 0, Math.PI*2); ctx.stroke();
    for (let fireball = 0; fireball < 4; fireball++) {
      const angle = elapsed * .13 + fireball * Math.PI / 2;
      ctx.font = "27px sans-serif"; ctx.fillText("🔥", marioX + Math.cos(angle)*58, marioY + Math.sin(angle)*42);
    }
    ctx.fillStyle = palette.white; ctx.font = "bold 21px monospace"; ctx.fillText("FIRE MARIO", marioX, marioY-82);
  } else if (elapsed < 145) {
    const leafX = marioX + 70 - (elapsed-125) * 1.8;
    const leafY = marioY - 70 + Math.sin(elapsed*.25)*28;
    ctx.save(); ctx.translate(leafX, leafY); ctx.rotate(elapsed*.18); ctx.font = "45px sans-serif"; ctx.fillText("🍂", 0, 0); ctx.restore();
    ctx.fillStyle = palette.white; ctx.font = "bold 21px monospace"; ctx.fillText("TANOOKI SUIT!", marioX, marioY-110);
  } else {
    const flight = Math.min(1, (elapsed - 145) / 55);
    // Speed lines and clouds pass over the still-scrolling world.
    ctx.strokeStyle = "rgba(255,255,255,.75)"; ctx.lineWidth = 5;
    for (let streak = 0; streak < 9; streak++) {
      const sx = (streak * 133 - elapsed * 12) % (W + 180);
      const sy = 75 + (streak * 61) % 360;
      ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx+120, sy); ctx.stroke();
    }
    ctx.fillStyle = palette.gold; ctx.font = "bold 22px monospace";
    ctx.fillText(flight < .75 ? "TAIL SPIN!" : "TANOOKI FLIGHT!", marioX, 145);
    ctx.fillStyle = nextWorld.color; ctx.strokeStyle = palette.black; ctx.lineWidth = 6;
    ctx.font = "bold 34px monospace"; ctx.strokeText(`WORLD ${nextWorld.world}`, W/2, 72); ctx.fillText(`WORLD ${nextWorld.world}`, W/2, 72);
    ctx.fillStyle = palette.white; ctx.font = "bold 18px monospace"; ctx.fillText(nextWorld.name, W/2, 102);
  }
  ctx.restore();
}

function drawDeathGag() {
  if (!player.dead) return;
  const elapsed = 150 - deathTimer;
  const progress = Math.min(1, elapsed / 115);
  const centerX = W / 2;
  const captions = {
    timeout: ["TIME RAN OUT!", "MARIO WAS STILL READING THE VARIABLE NAME"],
    bonk: ["BONK!", "THE GOOMBA HAS SUBMITTED A BUG REPORT"],
    bug: ["MARIO.EXE STOPPED WORKING", "CAUSE: CONFIDENTLY WRONG INPUT"],
    yeet: ["WRONG ANSWER DETECTED", "MARIO HAS LEFT THE CODEBASE"],
  };
  const [headline, subhead] = captions[deathStyle];
  ctx.save();
  // Comic-book impact flash and screen shake.
  const shake = elapsed < 22 ? Math.sin(elapsed * 2.7) * (22 - elapsed) : 0;
  ctx.translate(shake, 0);
  ctx.fillStyle = `rgba(35,0,45,${Math.min(.72, progress)})`;
  ctx.fillRect(0, 0, W, H);
  if (elapsed < 42) {
    ctx.fillStyle = deathStyle === "timeout" ? "#ffd43b" : "#ffef5a";
    ctx.beginPath();
    for (let point = 0; point < 20; point++) {
      const angle = point * Math.PI / 10;
      const radius = point % 2 ? 82 : 165;
      const px = centerX + Math.cos(angle) * radius;
      const py = 255 + Math.sin(angle) * radius;
      if (point === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.closePath(); ctx.fill();
  }
  // Mario's ghost floats away while his hat gives up and falls separately.
  const ghostY = 390 - progress * 245;
  ctx.globalAlpha = Math.min(1, progress * 2);
  ctx.font = "70px sans-serif"; ctx.textAlign = "center";
  ctx.fillText("👻", centerX + 110, ghostY);
  ctx.save(); ctx.translate(centerX - 105, 230 + progress * 170); ctx.rotate(progress * 5.5);
  ctx.font = "52px sans-serif"; ctx.fillText("🧢", 0, 0); ctx.restore();
  if (deathStyle === "timeout") {
    ctx.font = "82px sans-serif"; ctx.fillText("⏰", centerX - 150, 265 + Math.sin(elapsed) * 8);
  } else {
    ctx.font = "68px sans-serif"; ctx.fillText(deathStyle === "yeet" ? "🚀" : "🍄", centerX - 165, 290);
  }
  // Tombstone arrives late for the punchline.
  if (elapsed > 55) {
    const stoneY = Math.min(430, 560 - (elapsed - 55) * 5);
    ctx.fillStyle = "#777083"; ctx.fillRect(centerX - 72, stoneY, 144, 90);
    ctx.fillStyle = "#aaa4b2"; ctx.fillRect(centerX - 61, stoneY + 9, 122, 7);
    ctx.fillStyle = "#17121d"; ctx.font = "bold 18px monospace";
    ctx.fillText("RIP MARIO", centerX, stoneY + 38); ctx.font = "14px monospace";
    ctx.fillText(deathStyle === "timeout" ? "WAITED TOO LONG" : "INPUT MISMATCH", centerX, stoneY + 64);
  }
  ctx.globalAlpha = 1;
  ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#130b18"; ctx.lineWidth = 8;
  ctx.font = "bold 42px monospace"; ctx.strokeText(headline, centerX, 84); ctx.fillText(headline, centerX, 84);
  ctx.fillStyle = "#ffd43b"; ctx.font = "bold 19px monospace";
  ctx.fillText(subhead, centerX, 120);
  ctx.fillStyle = "#ffffff"; ctx.font = "bold 17px monospace";
  ctx.fillText("TAS REWINDING... PRETEND THAT NEVER HAPPENED", centerX, 505);
  ctx.restore();
}

function drawGoomba(e) {
  if (!e.alive) return; const x = e.x - cameraX; if (x < -50 || x > W + 50) return;
  if (e.kind === "koopa") {
    block(x+7,e.y-5,21,28,"#54b948"); block(x+2,e.y+7,30,20,"#2d7d35"); block(x+11,e.y-10,16,14,"#f2c16c");
    block(x+20,e.y-7,4,4,palette.black); block(x+2,e.y+27,13,7,palette.orange); block(x+20,e.y+27,13,7,palette.orange); return;
  }
  if (e.kind === "spiny") {
    block(x+3,e.y+8,29,20,"#e74b3c");
    ctx.fillStyle=palette.white;for(let i=0;i<3;i++){ctx.beginPath();ctx.moveTo(x+5+i*10,e.y+9);ctx.lineTo(x+10+i*10,e.y-7);ctx.lineTo(x+15+i*10,e.y+9);ctx.fill();}
    block(x+5,e.y+27,10,7,palette.black);block(x+21,e.y+27,10,7,palette.black);return;
  }
  block(x + 5, e.y, 24, 7, "#7e3d24"); block(x, e.y + 7, 34, 19, "#a65b37");
  block(x + 6, e.y + 12, 7, 7, palette.white); block(x + 21, e.y + 12, 7, 7, palette.white);
  block(x + 9, e.y + 13, 4, 5, palette.black); block(x + 21, e.y + 13, 4, 5, palette.black);
  block(x + 3, e.y + 26, 13, 7, palette.black); block(x + 20, e.y + 26, 13, 7, palette.black);
}

function drawBowser() {
  if (boss.defeated && bossTimer <= 0) return;
  const x=boss.x-cameraX, fall=boss.defeated?(80-bossTimer)*5:0, y=boss.y+fall;
  if(x<-150||x>W+150)return;
  ctx.save(); if(boss.defeated)ctx.rotate((80-bossTimer)*.05);
  block(x+18,y+14,64,66,"#4e9b42"); block(x+9,y+28,35,48,"#e8b447");
  block(x+44,y,48,36,"#79bd48"); block(x+76,y+9,20,22,"#e8b447");
  block(x+73,y+10,6,7,palette.white);block(x+76,y+12,4,5,palette.redDark);
  block(x+6,y+18,16,13,palette.white);block(x+4,y+43,18,13,palette.white);block(x+24,y+4,13,18,palette.white);
  block(x+16,y+76,27,17,"#29202d");block(x+60,y+76,28,17,"#29202d");
  ctx.restore();
  if(!boss.defeated){ctx.fillStyle=palette.red;ctx.font="bold 16px monospace";ctx.fillText("FINAL BOSS",x+4,y-18);}
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
  questions.forEach(drawGate); enemies.forEach(drawGoomba); drawBowser(); drawParticles(); drawFireballs(); drawMario(); drawDeathGag(); drawWorldTransition();
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
ui.start.addEventListener("click",()=>{if(!started)resetGame();});
ui.sound.addEventListener("click",()=>{audioOn=!audioOn;ui.sound.textContent=`MUSIC + SFX: ${audioOn?"ON":"OFF"}`;if(audioOn)startMusic();});
updateHud();requestAnimationFrame(loop);
