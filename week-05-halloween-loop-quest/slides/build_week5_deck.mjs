import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = process.cwd();
const buildDir = path.join(workspaceDir, ".codex-build", "week5-slides");
const outputDir = path.join(workspaceDir, "week-05-halloween-loop-quest", "slides");
const finalPath = path.join(outputDir, "week-05-engineering-foundations-workshop-v6.pptx");
const skillDir = "C:\\Users\\louie\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.1025.11240\\skills\\presentations";
const python = "C:\\Users\\louie\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe";
const navy="#071A33", blue="#1D4ED8", teal="#0F766E", green="#15803D", coral="#E85D4A", ink="#122033", muted="#526174", pale="#EEF4FA", white="#FFFFFF";

await fs.mkdir(buildDir,{recursive:true}); await fs.mkdir(outputDir,{recursive:true});
const deck=Presentation.create({slideSize:{width:1280,height:720}});

function box(slide,left,top,width,height,fill="none",line="none",radius="rounded-md"){
  return slide.shapes.add({geometry:radius==="none"?"rect":"roundRect",position:{left,top,width,height},fill,line:{style:"solid",fill:line,width:line==="none"?0:1},...(radius==="none"?{}:{borderRadius:radius})});
}
function text(slide,value,left,top,width,height,size=28,color=ink,bold=false,font="Arial",align="left"){
  const s=slide.shapes.add({geometry:"textbox",position:{left,top,width,height},fill:"none",line:{style:"solid",fill:"none",width:0}});
  s.text=value; s.text.style={fontFamily:font,fontSize:size,color,bold,alignment:align,verticalAlignment:"middle",wrap:true}; return s;
}
function base(title,subtitle=""){
  const s=deck.slides.add(); s.background.fill=white;
  box(s,0,0,1280,18,teal,"none","none"); text(s,title,64,42,1148,58,34,navy,true);
  if(subtitle) text(s,subtitle,66,98,1140,34,18,muted,false);
  text(s,String(deck.slides.items.length).padStart(2,"0"),1180,670,40,24,12,muted,true);
  return s;
}
function bullets(slide,items,left=82,top=160,width=1110,size=26,gap=74){
  items.forEach((item,i)=>{text(slide,"•",left,top+i*gap,28,38,size,teal,true);text(slide,item,left+38,top+i*gap,width-38,56,size,ink,false);});
}
function codeBlock(slide,code,left=100,top=175,width=1080,height=390){
  box(slide,left,top,width,height,"#F4F7FA","#C8D3DF","rounded-lg"); text(slide,code,left+28,top+20,width-56,height-40,24,ink,false,"Consolas");
}

let s=deck.slides.add(); s.background.fill=navy; box(s,0,0,1280,18,coral,"none","none");
text(s,"Python Foundations for Engineers",72,138,1100,90,50,white,true); text(s,"Beginner review before the team labs",76,238,1050,48,28,"#B8D7F0");
text(s,"Week 5: Mario review and three guided Colab labs",76,584,1080,36,20,"#D9E8F5",false);

s=base("Today’s path","Class ends at 1:00 PM — the first 15 minutes are for arrival and setup");
bullets(s,["9:00–9:15  Arrive, sign in, open the browser, and get settled","9:15–9:35  Mario review and class voting","9:35–10:25  Super Mario Team Quest in Module 1","10:00  Coin Rush photo showcase","10:25–10:35  Break","10:35–11:20  Module 2: Arcade Loop Trainer","11:20–11:30  Break","11:30–1:00  Module 3, boss challenge, peer debugging, and exit"],72,132,1140,20,62);

s=base("Google Colab setup","GitHub supplies the class notebook. Google Drive stores your copy.");
bullets(s,["Open the module link from the Week 5 GitHub README","Sign into the Google account you will use for class","Choose File, then Save a copy in Drive","Rename the copy with your name and module number","Complete the lesson only in your saved Drive copy"],88,150,1090,25,78);
text(s,"git pull updates a repository on a local computer. You do not need it for today’s Colab lesson.",88,574,1095,48,21,coral,true);

