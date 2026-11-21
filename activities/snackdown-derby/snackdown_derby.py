"""Launch a 3.5-minute, four-team snack race. Python standard library only."""

import argparse
from pathlib import Path
import tempfile
import webbrowser

HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Snackdown Derby</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#071226;color:#fff;font-family:Arial,sans-serif;overflow:hidden}
button{cursor:pointer;font:700 15px Arial;border:1px solid #ffffff44;border-radius:9px;padding:12px 19px;background:#142746;color:white}
button:hover{background:#284260}button:focus-visible{outline:3px solid #ffe071;outline-offset:3px}
.primary{background:#ffe071;color:#18233a;border:0;font-size:21px;padding:17px 34px}.primary:hover{background:#ffeaa3}
#stage{height:100vh;display:flex;align-items:center;justify-content:center}canvas{width:min(100vw,177.777vh);height:min(100vh,56.25vw);display:block}
#controls{position:fixed;bottom:13px;right:18px;display:flex;gap:7px;z-index:4}#controls button{padding:9px 12px;background:#0a193ad9;font-size:13px}
.overlay{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#061022bf;z-index:3;padding:20px}
.intro{max-width:1020px;width:100%;padding:40px 45px;border:1px solid #ffffff25;border-radius:22px;background:linear-gradient(135deg,#122747,#09152c);box-shadow:0 25px 100px #0008;text-align:center}
.kicker{letter-spacing:5px;color:#70e6d2;font-size:14px;font-weight:bold}.intro h1{font-size:clamp(40px,6vw,78px);letter-spacing:-3px;line-height:.95;margin:20px 0;color:#ffe071}
.subtitle{font-size:19px;color:#c0cde3;line-height:1.5}.teams{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:27px 0}.team{padding:18px 8px;border-top:5px solid var(--color);background:#ffffff08;border-radius:4px 4px 12px 12px}.team strong{display:block;font-size:23px;color:var(--color)}.team span{display:block;font-size:13px;color:#d4dceb;margin-top:8px}.actions{display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap}.hint{font-size:13px;color:#9cadc8;margin-top:18px}
[hidden]{display:none!important}#tickets{display:none}#pauseLabel{position:fixed;top:45%;left:0;right:0;text-align:center;pointer-events:none;font-size:72px;font-weight:900;color:#ffe071;text-shadow:0 4px 20px #000;z-index:5}
@media(max-width:650px){.intro{padding:24px 18px}.team strong{font-size:17px}.team span{font-size:11px}.teams{gap:5px}.kicker{letter-spacing:2px}.subtitle{font-size:15px}}
@media print{@page{size:letter;margin:.4in}body{background:white;overflow:visible;color:black}#stage,.overlay,#controls,#pauseLabel{display:none!important}#tickets{display:grid!important;grid-template-columns:repeat(3,1fr);gap:.12in}.ticket{border:2px dashed #111;border-top:7px solid #111;height:1.53in;padding:.12in;break-inside:avoid;text-align:center}.ticket small{font-size:9pt}.ticket b{display:block;font-size:20pt;margin:8px 0}.ticket em{font-size:10pt;font-style:normal}.ticket .number{font-size:10pt;margin-top:7px}}
</style></head><body>
<main id="stage"><canvas id="game" width="1600" height="900" aria-label="Animated four-team snack race with cartoon battles"></canvas></main>
<section class="overlay" id="lobby"><div class="intro">
<div class="kicker">TONIGHT'S EXTREMELY UNNECESSARY MAIN EVENT</div><h1>SNACKDOWN<br>DERBY</h1>
<p class="subtitle">Four teams. Eighteen tickets. Zero athletic qualifications.<br>A __DURATION_LABEL__ race with deeply unserious snack battles.</p>
<div class="teams"><div class="team" style="--color:#ffd35c"><strong>CHEESY</strong><span>The Big Cheddar</span></div><div class="team" style="--color:#ff7394"><strong>JUICY</strong><span>Lord of the Squeeze</span></div><div class="team" style="--color:#6ed9ff"><strong>CRISPY</strong><span>Crunch Time Criminal</span></div><div class="team" style="--color:#b7f774"><strong>SPICY</strong><span>The Mild Inconvenience</span></div></div>
<div class="actions"><button class="primary" id="start">LET THE NONSENSE BEGIN</button><button id="print">Print 18 tickets</button><button id="shuffle">Shuffle ticket teams</button></div>
<p class="hint">Hand out tickets as students enter. Cheer for your ticket's team.<br>Space: pause &nbsp; F: fullscreen &nbsp; M: music &nbsp; One winner, equal odds, new draw every show.</p>
<p class="hint" id="ticketSummary"></p>
</div></section>
<div id="pauseLabel" hidden>OFFICIAL SNACK BREAK</div>
<nav id="controls" aria-label="Show controls"><button id="pause" disabled>Pause</button><button id="mute">Music: ON</button><button id="full">Fullscreen</button><button id="again" hidden>New race</button></nav>
<section id="tickets" aria-label="Printable team tickets"></section>
<script>
'use strict';
const DURATION=__DURATION__, INTRO=8, FINISH=DURATION-10;
const teams=[{name:'CHEESY',nick:'The Big Cheddar',color:'#ffd35c',dark:'#c27420',move:'LACTOSE INTOLERANCE',quip:'Built different. Mostly dairy.'},{name:'JUICY',nick:'Lord of the Squeeze',color:'#ff7394',dark:'#a82d62',move:'PULP FICTION',quip:'100% juice. 0% technique.'},{name:'CRISPY',nick:'Crunch Time Criminal',color:'#6ed9ff',dark:'#267aad',move:'AIR FRYER UPPERCUT',quip:'No thoughts. Just crunch.'},{name:'SPICY',nick:'The Mild Inconvenience',color:'#b7f774',dark:'#558b36',move:'EMOTIONAL HOT SAUCE',quip:'Banned from the group chat.'}];
const battleWindows=[[.22,.29],[.48,.55],[.74,.81]].map(([a,b])=>({start:INTRO+(FINISH-INTRO)*a,end:INTRO+(FINISH-INTRO)*b}));
const battleLength=battleWindows.reduce((sum,b)=>sum+b.end-b.start,0),raceLength=FINISH-INTRO-battleLength;
const canvas=document.querySelector('#game'),c=canvas.getContext('2d');
const $=id=>document.getElementById(id);
let seed=1,rng,champion=0,rank=[],battles=[],phases=[],ticketTeams=[],running=false,paused=false,startTime=0,pauseTime=0,elapsed=0,finished=false,lastSound=-1,music=true,audio=null,beat=0,nextBeat=0;
function randomInt(n){const a=new Uint32Array(1);crypto.getRandomValues(a);const limit=Math.floor(4294967296/n)*n;if(a[0]>=limit)return randomInt(n);return a[0]%n}
function seeded(s){return()=>{s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function mix(a,random=()=>randomInt(1000000)/1000000){a=a.slice();for(let i=a.length-1;i>0;i--){let j=Math.floor(random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function newShow(){seed=randomInt(4294967296);rng=seeded(seed);champion=randomInt(4);rank=[champion,...mix([0,1,2,3].filter(i=>i!==champion),rng)];phases=teams.map(()=>rng());const pairs=[[0,1],[2,3],mix([0,1,2,3],rng).slice(0,2)];battles=battleWindows.map((b,i)=>({...b,pair:pairs[i],winner:pairs[i][Math.floor(rng()*2)],round:i+1}));elapsed=0;running=false;paused=false;finished=false;lastSound=-1;beat=0;nextBeat=0;$('pause').disabled=true;$('pause').textContent='Pause';$('pauseLabel').hidden=true;$('again').hidden=true;draw(0)}
function assignTickets(){ticketTeams=mix(Array.from({length:18},(_,i)=>i%4));$('tickets').innerHTML=ticketTeams.map((t,i)=>`<article class="ticket"><small>SNACKDOWN DERBY • ADMIT ONE</small><b>${teams[t].name}</b><em>${teams[t].nick}</em><div class="number">TICKET ${String(i+1).padStart(2,'0')} • CHEER LOUDLY</div></article>`).join('');$('ticketSummary').textContent=teams.map((t,i)=>`${t.name}: ${ticketTeams.filter(x=>x===i).length} tickets`).join('   /   ')}
function smooth(a,b,x){let u=Math.max(0,Math.min(1,(x-a)/(b-a)));return u*u*(3-2*u)}
function progress(t){let stopped=0;for(const b of battles)stopped+=Math.max(0,Math.min(t,b.end)-b.start);const u=Math.max(0,Math.min(1,(t-INTRO-stopped)/raceLength));return teams.map((team,i)=>4*u+.09*Math.sin(2*Math.PI*(2*u+phases[i]))*Math.sin(Math.PI*u)-.07*rank.indexOf(i)*smooth(.82,1,u))}
function stageAt(t){if(t<INTRO)return'intro';if(t>=FINISH)return'victory';return battles.some(b=>t>=b.start&&t<b.end)?'battle':'race'}
function label(text,x,y,size=24,color='#fff',align='center',weight=800){c.fillStyle=color;c.font=`${weight} ${size}px Arial`;c.textAlign=align;c.textBaseline='middle';c.fillText(text,x,y)}
function roundRect(x,y,w,h,r,fill){c.beginPath();c.roundRect(x,y,w,h,r);c.fillStyle=fill;c.fill()}
function ellipse(x,y,rx,ry,fill){c.beginPath();c.ellipse(x,y,rx,ry,0,0,Math.PI*2);c.fillStyle=fill;c.fill()}
function star(x,y,r,fill){c.save();c.translate(x,y);c.beginPath();for(let i=0;i<10;i++){const a=i*Math.PI/5-Math.PI/2,rr=i%2?r*.43:r;i?c.lineTo(Math.cos(a)*rr,Math.sin(a)*rr):c.moveTo(Math.cos(a)*rr,Math.sin(a)*rr)}c.closePath();c.fillStyle=fill;c.fill();c.restore()}
function mascot(id,x,y,scale=1,pose=0,flip=false,attack=false){
 const team=teams[id];c.save();c.translate(x,y);if(flip)c.scale(-1,1);c.scale(scale,scale);c.rotate(Math.sin(pose)*.055);
 ellipse(0,48,45,9,'#0005');
 c.lineWidth=12;c.strokeStyle=team.dark;c.lineCap='round';
 const stride=Math.sin(pose)*17;
 for(const side of[-1,1]){c.beginPath();c.moveTo(side*17,22);c.lineTo(side*21+stride*side,47);c.stroke();roundRect(side*22-12+stride*side,43,28,13,5,'#f2f5ff')}
 for(const side of[-1,1]){c.beginPath();c.moveTo(side*27,-8);c.lineTo(side*48+(attack&&side===1?30:0),-5+(attack&&side===1?-24:Math.sin(pose+side)*17));c.stroke();ellipse(side*48+(attack&&side===1?30:0),-5+(attack&&side===1?-24:Math.sin(pose+side)*17),13,12,'#fff')}
 if(id===0){c.beginPath();c.moveTo(-36,29);c.lineTo(-29,-40);c.lineTo(39,22);c.closePath();c.fillStyle=team.color;c.fill();for(const [xx,yy,rr] of[[-15,-8,7],[-18,17,5],[13,16,6]])ellipse(xx,yy,rr,rr,'#e7a62c')}
 if(id===1){roundRect(-29,-37,58,69,12,team.color);c.fillStyle='#ffe3e9';c.fillRect(-23,-28,46,13);c.strokeStyle='#78e2ed';c.lineWidth=8;c.beginPath();c.moveTo(10,-35);c.lineTo(18,-64);c.lineTo(34,-69);c.stroke();label('JUICE',0,15,11,'#84304a')}
 if(id===2){roundRect(-31,-21,62,54,10,team.color);for(let i=0;i<5;i++){c.save();c.translate(-23+i*11,-24);c.rotate((i-2)*.13);roundRect(-4,-30,9,46,3,'#ffe08a');c.restore()}c.strokeStyle='#287ca8';c.lineWidth=2;for(let yy=-10;yy<25;yy+=10){c.beginPath();c.moveTo(-25,yy);c.lineTo(25,yy);c.stroke()}}
 if(id===3){c.fillStyle=team.color;c.beginPath();c.moveTo(-23,-30);c.bezierCurveTo(38,-48,41,24,-15,39);c.bezierCurveTo(-6,18,-38,5,-23,-30);c.fill();c.strokeStyle='#418e45';c.lineWidth=8;c.beginPath();c.moveTo(0,-30);c.quadraticCurveTo(4,-58,23,-52);c.stroke()}
 c.fillStyle='#17233b';for(const side of[-1,1])ellipse(side*11,-7,5,7,'#17233b');c.strokeStyle='#17233b';c.lineWidth=3;c.beginPath();c.arc(2,4,10,.1,Math.PI-.1);c.stroke();
 if(attack){c.strokeStyle='#17233b';c.lineWidth=4;c.beginPath();c.moveTo(-18,-21);c.lineTo(-5,-16);c.moveTo(5,-16);c.lineTo(18,-21);c.stroke()}
 c.restore();
}
function stadium(t){
 const sky=c.createLinearGradient(0,0,0,900);sky.addColorStop(0,'#0b2042');sky.addColorStop(1,'#17294c');c.fillStyle=sky;c.fillRect(0,0,1600,900);
 for(let row=0;row<4;row++)for(let j=0;j<57;j++){const x=18+j*28,y=157+row*18;ellipse(x,y,5,5,['#e7a962','#48a8c7','#bc7fb5','#89b66e'][(row*7+j)%4]);if((j+row)%7===0){c.fillStyle='#fff3';c.fillRect(x-1,y-12+Math.sin(t*5+j)*3,2,10)}}
 label('SNACKDOWN DERBY',55,48,40,'#ffe071','left');label('THE LEAGUE NOBODY ASKED FOR',56,90,16,'#9cb6d7','left',700);
 const remaining=Math.ceil(Math.max(0,DURATION-t)),time=`${Math.floor(remaining/60)}:${String(remaining%60).padStart(2,'0')}`;
 label(time,1535,51,43,'#fff','right');label(paused?'PAUSED':t>=FINISH?'FINAL RESULT':'LIVE • SNACK SPORTS NETWORK',1535,94,15,'#7ee9d6','right');
}
function race(t,dim=false){
 const p=progress(t),order=[0,1,2,3].sort((a,b)=>p[b]-p[a]);
 ellipse(800,500,699,287,'#213f55');ellipse(800,500,670,260,'#bf6d4c');
 for(let lane=0;lane<5;lane++){c.beginPath();c.ellipse(800,500,650-lane*24,241-lane*22,0,0,2*Math.PI);c.strokeStyle='#ffddb780';c.lineWidth=2;c.stroke()}
 ellipse(800,500,550,151,'#27785c');ellipse(800,500,510,119,'#236b53');
 for(let k=0;k<4;k++){c.save();c.translate(800,500);c.rotate(k*Math.PI/2);c.fillStyle='#ffffff0b';c.fillRect(-1,-96,2,192);c.restore()}
 label('NO SKILLS REQUIRED',800,465,30,'#b3e5c8');label('JUST UNREASONABLE CONFIDENCE',800,507,17,'#8fcbad');
 const banner=t<INTRO?'WELCOME TO THE SNACK SHOW':t>FINISH-22?'FINAL STRETCH! PANIC RESPONSIBLY!':`LAP ${Math.min(4,Math.floor(Math.max(...p))+1)} OF 4`;
 label(banner,800,132,27,'#ffe071');
 // Finish line stays at the top of the oval, across all four lanes.
 for(let xx=0;xx<5;xx++)for(let yy=0;yy<8;yy++){c.fillStyle=(xx+yy)%2?'#15253b':'#fff';c.fillRect(786+xx*7,259+yy*11,7,11)}
 label('FINISH',804,240,15,'#fff');
 const racers=teams.map((team,id)=>{let a=-Math.PI/2+2*Math.PI*p[id];return{id,x:800+(638-id*24)*Math.cos(a),y:500+(230-id*22)*Math.sin(a)}}).sort((a,b)=>a.y-b.y);
 for(const r of racers){const bounce=t>FINISH?Math.sin(t*8+r.id)*5:Math.abs(Math.sin(t*11+r.id))*6;mascot(r.id,r.x,r.y-bounce,0.66,t*14+r.id);label(teams[r.id].name,r.x,r.y-65,17,teams[r.id].color)}
 order.forEach((id,pos)=>{const x=66+pos*384;roundRect(x,805,360,63,12,'#06152abf');label(`${pos+1}  ${teams[id].name}`,x+20,828,22,teams[id].color,'left');label(pos===0?'ABSOLUTELY LOCKED IN':['','ALLEGEDLY AN ATHLETE','NEEDS A SNACK BREAK','JUST HERE FOR THE TICKET'][pos],x+20,852,10,'#c7d5e7','left')});
 if(dim){c.fillStyle='#020713bb';c.fillRect(0,122,1600,660)}
}
const announcements=['CHEESY REQUESTS A DAIRY TIMEOUT','JUICY HAS FILED A FORMAL COMPLAINT','CRISPY IS RUNNING ON VIBES','SPICY HAS NO INSIDE VOICE','THE REFEREE IS A MICROWAVE','THIS EVENT HAS NO NUTRITIONAL VALUE','SOMEONE LEFT THEIR AURA IN THE PARKING LOT','THE CROWD HAS LOST THE PLOT'];
function battle(t,b){
 const u=(t-b.start)/(b.end-b.start),local=(t-b.start),left=b.pair[0],right=b.pair[1],win=b.winner,lose=b.pair.find(i=>i!==win),impact=u>.73;
 race(t,true);
 c.save();const shake=impact&&u<.84?Math.sin(local*90)*9:0;c.translate(shake,0);
 roundRect(155,180,1290,555,24,'#11152bf2');
 const gradient=c.createLinearGradient(0,220,0,720);gradient.addColorStop(0,'#5a2462');gradient.addColorStop(1,'#172c4b');c.fillStyle=gradient;c.fillRect(175,310,1250,405);
 c.strokeStyle='#af82c844';c.lineWidth=2;for(let k=0;k<14;k++){c.beginPath();c.moveTo(175+k*100,715);c.lineTo(800+(k-6)*50,475);c.stroke()}for(let k=0;k<6;k++){c.beginPath();c.moveTo(175,490+k*k*8);c.lineTo(1425,490+k*k*8);c.stroke()}
 label(`SNACK KOMBAT • ROUND ${b.round}`,800,215,38,'#ffe071');
 for(const [id,x] of[[left,210],[right,940]]){label(teams[id].name,x,270,26,teams[id].color,'left');roundRect(x,292,450,18,5,'#ffffff22');const health=id===win?1-.25*smooth(.2,.7,u):1-smooth(.18,.83,u);roundRect(x,292,450*health,18,5,teams[id].color)}
 const attacks=u>.14&&u<.73,cycle=Math.floor(u*10)%2,kick=Math.sin(local*12),lunge=attacks?Math.max(0,kick)*85:0;
 function fighter(id,base,flip){const losing=id===lose&&impact;let xx=base+(id===left?1:-1)*lunge,yy=560;let rotation=0;if(losing){const fly=smooth(.76,.96,u);xx+=(id===left?-1:1)*fly*480;yy-=Math.sin(fly*Math.PI)*230;rotation=fly*8}c.save();c.translate(xx,yy);c.rotate(rotation);mascot(id,0,0,2.15,local*9,flip,attacks);c.restore()}
 fighter(left,420,false);fighter(right,1180,true);
 if(attacks){const from=cycle?right:left,to=cycle?left:right,f=(u*10)%1;const a=from===left?500:1100,z=to===left?500:1100;const px=a+(z-a)*f,py=475-Math.sin(f*Math.PI)*65;star(px,py,26,teams[from].color);label(['CHEESE!','SQUEEZE!','CRUNCH!','HOT!'][from],px,py-49,24,teams[from].color);if(f>.72){star(z,490,65,'#ffe071');label(['BONK!','ABSOLUTE NONSENSE!','SKILL ISSUE!'][Math.floor(local)%3],800,430,35,'#fff')}}
 if(u<.15){label('FIGHT FOR YOUR LUNCH MONEY!',800,399,43,'#fff');label('NO ACTUAL FIGHTING. THESE ARE GROCERIES.',800,450,18,'#e6c7e8')}
 else if(impact){label('SNACKTALITY!',800,390,66,'#ffe071');label(teams[win].move,800,454,30,teams[win].color);label(`${teams[win].name} WINS • EGO BOOST +9000`,800,655,30,'#fff')}
 else{label(teams[cycle?right:left].move,800,375,33,'#ffe071')}
 c.restore();
}
function confetti(t){for(let i=0;i<120;i++){const x=(i*71+Math.sin(t+i)*40)%1600,y=((t*125+i*53)%1100)-100;c.save();c.translate(x,y);c.rotate(t*2+i);c.fillStyle=teams[i%4].color;c.fillRect(-4,-7,8,14);c.restore()}}
function victory(t){race(FINISH);c.fillStyle='#061024db';c.fillRect(0,120,1600,665);confetti(t);label('YOUR EXTREMELY OFFICIAL CHAMPION',800,205,28,'#aac1df');label(teams[champion].name,800,300,100,teams[champion].color);mascot(champion,800,510+Math.sin(t*6)*13,2.65,t*9);star(800,359,25,'#ffe071');label(teams[champion].quip,800,679,30,'#fff');label('WINNING TICKETS: MAKE AN UNREASONABLE AMOUNT OF NOISE',800,740,21,'#ffe071');label('Prize: bragging rights. Financial value: approximately zero.',800,780,16,'#b0c1dc')}
function draw(t){stadium(t);const stage=stageAt(t);if(stage==='victory')victory(t);else if(stage==='battle')battle(t,battles.find(b=>t>=b.start&&t<b.end));else{race(t);if(stage==='intro'){c.fillStyle='#061024d9';c.fillRect(300,350,1000,255);const count=Math.ceil(INTRO-t);label(count>3?'PRESENTING FOUR ABSOLUTE LEGENDS':String(count),800,430,count>3?35:110,'#ffe071');label(count>3?teams[Math.floor(t)%4].nick:'THEY HAVE NEVER TRAINED FOR THIS',800,550,29,'#fff')}else{const line=announcements[Math.floor((t-INTRO)/8)%announcements.length];label(line,800,755,21,'#dbe9fa')}}}
function tone(freq,time,length=.13,type='square',gain=.045,slide=0){if(!audio||!music)return;const o=audio.createOscillator(),g=audio.createGain();o.type=type;o.frequency.setValueAtTime(freq,time);if(slide)o.frequency.exponentialRampToValueAtTime(slide,time+length);g.gain.setValueAtTime(gain,time);g.gain.exponentialRampToValueAtTime(.001,time+length);o.connect(g).connect(audio.destination);o.start(time);o.stop(time+length+.01)}
function audioPump(){if(!audio||!music||!running||paused||finished)return;const now=audio.currentTime;if(nextBeat<now-.3)nextBeat=now;while(nextBeat<now+.15){const stage=stageAt(elapsed),b=beat++,notes=stage==='battle'?[0,1,7,3,10,1,5,7]:[0,7,3,10,5,12,8,2];tone(110*Math.pow(2,notes[b%8]/12),nextBeat,.1,'sawtooth',.018);if(b%2===0)tone(b%4===0?65:90,nextBeat,.16,'sine',.1,35);if(b%4===3)tone(350+(b%3)*100,nextBeat,.18,'triangle',.027,120);if(b%8===7)tone(800,nextBeat,.3,'sine',.018,180);nextBeat+=.23}}
setInterval(audioPump,90);
function tick(now){if(running&&!paused){elapsed=Math.max(0,Math.min(DURATION,(now-startTime)/1000));if(elapsed>=DURATION){running=false;finished=true;$('again').hidden=false;$('pause').disabled=true}const b=battles.findIndex(b=>elapsed>=b.start&&elapsed<b.end);if(b!==lastSound){if(b>=0&&audio){tone(150,audio.currentTime,.5,'sawtooth',.06,40);tone(650,audio.currentTime+.2,.4,'triangle',.03,160)}lastSound=b}}draw(elapsed);requestAnimationFrame(tick)}
async function start(){if(running||finished)return;try{if(!audio)audio=new(window.AudioContext||window.webkitAudioContext)();audio.resume().catch(error=>console.warn("Audio unavailable:",error))}catch(error){console.warn('Audio unavailable:',error)}$('lobby').hidden=true;running=true;startTime=performance.now();$('pause').disabled=false;nextBeat=audio?audio.currentTime:0}
function pause(){if(!running)return;paused=!paused;if(paused)pauseTime=performance.now();else startTime+=performance.now()-pauseTime;$('pauseLabel').hidden=!paused;$('pause').textContent=paused?'Resume':'Pause'}
async function full(){try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch(error){console.warn('Fullscreen unavailable:',error)}}
function toggleMusic(){music=!music;$('mute').textContent=`Music: ${music?'ON':'OFF'}`;if(music&&audio){audio.resume();nextBeat=audio.currentTime}}
$('start').onclick=start;$('pause').onclick=pause;$('mute').onclick=toggleMusic;$('full').onclick=full;$('print').onclick=()=>window.print();$('shuffle').onclick=assignTickets;$('again').onclick=()=>{newShow();$('lobby').hidden=false};
document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();if(!$('lobby').hidden)start();else pause()}if(e.key.toLowerCase()==='f')full();if(e.key.toLowerCase()==='m')toggleMusic()});
assignTickets();newShow();requestAnimationFrame(tick);
// Test access is absent from the normal classroom view.
if(new URLSearchParams(location.search).has('test'))window.derbyTest={seek(t){elapsed=Math.max(0,Math.min(DURATION,t));startTime=performance.now()-elapsed*1000;draw(elapsed)},snapshot(){return{elapsed,stage:stageAt(elapsed),champion,rank:rank.slice(),progress:progress(elapsed),running,paused,tickets:ticketTeams.slice(),battles:battles.map(b=>({...b})),duration:DURATION}},newShow};
</script></body></html>'''


def build_page(duration: int = 210) -> str:
    """Return a self-contained show with original canvas art and synthesized audio."""
    if not 180 <= duration <= 240:
        raise ValueError("Choose a show length between 180 and 240 seconds.")
    minutes, seconds = divmod(duration, 60)
    label = f"{minutes}-minute" if not seconds else f"{minutes}-minute {seconds}-second"
    return HTML.replace("__DURATION__", str(duration)).replace("__DURATION_LABEL__", label)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=int, default=210, choices=range(180, 241),
                        metavar="180-240", help="Show length in seconds (default: 210).")
    parser.add_argument("--output", type=Path, help="Optional HTML destination.")
    parser.add_argument("--no-browser", action="store_true", help="Save the show without opening it.")
    args = parser.parse_args()
    output = args.output or Path(tempfile.mkdtemp(prefix="snackdown-")) / "snackdown.html"
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_page(args.duration), encoding="utf-8")
    print(f"Snackdown Derby: {output}")
    print("Print the 18 tickets, hand them out, then click LET THE NONSENSE BEGIN.")
    print("Space pauses. F opens fullscreen. M toggles the original music.")
    if not args.no_browser and not webbrowser.open(output.as_uri()):
        print("Open the HTML file above in your browser.")


if __name__ == "__main__":
    main()
