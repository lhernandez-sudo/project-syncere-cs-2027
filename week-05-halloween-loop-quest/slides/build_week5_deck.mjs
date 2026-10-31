import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = process.cwd();
const buildDir = path.join(workspaceDir, ".codex-build", "week5-slides");
const outputDir = path.join(workspaceDir, "week-05-halloween-loop-quest", "slides");
const finalPath = path.join(outputDir, "week-05-review-game-labs-v9.pptx");
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
bullets(s,["9:00–9:15  Arrive, sign in, open the browser, and get settled","9:15–9:22  Fast engineering concept review","9:22–9:40  Mario Python review game","9:40–10:25  Super Mario Debug Quest in Module 1","10:25–10:35  Break","10:35–11:20  Module 2: Arcade Loop Trainer","11:20–11:30  Break","11:30–12:35  Module 3 and boss challenge","12:35–12:50  Quick preview: classes and objects","12:50–1:00  Exit ticket and notebook download"],72,126,1140,18,52);

s=base("Mario is a software system","Every game action depends on the same foundations engineers use");
text(s,"VARIABLES",82,158,220,34,19,teal,true); text(s,"Store Mario’s lives, coins, speed, and power state",82,198,470,72,26,ink,true);
text(s,"LISTS",82,322,220,34,19,teal,true); text(s,"Keep enemies, questions, platforms, and collected items",82,362,470,72,26,ink,true);
text(s,"CONDITIONS",690,158,240,34,19,coral,true); text(s,"Choose what happens after a collision or answer",690,198,470,72,26,ink,true);
text(s,"LOOPS + FUNCTIONS",690,322,330,34,19,coral,true); text(s,"Update the world repeatedly and reuse reliable actions",690,362,470,72,26,ink,true);
text(s,"Engineering starts by turning a real situation into data, rules, repetition, and reusable jobs.",84,540,1090,70,28,navy,true,"Arial","center");

s=base("Engineers debug with evidence","A failure shows which assumption or value needs another look");
text(s,"1",86,170,55,55,35,teal,true,"Arial","center"); text(s,"Predict the result before running",155,168,950,58,29,ink,true);
text(s,"2",86,265,55,55,35,teal,true,"Arial","center"); text(s,"Run one test and read the actual result",155,263,950,58,29,ink,true);
text(s,"3",86,360,55,55,35,teal,true,"Arial","center"); text(s,"Find the first value that differs from the prediction",155,358,980,58,29,ink,true);
text(s,"4",86,455,55,55,35,teal,true,"Arial","center"); text(s,"Change one thing, then run the same test again",155,453,950,58,29,ink,true);
text(s,"The Mario labs use failure animations because engineers learn by testing and repairing systems.",82,570,1100,48,22,coral,true,"Arial","center");

s=base("Mario Python review game","Use the game to identify which concepts need practice today");
bullets(s,["We play together on the projector as one class","One student controls the answer while everyone votes","Vote before the 20-second timer ends","Name the concept after every answer","Rotate the controller after each Python world"],100,145,1080,25,82);
text(s,"After the final gate, form teams of 3 or 4 for Module 1.",100,574,1080,48,26,coral,true,"Arial","center");

s=base("Google Colab setup","The whole-class Mario game leads into the first team notebook");
bullets(s,["Form a team of 3 or 4 after the review game","Open Module 1 from the Week 5 GitHub README","Sign into the Google account you will use for class","Choose File, then Save a copy in Drive","Rename the copy with your name and module number"],88,150,1090,25,78);
text(s,"git pull updates a repository on a local computer. You do not need it for today’s Colab lesson.",88,574,1095,48,21,coral,true);

s=base("Super Mario Debug Quest","Module 1 continues the same concepts and team energy");
bullets(s,["Work in the team you formed after the class game","Choose Driver, Navigator, Predictor, and Debugger roles","Run each broken mission once and watch Mario fail","Use the tips to repair variables, lists, and conditions","Finish with the Mario versus Bowser coding challenge"],100,158,1080,25,86);
text(s,"Open module-1-game-loadout.ipynb in Colab",100,590,1080,46,24,blue,true);

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