s=base("Mario is a software system","Every game action depends on the same foundations engineers use");
text(s,"VARIABLES",82,158,220,34,19,teal,true); text(s,"Store Mario’s lives, coins, speed, and power state",82,198,470,72,26,ink,true);
text(s,"LISTS",82,322,220,34,19,teal,true); text(s,"Keep enemies, questions, platforms, and collected items",82,362,470,72,26,ink,true);
text(s,"CONDITIONS",690,158,240,34,19,coral,true); text(s,"Choose what happens after a collision or answer",690,198,470,72,26,ink,true);
text(s,"LOOPS + FUNCTIONS",690,322,330,34,19,coral,true); text(s,"Update the world repeatedly and reuse reliable actions",690,362,470,72,26,ink,true);
text(s,"Engineering starts by turning a real situation into data, rules, repetition, and reusable jobs.",84,540,1090,70,28,navy,true,"Arial","center");

s=base("Variables and lists model a system","Engineers name the information a program must remember");
codeBlock(s,'player = "Mario"\nlives = 3\ncoins = 12\npower_ups = ["mushroom", "leaf"]',72,165,610,300);
text(s,"Why engineers need them",750,166,390,42,24,teal,true);
text(s,"A delivery app stores drivers and orders.\n\nA robot stores sensor readings.\n\nA game stores players and inventory.",750,220,420,240,25,ink,false);
text(s,"Quick check: Which name stores one value? Which name stores several values?",72,530,1090,66,27,coral,true,"Arial","center");

s=base("Conditions encode decisions","Engineers turn requirements and safety rules into True or False checks");
codeBlock(s,'door_closed = True\nperson_nearby = True\n\nif door_closed and person_nearby:\n    stop_motor()',72,165,610,315);
text(s,"Why engineers need them",750,166,390,42,24,teal,true);
text(s,"Games choose whether Mario takes damage.\n\nWebsites decide whether a login is valid.\n\nMachines stop when a safety rule becomes true.",750,220,430,255,25,ink,false);
text(s,"Engineering question: What could go wrong if the condition checks the wrong value?",72,540,1090,56,26,coral,true,"Arial","center");

s=base("Loops make work scale","Engineers describe one correct action, then repeat it across the data");
codeBlock(s,'temperatures = [72, 75, 91, 68]\n\nfor temperature in temperatures:\n    if temperature > 90:\n        print("ALERT")',72,165,620,315);
text(s,"Without a loop",755,170,390,38,23,coral,true); text(s,"Copy the same code for every sensor",755,212,400,60,25,ink,false);
text(s,"With a loop",755,322,390,38,23,teal,true); text(s,"One tested block can process four sensors or four million",755,364,410,92,25,ink,true);
text(s,"Quick check: What changes during each iteration?",72,540,1090,56,27,navy,true,"Arial","center");

s=base("Functions make code reusable","Engineers give a reliable job a name so teammates can call it");
codeBlock(s,'def calculate_total(prices):\n    total = 0\n    for price in prices:\n        total += price\n    return total',72,160,625,340);
text(s,"Why engineers need them",760,164,390,42,24,teal,true);
text(s,"A function can be tested once.\n\nTeammates can reuse it without rewriting the steps.\n\nA clear name explains the job the code performs.",760,220,410,260,25,ink,false);
text(s,"Trace it: What enters the function? What repeats? What returns?",72,548,1090,50,27,coral,true,"Arial","center");

s=base("Engineers debug with evidence","A failure shows which assumption or value needs another look");
text(s,"1",86,170,55,55,35,teal,true,"Arial","center"); text(s,"Predict the result before running",155,168,950,58,29,ink,true);
text(s,"2",86,265,55,55,35,teal,true,"Arial","center"); text(s,"Run one test and read the actual result",155,263,950,58,29,ink,true);
text(s,"3",86,360,55,55,35,teal,true,"Arial","center"); text(s,"Find the first value that differs from the prediction",155,358,980,58,29,ink,true);
text(s,"4",86,455,55,55,35,teal,true,"Arial","center"); text(s,"Change one thing, then run the same test again",155,453,950,58,29,ink,true);
text(s,"The Mario labs use failure animations because engineers learn by testing and repairing systems.",82,570,1100,48,22,coral,true,"Arial","center");

