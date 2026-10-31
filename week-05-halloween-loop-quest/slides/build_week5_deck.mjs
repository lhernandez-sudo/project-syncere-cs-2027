import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = process.cwd();
const buildDir = path.join(workspaceDir, ".codex-build", "week5-slides");
const outputDir = path.join(workspaceDir, "week-05-halloween-loop-quest", "slides");
const finalPath = path.join(outputDir, "week-05-beginner-loop-workshop-v2.pptx");
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
text(s,"Python Loop Workshop",72,138,1080,90,52,white,true); text(s,"Beginner practice before every lab module",76,238,1050,48,28,"#B8D7F0");
text(s,"Week 5  •  Mario review  •  Three guided Colab labs",76,584,1080,36,20,"#D9E8F5",false);

s=base("Today’s path","Class ends at 1:00 PM — the first 15 minutes are for arrival and setup");
bullets(s,["9:00–9:15  Arrive, sign in, open the browser, and get settled","9:15–9:35  Mario review and class voting","9:35–10:25  Loop demonstration and Module 1","10:25–10:35  Break","10:35–11:20  Module 2: Arcade Loop Trainer","11:20–11:30  Break","11:30–12:15  Module 3: Power-Up Functions","12:15–1:00  Boss challenge, peer debugging, exit ticket, and save"],72,132,1140,20,62);

s=base("Participation routine","Every student gets thinking time before anyone answers");
bullets(s,["Think silently for 20 seconds","Write one prediction","Compare with one partner","Vote with fingers: 1, 2, or 3","Run the code only after the vote","Explain the result in plain English"],110,150,1050,24,72);

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

s=base("Module 1 practice","Game Loadout: variables, lists, and decisions");
bullets(s,["Teacher models the first variable trace","Class predicts the backpack after append","Pairs test the decision boundary at 9, 10, and 11","Students complete the loadout boss challenge"],100,182,1080,27,100);
text(s,"Open module-1-game-loadout.ipynb in Colab",100,590,1080,46,24,blue,true);

s=base("Practice before Module 1","No typing for the first prediction");
codeBlock(s,'coins = 5\ncoins = coins + 3\ncoins = coins - 1\n\nprint(coins)',115,190,650,300);
text(s,"1. Write the starting value\n2. Update after treasure\n3. Update after the shop\n4. Compare with a partner\n5. Run and explain",830,190,340,300,25,ink,false);

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
await finalizePresentation({workspaceDir,candidatePath:candidate,finalPath,pythonExecutable:python,integrityValidatorPath:path.join(skillDir,"container_tools","inspect_presentation_package_integrity.py"),layoutValidatorPath:path.join(skillDir,"container_tools","inspect_presentation_layout_geometry.py"),layoutArgs:["--expected-slide-size-emu","12192000,6858000","--validate-heading-fit"],fontPolicy:{basis:"design",families:["Aptos"]},verifyArtifactToolImport:true,receiptPath:path.join(buildDir,"validation-v2.json")});
console.log(finalPath);