s=base("Classes and objects","A short preview for future lessons");
text(s,"CLASS",82,160,210,34,19,teal,true); text(s,"A blueprint that describes shared data and actions",82,200,470,72,26,ink,true);
text(s,"OBJECT",82,330,210,34,19,teal,true); text(s,"One independent thing created from the blueprint",82,370,470,72,26,ink,true);
text(s,"ATTRIBUTES",690,160,240,34,19,coral,true); text(s,"Values stored on an object, such as name or health",690,200,470,72,26,ink,true);
text(s,"METHODS",690,330,240,34,19,coral,true); text(s,"Actions an object can perform, such as jump or take damage",690,370,470,86,26,ink,true);
text(s,"Classes organize concepts you already know. They still use variables, conditions, loops, and functions.",84,555,1090,66,25,navy,true,"Arial","center");

s=base("A Player blueprint","__init__ gives each new object its starting attributes");
codeBlock(s,'class Player:\n    def __init__(self, name):\n        self.name = name\n        self.health = 3\n\n    def take_damage(self):\n        self.health -= 1',72,160,720,400);
text(s,"Read it aloud",850,170,300,38,24,teal,true); text(s,"self means this object\n\nname and health are attributes\n\ntake_damage is a method\n\nNo coding assignment today",850,225,340,300,24,ink,false);

s=base("Objects keep independent state","The same class can create many game characters");
codeBlock(s,'mario = Player("Mario")\nluigi = Player("Luigi")\n\nmario.take_damage()\n\nprint(mario.health)  # 2\nprint(luigi.health)  # 3',72,165,680,370);
text(s,"Why engineers care",820,170,340,38,24,coral,true); text(s,"The class defines the shared rules.\n\nEach object keeps its own values.\n\nUse classes when a program manages many related things with the same kinds of actions.",820,225,360,270,24,ink,false);
text(s,"For now, recognize the pattern. We will build classes after the foundations feel comfortable.",110,570,1060,48,23,blue,true,"Arial","center");

s=base("Peer debug routine","The reviewer explains before touching the keyboard");
bullets(s,["Developer states the expected result","Reviewer traces one test case on paper","Pair runs the same case","Reviewer names the first unexpected value","Developer changes one line and retests"],100,160,1080,26,88);

s=base("Exit ticket","Write complete sentences");
bullets(s,["What does a loop variable hold?","How does an accumulator change?","When would you choose while instead of for?","How can a function use a loop?","What is the difference between a class and an object?"],100,156,1080,26,88);

for(let i=0;i<deck.slides.items.length;i++){
  const slide=deck.slides.items[i]; const blob=await deck.export({slide,format:"png",scale:1});
  await fs.writeFile(path.join(buildDir,`slide-${String(i+1).padStart(2,"0")}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const montage=await deck.export({format:"webp",montage:true}); await fs.writeFile(path.join(buildDir,"montage.webp"),new Uint8Array(await montage.arrayBuffer()));
const {finalizePresentation}=await import(pathToFileURL(path.join(skillDir,"container_tools","artifact_tool_utils.mjs")).href);
const candidate=path.join(buildDir,"candidate.pptx"); await (await PresentationFile.exportPptx(deck)).save(candidate);
await finalizePresentation({workspaceDir,candidatePath:candidate,finalPath,pythonExecutable:python,integrityValidatorPath:path.join(skillDir,"container_tools","inspect_presentation_package_integrity.py"),layoutValidatorPath:path.join(skillDir,"container_tools","inspect_presentation_layout_geometry.py"),layoutArgs:["--expected-slide-size-emu","12192000,6858000","--validate-heading-fit"],fontPolicy:{basis:"design",families:["Aptos"]},verifyArtifactToolImport:true,receiptPath:path.join(buildDir,"validation-v9.json")});
console.log(finalPath);