s=base("A loop repeats a block","The computer follows the same steps for several values");
text(s,"PLAIN ENGLISH",88,170,290,34,18,teal,true); text(s,"For each player in the team, print the player’s name.",88,215,1090,58,32,ink,true);
text(s,"PYTHON",88,330,180,34,18,teal,true); codeBlock(s,'players = ["Ava", "Noah", "Zion"]\n\nfor player in players:\n    print(player)',88,370,850,220);

s=base("Human loop practice","Three volunteers act as the list, loop variable, and computer");
bullets(s,["List student points to the next name","Variable student holds that one name","Computer student reads the indented instruction","Class counts the iteration","Repeat until the list has no more items"],94,158,1085,25,84);

s=base("Parts of a for loop","Point to each part before tracing");
codeBlock(s,'enemies = ["slime", "ghost", "dragon"]\n\nfor enemy in enemies:\n    print("Battle:", enemy)',80,180,760,300);
text(s,"collection",900,190,250,42,23,blue,true); text(s,"loop variable",900,286,250,42,23,coral,true); text(s,"repeated block",900,382,250,42,23,green,true);

s=base("Trace one iteration at a time","Predict the final count before Run");
codeBlock(s,'enemies = ["slime", "ghost", "dragon"]\ncount = 0\n\nfor enemy in enemies:\n    count = count + 1\n    print(count, enemy)\n\nprint("Final:", count)',72,160,760,430);
text(s,"Trace",888,170,220,38,24,teal,true); text(s,"Start: count = 0\n\n1: count = ___\n2: count = ___\n3: count = ___",888,222,310,260,25,ink,false);

s=base("An accumulator builds a result","The variable keeps the total from earlier iterations");
codeBlock(s,'scores = [4, 6, 5]\ntotal = 0\n\nfor score in scores:\n    total = total + score\n\nprint(total)',80,180,690,330);
text(s,"0",850,220,70,60,34,navy,true,"Arial","center"); text(s,"4",970,220,70,60,34,blue,true,"Arial","center"); text(s,"10",1090,220,70,60,34,teal,true,"Arial","center"); text(s,"15",970,350,70,60,34,green,true,"Arial","center");
text(s,"Say each update: old total + current score = new total",800,480,380,78,23,muted,true,"Arial","center");

s=base("While loops need an exit","Name what stays true and what changes");
codeBlock(s,'energy = 3\n\nwhile energy > 0:\n    print(energy)\n    energy = energy - 1\n\nprint("REST")',78,170,670,370);
text(s,"Keeps running",820,192,320,40,22,teal,true); text(s,"energy > 0",820,236,320,44,28,ink,true);
text(s,"Changes",820,328,320,40,22,coral,true); text(s,"energy = energy - 1",820,372,350,56,25,ink,true);

s=base("Loop check before Module 1","Answer with a partner");
bullets(s,["How many times does a for loop run over a four-item list?","What does the loop variable hold during one iteration?","Why does an accumulator start before the loop?","What must change inside most while loops?"],96,176,1080,27,104);

s=base("Super Mario Team Quest","Module 1 is the main showcase from 9:35 to 10:25");
bullets(s,["Teams choose Driver, Navigator, Predictor, and Reporter roles","Each code cell changes an animated Mario scene","Students visit another team for the 10:00 Coin Rush","Pairs finish with a Mario versus Bowser castle battle"],100,182,1080,27,100);
text(s,"Open module-1-game-loadout.ipynb in Colab",100,590,1080,46,24,blue,true);

s=base("Coin Rush photo showcase","At 10:00, every team visits another team and triggers the reveal");
codeBlock(s,'coins = starting_coins\ncoins = coins + visitor_bonus\ncoins = coins + question_bonus\n\nif coins >= 10:\n    finish = "SECRET PIPE UNLOCKED!"',80,170,700,350);
text(s,"Photo moment",850,180,290,42,25,coral,true); text(s,"Teams stand together\n\nPredictors announce the total\n\nDrivers run at the same time\n\nAnimated results fill every screen",850,240,330,310,25,ink,false);

