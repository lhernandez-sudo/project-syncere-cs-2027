"""Launch a six-minute, four-team snack race. Python standard library only."""

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
<p class="hint" id="ticketSummary"></p><p class="hint" id="musicStatus" role="status">Soundtrack: built-in pop. You can choose a local audio file.</p>
</div></section>
<div id="pauseLabel" hidden>OFFICIAL SNACK BREAK</div>
<nav id="controls" aria-label="Show controls"><button id="pause" disabled>Pause</button><button id="mute">Music: ON</button><button id="chooseMusic">Choose music file</button><input id="musicFile" type="file" accept="audio/*" hidden><button id="full">Fullscreen</button><button id="again" hidden>New race</button></nav>
<section id="tickets" aria-label="Printable team tickets"></section>
<script>
'use strict';
const DURATION=__DURATION__, INTRO=8, FINISH=DURATION-10;
const teams=[{name:'CHEESY',nick:'The Big Cheddar',color:'#ffd35c',dark:'#c27420',move:'FONDUE OF DOOM',quip:'Built different. Mostly dairy.'},{name:'JUICY',nick:'Lord of the Squeeze',color:'#ff7394',dark:'#a82d62',move:'PULP PRESSURE 9000',quip:'100% juice. 0% technique.'},{name:'CRISPY',nick:'Crunch Time Criminal',color:'#6ed9ff',dark:'#267aad',move:'AIR-FRYER ARTILLERY',quip:'No thoughts. Just crunch.'},{name:'SPICY',nick:'The Mild Inconvenience',color:'#b7f774',dark:'#558b36',move:'HOT SAUCE: FINAL BOSS',quip:'Banned from the group chat.'}];
const battleWindows=[[.12,.17],[.26,.31],[.40,.45],[.54,.59],[.68,.73],[.82,.87]].map(([a,b])=>({start:INTRO+(FINISH-INTRO)*a,end:INTRO+(FINISH-INTRO)*b}));
const battleLength=battleWindows.reduce((sum,b)=>sum+b.end-b.start,0),raceLength=FINISH-INTRO-battleLength;
const canvas=document.querySelector('#game'),c=canvas.getContext('2d');
const $=id=>document.getElementById(id);
let seed=1,rng,champion=0,rank=[],battles=[],sabotages=[],paceTables=[],phases=[],ticketTeams=[],running=false,paused=false,startTime=0,pauseTime=0,elapsed=0,finished=false,lastSound=-1,music=true,audio=null,beat=0,nextBeat=0,audioBus=null,echoBus=null,noiseBuffer=null,lastFxSlot="",customMusic=null,customUrl=null;
function randomInt(n){const a=new Uint32Array(1);crypto.getRandomValues(a);const limit=Math.floor(4294967296/n)*n;if(a[0]>=limit)return randomInt(n);return a[0]%n}
function seeded(s){return()=>{s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function mix(a,random=()=>randomInt(1000000)/1000000){a=a.slice();for(let i=a.length-1;i>0;i--){let j=Math.floor(random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function newShow(){if(customMusic){customMusic.pause();customMusic.currentTime=0}seed=randomInt(4294967296);rng=seeded(seed);champion=randomInt(4);rank=[champion,...mix([0,1,2,3].filter(i=>i!==champion),rng)];phases=teams.map(()=>rng());const pairs=mix([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],rng);battles=battleWindows.map((b,i)=>({...b,pair:pairs[i],winner:pairs[i][Math.floor(rng()*2)],round:i+1}));prepareSabotage();elapsed=0;running=false;paused=false;finished=false;lastSound=-1;beat=0;nextBeat=0;$('pause').disabled=true;$('pause').textContent='Pause';$('pauseLabel').hidden=true;$('again').hidden=true;draw(0)}
function assignTickets(){ticketTeams=mix(Array.from({length:18},(_,i)=>i%4));$('tickets').innerHTML=ticketTeams.map((t,i)=>`<article class="ticket"><small>SNACKDOWN DERBY • ADMIT ONE</small><b>${teams[t].name}</b><em>${teams[t].nick}</em><div class="number">TICKET ${String(i+1).padStart(2,'0')} • CHEER LOUDLY</div></article>`).join('');$('ticketSummary').textContent=teams.map((t,i)=>`${t.name}: ${ticketTeams.filter(x=>x===i).length} tickets`).join('   /   ')}
function smooth(a,b,x){let u=Math.max(0,Math.min(1,(x-a)/(b-a)));return u*u*(3-2*u)}
function raceClock(t){let stopped=0;for(const b of battles)stopped+=Math.max(0,Math.min(t,b.end)-b.start);return Math.max(0,Math.min(raceLength,t-INTRO-stopped))}
const sabotageNames=['NACHO CHEESE OIL SLICK','HIGH-PRESSURE JUICE FLOOD','DEEP-FRIED CRUMB STORM','HOT-SAUCE ROCKET BOOST'];
const sabotageJokes=['THAT IS NACHO PERSONAL SPACE','NOW WITH 300% OF YOUR DAILY ATTITUDE','CRUNCHY ON THE OUTSIDE. PANICKING INSIDE.','SCOVILLE LEVEL: PARENT CONFERENCE'];
function prepareSabotage(){
 const points=[.055,.205,.345,.485,.625,.765,.915];
 sabotages=points.map((fraction,i)=>{const actor=i%4,victim=(actor+1+Math.floor(rng()*3))%4,start=INTRO+(FINISH-INTRO)*fraction;return{actor,victim,start,end:start+8,clock:raceClock(start),kind:i%4}});
 paceTables=teams.map((_,id)=>{const a=[0];for(let k=0;k<1000;k++){const clock=(k+.5)/1000*raceLength;let speed=1+.17*Math.sin(clock/8+phases[id]*7);for(const e of sabotages){const d=clock-e.clock,weight=smooth(0,1,d)*(1-smooth(5,8,d));if(e.actor===id)speed+=.40*weight;if(e.victim===id)speed-=.67*weight}a.push(a[k]+Math.max(.22,speed))}const total=a[1000];return a.map(value=>value/total)});
}
function progress(t){const u=raceClock(t)/raceLength,n=u*1000,k=Math.min(999,Math.floor(n)),f=n-k;return teams.map((team,id)=>{const table=paceTables[id],v=table[k]+(table[k+1]-table[k])*f;return 4*v+.09*Math.sin(2*Math.PI*(2*v+phases[id]))*Math.sin(Math.PI*v)-.07*rank.indexOf(id)*smooth(.82,1,v)})}

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
function weapon(id,x,y,scale=1,flip=false,phase=0,firing=false){
 c.save();c.translate(x,y);if(flip)c.scale(-1,1);c.scale(scale,scale);c.translate(53,-20);c.rotate(Math.sin(phase)*.08);
 if(id===0){roundRect(-21,-22,61,39,8,'#ba6330');ellipse(9,-21,30,9,'#ffe078');roundRect(-12,13,14,22,3,'#773e25');roundRect(30,-6,37,15,4,'#ffbb42');ellipse(65,1,8,11,'#ffdf71');label('FONDUE',7,0,9,'#fff4bc');for(let i=0;i<3;i++){ellipse(-8+i*15,-27-Math.sin(phase+i)*3,3,5,'#ffd35c')}if(firing)ellipse(75,0,15,8,'#ffe483')}
 if(id===1){roundRect(-16,-27,55,48,8,'#ad3765');roundRect(-11,-22,45,28,5,'#ffb5c5');c.fillStyle='#f96c9c';c.fillRect(-8,-7-Math.sin(phase)*3,39,11);roundRect(33,-5,37,12,4,'#77d8e5');c.strokeStyle='#74d4d9';c.lineWidth=5;c.beginPath();c.moveTo(-4,-27);c.lineTo(6,-43);c.lineTo(29,-43);c.stroke();roundRect(-5,17,14,20,4,'#6c2849');label('PULP',11,-9,9,'#9b2851');if(firing)ellipse(76,0,10,7,'#ff9fba')}
 if(id===2){roundRect(-23,-29,73,54,11,'#253c53');roundRect(-18,-23,63,18,5,'#5ab5d7');roundRect(-13,-2,55,22,5,'#f1aa43');roundRect(9,3,23,6,2,'#24384d');roundRect(42,-7,29,19,4,'#304d65');label('AIR FRY',13,-14,8,'#e9f8ff');for(let i=0;i<3;i++){roundRect(57+i*6,-10-i*5,5,23,2,'#ffe18b')}if(firing){for(let i=0;i<3;i++){c.strokeStyle='#fff2c9';c.lineWidth=2;c.beginPath();c.moveTo(-12+i*17,-35);c.quadraticCurveTo(-20+i*17,-45,-8+i*17,-52);c.stroke()}}}
 if(id===3){roundRect(-14,-22,43,48,9,'#d33030');roundRect(-5,-34,24,13,4,'#f6b343');roundRect(20,-5,48,15,4,'#aa1b24');roundRect(-2,23,13,16,4,'#6b2530');label('HOT',7,1,11,'#fff4c8');c.strokeStyle='#ffbb60';c.lineWidth=3;c.beginPath();c.moveTo(-10,17);c.lineTo(-30,24);c.lineTo(-38,14);c.stroke();if(firing){ellipse(79,1,20,10,'#ff6533');ellipse(75,1,12,6,'#ffe27a')}}
 c.restore();
}
function foodAttack(id,x1,x2,y,t,power=1){
 c.save();const dx=x2-x1;
 if(id===0||id===1){c.lineCap='round';c.lineWidth=(id===0?16:11)*power;c.strokeStyle=id===0?'#ffc73f':'#ff83a8';c.beginPath();c.moveTo(x1,y);c.bezierCurveTo(x1+dx*.35,y-24*power,x1+dx*.65,y+15*power,x2,y+Math.sin(t*11)*12);c.stroke();c.lineWidth=4*power;c.strokeStyle=id===0?'#ffe895':'#ffd2e1';c.stroke();for(let i=0;i<12;i++){let u=(t*1.7+i/12)%1;ellipse(x1+dx*u,y+Math.sin(u*12+t)*12+u*u*22,5*power,3*power,id===0?'#ffd259':'#ffb0cc')}}
 if(id===2){for(let i=0;i<13;i++){const u=(t*1.5+i/13)%1;c.save();c.translate(x1+dx*u,y-Math.sin(u*Math.PI)*80+(i%3-1)*22);c.rotate(t*9+i);roundRect(-15*power,-3*power,30*power,7*power,2,'#ffe08a');c.fillStyle='#b77c2d';c.fillRect(-10*power,-2*power,5*power,2*power);c.restore()}}
 if(id===3){for(let i=0;i<28;i++){const u=(t*2+i/28)%1,spread=(8+u*50)*power;c.globalAlpha=(1-u)*.85;ellipse(x1+dx*u,y+Math.sin(i*7+t*13)*spread,(16+u*25)*power,(6+u*18)*power,i%3===0?'#ffe28b':i%3===1?'#ff9a35':'#f24e35')}}
 c.restore();
}
function foodReaction(id,x,y,scale=1,t=0){
 c.save();c.translate(x,y);c.scale(scale,scale);
 if(id===0){ellipse(0,-28,39,10,'#ffd35cdd');for(let i=0;i<5;i++){const xx=-30+i*15;roundRect(xx,-28,9,25+Math.sin(i+t*4)*9,4,'#ffce4cdd')}label('NACHO DAY',0,73,12,'#ffe397')}
 if(id===1){for(let i=0;i<9;i++){const a=i*2.4+t,r=40+(i%3)*7;ellipse(Math.cos(a)*r,Math.sin(a)*r,4,8,'#ff9cbe')}label('PULP TRAUMA',0,73,12,'#ffbad0')}
 if(id===2){for(let i=0;i<22;i++){const a=i*2.4,rr=22+(i%4)*8;roundRect(Math.cos(a)*rr-3,Math.sin(a)*rr-8,7,6,2,i%2?'#ffda85':'#b8752e')}label('EXTRA CRISPY',0,73,12,'#ffe4a5')}
 if(id===3){for(let i=0;i<6;i++){const yy=-45-((t*35+i*13)%60);ellipse((i%2?1:-1)*(16+i*3),yy,10+(i%3)*4,7,'#ffd3bb99')}label('SPICE REGRET',0,73,12,'#ffac79')}
 c.restore();
}

function raceSabotage(t,event,racers){
 const a=racers.find(r=>r.id===event.actor),v=racers.find(r=>r.id===event.victim),u=(t-event.start)/8;
 weapon(event.actor,a.x,a.y,.85,v.x<a.x,t*7,u<.7);
 if(u<.78)foodAttack(event.actor,a.x+(v.x>a.x?40:-40),v.x,v.y-15,t,.45);
 if(u>.23)foodReaction(event.actor,v.x,v.y,.8,t);
 if(event.actor===0){ellipse(v.x,v.y+36,65,14,'#ffcf53bb');label('SLIPPERY WHEN CHEDDAR',800,580,24,'#ffe071')}
 if(event.actor===1){ellipse(v.x,v.y+38,75,12,'#ff83a888');label('CLEANUP ON LANE TWO',800,580,24,'#ffbad0')}
 if(event.actor===2){label('THEY HAVE BEEN BREADED AGAINST THEIR WILL',800,580,22,'#ffe4a5')}
 if(event.actor===3){for(let k=0;k<5;k++)ellipse(a.x-30-k*12,a.y+22,17-k*2,8,k%2?'#ff963e':'#ffe071');label('HOT SAUCE IS NOT AN APPROVED FUEL',800,580,22,'#ffb483')}
 label(`${teams[event.actor].name} USES ${sabotageNames[event.actor]}!`,800,455,26,teams[event.actor].color);
 label(sabotageJokes[event.actor],800,503,19,'#fff');
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
 const event=!dim&&t>=INTRO&&t<FINISH?sabotages.find(e=>t>=e.start&&t<e.end):null;if(!event){label('NO SKILLS. JUST FELONIES.',800,465,30,'#b3e5c8');label('THE REFEREE HAS REQUESTED A TRANSFER',800,507,17,'#8fcbad')}
 const banner=t<INTRO?'WELCOME TO THE SNACK SHOW':t>FINISH-22?'FINAL STRETCH! PANIC RESPONSIBLY!':`LAP ${Math.min(4,Math.floor(Math.max(...p))+1)} OF 4`;
 label(banner,800,132,27,'#ffe071');
 // Finish line stays at the top of the oval, across all four lanes.
 for(let xx=0;xx<5;xx++)for(let yy=0;yy<8;yy++){c.fillStyle=(xx+yy)%2?'#15253b':'#fff';c.fillRect(786+xx*7,259+yy*11,7,11)}
 label('FINISH',804,240,15,'#fff');
 const racers=teams.map((team,id)=>{let a=-Math.PI/2+2*Math.PI*p[id];return{id,x:800+(638-id*24)*Math.cos(a),y:500+(230-id*22)*Math.sin(a)}}).sort((a,b)=>a.y-b.y);
 for(const r of racers){const bounce=t>FINISH?Math.sin(t*8+r.id)*5:Math.abs(Math.sin(t*11+r.id))*6;const hit=event&&event.victim===r.id&&(t-event.start)>2;c.save();c.translate(r.x,r.y-bounce);if(hit&&event.actor===0)c.rotate(Math.sin((t-event.start)*8)*1.1);if(hit&&event.actor===2)c.scale(1.3,.7);mascot(r.id,0,0,.66,t*14+r.id);c.restore();label(teams[r.id].name,r.x,r.y-65,17,teams[r.id].color)}if(event)raceSabotage(t,event,racers);
 order.forEach((id,pos)=>{const x=66+pos*384;roundRect(x,805,360,63,12,'#06152abf');label(`${pos+1}  ${teams[id].name}`,x+20,828,22,teams[id].color,'left');label(pos===0?'ABSOLUTELY LOCKED IN':['','ALLEGEDLY AN ATHLETE','NEEDS A SNACK BREAK','JUST HERE FOR THE TICKET'][pos],x+20,852,10,'#c7d5e7','left')});
 if(dim){c.fillStyle='#020713bb';c.fillRect(0,122,1600,660)}
}
const announcements=['CHEESY HAS BEEN BANNED FROM THREE LUNCHROOMS','JUICY IS CURRENTLY 40% WATER AND 60% ATTITUDE','CRISPY BROUGHT AN ENTIRE AIR FRYER TO A FOOT RACE','SPICY THOUGHT THIS WAS A JOB INTERVIEW','THE REFEREE IS HIDING IN THE AIR FRYER','THAT CHEESE PUDDLE HAS A BETTER WIN RATE THAN YOU','JUICY HAS TURNED THE TRACK INTO A SMOOTHIE','THE CROWD HAS FILED FOR EMOTIONAL DAMAGES','CHEESY CALLS THIS A DAIRY DISPUTE','JUICY HAS ASKED TO SPEAK TO THE PHYSICS MANAGER','SPICY IS NOW LEGALLY CLASSIFIED AS A SPACE HEATER','THEY TRAINED FOR THIS. NO THEY DID NOT.'];
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
 function fighter(id,base,flip){const losing=id===lose&&impact;let xx=base+(id===left?1:-1)*lunge,yy=560;let rotation=0;if(losing){const fly=smooth(.76,.96,u);xx+=(id===left?-1:1)*fly*480;yy-=Math.sin(fly*Math.PI)*230;rotation=fly*8}c.save();c.translate(xx,yy);c.rotate(rotation);mascot(id,0,0,2.15,local*9,flip,attacks);weapon(id,0,0,2.15,flip,local*8,attacks);if(id===lose&&impact)foodReaction(win,0,0,2.15,local);c.restore()}
 fighter(left,420,false);fighter(right,1180,true);
 if(attacks){const from=cycle?right:left,to=cycle?left:right,f=(u*10)%1,a=from===left?560:1040,z=to===left?440:1160;
   foodAttack(from,a,z,490,local,1.2);
   if(f>.45)foodReaction(from,z,550,1.4,local);
   if(f>.6){star(z,490,45,teams[from].color);label(['YOU HAVE BEEN FON-DUED','100% JUICE. 0% MERCY.','YOUR WARRANTY IS NOW CRUMBS','SPICE LEVEL: REGRET'][from],800,435,27,teams[from].color)}
 }
 if(impact){const attacker=win===left?560:1040,target=lose===left?360:1240;foodAttack(win,attacker,target,495,local,2)}

 if(u<.15){label('THE FOOD COURT HAS FALLEN!',800,399,43,'#fff');label('THEY FOUND THE WEAPON AISLE. WE ARE SO SORRY.',800,450,18,'#e6c7e8')}
 else if(impact){label('SNACKTALITY!',800,390,66,'#ffe071');label(teams[win].move,800,454,30,teams[win].color);label(`${teams[win].name} WINS • ${['SENT TO THE SHADOW FRIDGE','YEETED INTO THIRD PERIOD','REFUND REQUEST DENIED','UNINSTALLED FROM THE FOOD COURT','SENT TO THE PRINCIPALS AIR FRYER','EMOTIONAL SUPPORT NUGGET REQUIRED'][b.round-1]}`,800,655,25,'#fff')}
 else{label(teams[cycle?right:left].move,800,375,33,'#ffe071')}
 c.restore();
}
function confetti(t){for(let i=0;i<120;i++){const x=(i*71+Math.sin(t+i)*40)%1600,y=((t*125+i*53)%1100)-100;c.save();c.translate(x,y);c.rotate(t*2+i);c.fillStyle=teams[i%4].color;c.fillRect(-4,-7,8,14);c.restore()}}
function victory(t){race(FINISH);c.fillStyle='#061024db';c.fillRect(0,120,1600,665);confetti(t);label('YOUR EXTREMELY OFFICIAL CHAMPION',800,205,28,'#aac1df');label(teams[champion].name,800,300,100,teams[champion].color);mascot(champion,800,510+Math.sin(t*6)*13,2.65,t*9);star(800,359,25,'#ffe071');label(teams[champion].quip,800,679,30,'#fff');label('WINNING TICKETS: MAKE AN UNREASONABLE AMOUNT OF NOISE',800,740,21,'#ffe071');label('Prize: bragging rights. Financial value: approximately zero.',800,780,16,'#b0c1dc')}
function draw(t){stadium(t);const stage=stageAt(t);if(stage==='victory')victory(t);else if(stage==='battle')battle(t,battles.find(b=>t>=b.start&&t<b.end));else{race(t);if(stage==='intro'){c.fillStyle='#061024d9';c.fillRect(300,350,1000,255);const count=Math.ceil(INTRO-t);label(count>3?'PRESENTING FOUR ABSOLUTE LEGENDS':String(count),800,430,count>3?35:110,'#ffe071');label(count>3?teams[Math.floor(t)%4].nick:'THEY HAVE NEVER TRAINED FOR THIS',800,550,29,'#fff')}else{const line=announcements[Math.floor((t-INTRO)/8)%announcements.length];label(line,800,755,21,'#dbe9fa')}}}
const BPM=128,STEP=60/BPM/4;
function ensureSound(){if(!audio||audioBus)return;audioBus=audio.createGain();audioBus.gain.value=.7;const limiter=audio.createDynamicsCompressor();limiter.threshold.value=-18;limiter.knee.value=14;limiter.ratio.value=5;limiter.attack.value=.003;limiter.release.value=.12;audioBus.connect(limiter).connect(audio.destination);const delay=audio.createDelay(.8),feedback=audio.createGain();echoBus=audio.createGain();delay.delayTime.value=60/BPM*.75;feedback.gain.value=.23;echoBus.gain.value=.16;echoBus.connect(delay);delay.connect(feedback).connect(delay);delay.connect(audioBus);noiseBuffer=audio.createBuffer(1,audio.sampleRate*.3,audio.sampleRate);const data=noiseBuffer.getChannelData(0);let noise=seeded(43117);for(let i=0;i<data.length;i++)data[i]=noise()*2-1}
function midi(note){return 440*Math.pow(2,(note-69)/12)}
function tone(freq,time,length=.13,type='triangle',gain=.05,slide=0){if(!audio||!music)return;ensureSound();const o=audio.createOscillator(),g=audio.createGain(),filter=audio.createBiquadFilter();o.type=type;o.frequency.setValueAtTime(freq,time);if(slide)o.frequency.exponentialRampToValueAtTime(slide,time+length);filter.type='lowpass';filter.frequency.setValueAtTime(type==='sawtooth'?2400:6000,time);if(type==='sawtooth')filter.frequency.exponentialRampToValueAtTime(450,time+length);g.gain.setValueAtTime(.0001,time);g.gain.exponentialRampToValueAtTime(gain,time+.008);g.gain.exponentialRampToValueAtTime(.0001,time+length);o.connect(filter).connect(g);g.connect(audioBus);if(freq>200)g.connect(echoBus);o.start(time);o.stop(time+length+.02)}
function drum(kind,time,volume=1){if(!audio||!music)return;ensureSound();if(kind==='kick'){tone(155,time,.22,'sine',.30*volume,43);return}const src=audio.createBufferSource(),g=audio.createGain(),filter=audio.createBiquadFilter();src.buffer=noiseBuffer;filter.type='highpass';filter.frequency.value=kind==='hat'?8000:1400;const duration=kind==='hat'?.045:.16;g.gain.setValueAtTime(kind==='hat'?.036*volume:.12*volume,time);g.gain.exponentialRampToValueAtTime(.0001,time+duration);src.connect(filter).connect(g).connect(audioBus);src.start(time);src.stop(time+duration+.01);if(kind==='clap')tone(190,time,.09,'triangle',.055*volume)}
function playPopStep(index,time,mode='race'){
 const step=index%16,bar=Math.floor(index/16),root=[48,43,45,41][bar%4],minor=bar%4===2,third=minor?3:4;
 if(step%4===0)drum('kick',time,mode==='battle'?1.1:1);
 if(step===4||step===12){drum('clap',time);drum('clap',time+.012,.35)}
 if(step%2===0)drum('hat',time,step%4===2?1.4:.7);if(mode==='battle'&&step%2)drum('hat',time,.4);
 if([0,3,6,8,11,14].includes(step)){tone(midi(root-12),time,STEP*1.45,'sine',.15);tone(midi(root),time,STEP*.8,'triangle',.033)}
 if([2,6,10,14].includes(step))for(const note of[root+12,root+12+third,root+19])tone(midi(note),time,STEP*1.55,'sawtooth',.021);
 const hook=[76,79,81,79,76,-1,74,72,74,76,79,-1,76,74,72,-1,76,79,84,81,79,76,74,-1,72,74,76,79,76,74,72,-1];
 if(step%2===0){let note=hook[Math.floor(index/2)%hook.length];if(note>=0){if(mode==='battle')note+=bar%2?12:0;tone(midi(note),time,STEP*1.8,'triangle',.075);tone(midi(note+12),time,STEP*.65,'sine',.012)}}
 if(step===15&&bar%4===3)tone(midi(84),time,.25,'sine',.018,midi(72));
 if(mode==='victory'&&step%4===0)for(const note of[72,76,79])tone(midi(note),time,.32,'triangle',.028);
}
function weaponSound(id,time){
 if(id===0){tone(180,time,.3,'triangle',.065,70);tone(95,time+.09,.18,'sine',.11,50)}
 if(id===1){for(let i=0;i<4;i++)tone(460+i*90,time+i*.045,.10,'sine',.045,180+i*30)}
 if(id===2){for(let i=0;i<3;i++){drum('hat',time+i*.07,1.3);tone(230+i*80,time+i*.07,.055,'triangle',.04,100)}}
 if(id===3){drum('clap',time,.45);drum('hat',time+.05,1.8);tone(90,time,.45,'sawtooth',.065,40)}
}

function audioPump(){if(customMusic||!audio||!music||!running||paused||finished)return;ensureSound();const now=audio.currentTime;if(nextBeat<now-.3)nextBeat=now;while(nextBeat<now+.12){playPopStep(beat++,nextBeat,stageAt(elapsed));nextBeat+=STEP}}

setInterval(audioPump,90);
function tick(now){if(running&&!paused){elapsed=Math.max(0,Math.min(DURATION,(now-startTime)/1000));if(elapsed>=DURATION){running=false;finished=true;if(customMusic)customMusic.pause();$('again').hidden=false;$('pause').disabled=true}const b=battles.findIndex(b=>elapsed>=b.start&&elapsed<b.end);if(b!==lastSound){if(b>=0&&audio){tone(150,audio.currentTime,.5,'sawtooth',.06,40);tone(650,audio.currentTime+.2,.4,'triangle',.03,160)}lastSound=b}const event=sabotages.find(e=>elapsed>=e.start&&elapsed<e.end);const fight=b>=0?battles[b]:null;const slot=event?'s'+sabotages.indexOf(event)+':'+Math.floor((elapsed-event.start)/1.6):fight?'b'+b+':'+Math.floor((elapsed-fight.start)/1.2):'';if(slot&&slot!==lastFxSlot&&audio&&music){weaponSound(event?event.actor:fight.pair[Math.floor((elapsed-fight.start)/1.2)%2],audio.currentTime);lastFxSlot=slot}}draw(elapsed);requestAnimationFrame(tick)}
async function start(){if(running||finished)return;try{if(!audio)audio=new(window.AudioContext||window.webkitAudioContext)();audio.resume().catch(error=>console.warn("Audio unavailable:",error))}catch(error){console.warn('Audio unavailable:',error)}$('lobby').hidden=true;running=true;startTime=performance.now();$('pause').disabled=false;nextBeat=audio?audio.currentTime:0;syncCustomMusic()}
function pause(){if(!running)return;paused=!paused;if(paused)pauseTime=performance.now();else startTime+=performance.now()-pauseTime;$('pauseLabel').hidden=!paused;$('pause').textContent=paused?'Resume':'Pause';syncCustomMusic()}
async function full(){try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch(error){console.warn('Fullscreen unavailable:',error)}}
function toggleMusic(){music=!music;$('mute').textContent=`Music: ${music?'ON':'OFF'}`;if(music&&audio){audio.resume();nextBeat=audio.currentTime}syncCustomMusic()}
function syncCustomMusic(){
 if(!customMusic)return;
 if(!running||paused||!music||finished){customMusic.pause();return}
 customMusic.play().catch(error=>{console.warn('Selected audio could not play:',error);$('musicStatus').textContent='Audio could not play. Choose another file or use the built-in soundtrack.'});
}
function chooseSoundtrack(file){
 if(!file)return;
 if(customMusic){customMusic.pause();customMusic.src=''}
 if(customUrl)URL.revokeObjectURL(customUrl);
 customUrl=URL.createObjectURL(file);customMusic=new Audio(customUrl);customMusic.loop=true;customMusic.volume=.45;
 customMusic.onerror=()=>{$('musicStatus').textContent='Unsupported audio file. Using built-in pop.';customMusic.pause();customMusic=null;nextBeat=audio?audio.currentTime:0};
 $('musicStatus').textContent='Soundtrack: '+file.name+' (local playback only)';
 $('chooseMusic').textContent='Change music file';syncCustomMusic();
}
$('chooseMusic').onclick=()=>$('musicFile').click();
$('musicFile').onchange=event=>chooseSoundtrack(event.target.files[0]);
$('start').onclick=start;$('pause').onclick=pause;$('mute').onclick=toggleMusic;$('full').onclick=full;$('print').onclick=()=>window.print();$('shuffle').onclick=assignTickets;$('again').onclick=()=>{newShow();$('lobby').hidden=false};
document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();if(!$('lobby').hidden)start();else pause()}if(e.key.toLowerCase()==='f')full();if(e.key.toLowerCase()==='m')toggleMusic()});
assignTickets();newShow();requestAnimationFrame(tick);
// Test access is absent from the normal classroom view.
if(new URLSearchParams(location.search).has('test'))window.derbyTest={seek(t){elapsed=Math.max(0,Math.min(DURATION,t));startTime=performance.now()-elapsed*1000;draw(elapsed)},snapshot(){return{elapsed,stage:stageAt(elapsed),champion,rank:rank.slice(),progress:progress(elapsed),running,paused,tickets:ticketTeams.slice(),battles:battles.map(b=>({...b})),sabotages:sabotages.map(e=>({...e})),duration:DURATION,customAudio:customMusic?{paused:customMusic.paused,muted:!music,loop:customMusic.loop}:null}},newShow,previewPop(context,seconds=12){audio=context;audioBus=null;echoBus=null;music=true;ensureSound();for(let step=0;step*STEP<seconds;step++)playPopStep(step,step*STEP,"race")}};
</script></body></html>'''


def build_page(duration: int = 360) -> str:
    """Return a self-contained show with original canvas art and synthesized audio."""
    if not 180 <= duration <= 360:
        raise ValueError("Choose a show length between 180 and 360 seconds.")
    minutes, seconds = divmod(duration, 60)
    label = f"{minutes}-minute" if not seconds else f"{minutes}-minute {seconds}-second"
    return HTML.replace("__DURATION__", str(duration)).replace("__DURATION_LABEL__", label)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=int, default=360, choices=range(180, 361),
                        metavar="180-360", help="Show length in seconds (default: 360).")
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