s=base("Break","10 minutes"); text(s,"Stand up. Get water. Be back when the timer ends.",140,270,1000,70,32,navy,true,"Arial","center");

s=base("Module 2 practice","Arcade Loop Trainer is today’s main learning block");
bullets(s,["Act out one loop with student volunteers","Trace a counter through four iterations","Trace an accumulator through three scores","Build a new list inside a loop","Repair a while loop so it stops","Complete the arcade scoreboard boss"],92,142,1100,23,76);

s=base("Loop boss challenge","Count games, total scores, and identify bonus rounds");
codeBlock(s,'scores = [8, 12, 5, 15]\ngames = 0\ntotal = 0\n\nfor score in scores:\n    games += 1\n    total += score\n    if score >= 10:\n        print("BONUS", score)',75,150,730,450);
text(s,"Before Run",875,174,260,38,24,coral,true); text(s,"games = ___\n\ntotal = ___\n\nbonus scores = ___",875,235,310,250,27,ink,false);

s=base("Break","10 minutes"); text(s,"Reset your brain. Module 3 connects functions and loops.",140,270,1000,70,32,navy,true,"Arial","center");

s=base("Module 3 practice","Power-Up Functions: name reusable jobs");
codeBlock(s,'def add_bonus(score, bonus):\n    new_score = score + bonus\n    return new_score\n\nfinal_score = add_bonus(10, 5)',74,170,690,340);
text(s,"Trace the call",830,175,320,38,24,teal,true); text(s,"arguments\n10 and 5\n\nparameters\nscore and bonus\n\nreturn value\n15",830,224,320,300,25,ink,false);

s=base("Functions can contain loops","One function can own the complete totaling job");
codeBlock(s,'def total_scores(scores):\n    total = 0\n    for score in scores:\n        total += score\n    return total\n\nteam_total = total_scores([4, 6, 5])',78,165,770,410);
text(s,"Explain",900,180,250,38,24,coral,true); text(s,"What enters?\n\nWhat repeats?\n\nWhat changes?\n\nWhat returns?",900,235,270,300,27,ink,false);

s=base("Peer debug routine","The reviewer explains before touching the keyboard");
bullets(s,["Developer states the expected result","Reviewer traces one test case on paper","Pair runs the same case","Reviewer names the first unexpected value","Developer changes one line and retests"],100,160,1080,26,88);

s=base("Exit ticket","Write complete sentences");
bullets(s,["What does a loop variable hold?","How does an accumulator change?","When would you choose while instead of for?","What must happen so a while loop stops?","How can a function use a loop?"],100,156,1080,26,88);

for(let i=0;i<deck.slides.items.length;i++){
  const slide=deck.slides.items[i]; const blob=await deck.export({slide,format:"png",scale:1});
  await fs.writeFile(path.join(buildDir,`slide-${String(i+1).padStart(2,"0")}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const montage=await deck.export({format:"webp",montage:true}); await fs.writeFile(path.join(buildDir,"montage.webp"),new Uint8Array(await montage.arrayBuffer()));
const {finalizePresentation}=await import(pathToFileURL(path.join(skillDir,"container_tools","artifact_tool_utils.mjs")).href);
const candidate=path.join(buildDir,"candidate.pptx"); await (await PresentationFile.exportPptx(deck)).save(candidate);
await finalizePresentation({workspaceDir,candidatePath:candidate,finalPath,pythonExecutable:python,integrityValidatorPath:path.join(skillDir,"container_tools","inspect_presentation_package_integrity.py"),layoutValidatorPath:path.join(skillDir,"container_tools","inspect_presentation_layout_geometry.py"),layoutArgs:["--expected-slide-size-emu","12192000,6858000","--validate-heading-fit"],fontPolicy:{basis:"design",families:["Aptos"]},verifyArtifactToolImport:true,receiptPath:path.join(buildDir,"validation-v6.json")});
console.log(finalPath);
