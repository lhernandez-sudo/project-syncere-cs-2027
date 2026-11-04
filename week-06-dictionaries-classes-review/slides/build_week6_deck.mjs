import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = process.cwd();
const buildDir = path.join(workspaceDir, ".codex-build", "week6-slides");
const outputDir = path.join(workspaceDir, "week-06-dictionaries-classes-review", "slides");
const finalPath = path.join(outputDir, "week-06-dictionaries-classes-review-v7.pptx");
const skillDir = "C:\\Users\\louie\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.1030.10813\\skills\\presentations";
const python = "C:\\Users\\louie\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe";
const navy="#071A33", blue="#1D4ED8", teal="#0F766E", green="#15803D", coral="#E85D4A", ink="#122033", muted="#526174", pale="#EEF4FA", white="#FFFFFF", gold="#D89B18";

await fs.mkdir(buildDir,{recursive:true});
await fs.mkdir(outputDir,{recursive:true});
const deck=Presentation.create({slideSize:{width:1280,height:720}});

function box(slide,left,top,width,height,fill="none",line="none",radius="rounded-md"){
  return slide.shapes.add({geometry:radius==="none"?"rect":"roundRect",position:{left,top,width,height},fill,line:{style:"solid",fill:line,width:line==="none"?0:1},...(radius==="none"?{}:{borderRadius:radius})});
}
function text(slide,value,left,top,width,height,size=28,color=ink,bold=false,font="Aptos",align="left"){
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
function bullets(slide,items,left=88,top=150,width=1100,size=25,gap=76,color=teal){
  items.forEach((item,i)=>{text(slide,"•",left,top+i*gap,28,38,size,color,true);text(slide,item,left+38,top+i*gap,width-38,56,size,ink,false);});
}
function codeBlock(slide,code,left=80,top=165,width=760,height=390){
  box(slide,left,top,width,height,"#F4F7FA","#C8D3DF","rounded-lg"); text(slide,code,left+30,top+20,width-60,height-40,23,ink,false,"Consolas");
}

let s=deck.slides.add(); s.background.fill=navy; box(s,0,0,1280,18,coral,"none","none");
text(s,"Code and Consequences",72,145,1100,82,52,white,true);
text(s,"Beginner programming and technology awareness",76,242,1080,48,30,"#B8D7F0");
text(s,"Week 6 self-guided Colab session",76,584,1080,36,21,"#D9E8F5");

s=base("Today’s plan","Programming first, technology investigation after the second break");
bullets(s,["9:00–9:15  Arrive, sign in, and open Week 6","9:15–9:30  Secret Identity Generator","9:30–10:25  Notebook 1: Dictionary Arcade","10:25–10:35  Break","10:35–11:20  Notebook 2: Friendly Character Classes","11:20–11:30  Break and form groups of 2 or 3","11:30–12:15  Technology research","12:15–12:45  Share-outs and discussion","12:45–1:00  Individual exit ticket"],72,126,1140,18,55);

s=base("Work style","Independent programming, then small-group investigation");
bullets(s,["Save an individual Google Drive copy","Read each notebook cell before running it","Try one repair before asking for help","Complete Notebook 1, then open Notebook 2","Form groups of 2 or 3 after the second break","Use evidence and respectful disagreement","Complete the final exit ticket independently"],86,136,1100,22,66);

s=base("Week 6 Colab links","Choose either route, then open the Week 6 README");
text(s,"LOCAL PROJECT",80,152,470,34,20,teal,true);
text(s,"1. Open a terminal in the project folder\n\n2. Run  git pull\n\n3. Open the Week 6 folder\n\n4. Open README.md and click a Colab link",80,200,500,300,24,ink,false);
text(s,"GITHUB WEBSITE",700,152,470,34,20,coral,true);
text(s,"1. Paste the repository URL into a browser\n\n2. Open week-06-dictionaries-classes-review\n\n3. Open README.md\n\n4. Click the notebook's Colab link",700,200,500,300,24,ink,false);
text(s,"https://github.com/lhernandez-sudo/project-syncere-cs-2027.git",80,572,1120,38,18,blue,true,"Consolas","center");

s=base("Secret Identity Generator","Individual and private, about 15 minutes");
bullets(s,["Run the generator to get a random draft","Reroll until a combination makes you laugh","Customize your alias, power, snack, and weakness","Run the check and repair any unfinished value","Save your identity card in your Drive copy","Sharing with one person is optional"],90,142,1090,24,76,coral);

s=base("Notebook 1: Dictionary Arcade","The notebook teaches the new material step by step");
text(s,"START",90,155,220,34,20,teal,true); text(s,"Read the explanation and run the working example",90,198,470,70,26,ink,true);
text(s,"PRACTICE",90,335,220,34,20,teal,true); text(s,"Change one small part using the shown pattern",90,378,470,70,26,ink,true);
text(s,"CHECK",700,155,220,34,20,coral,true); text(s,"Read the message and repair one issue",700,198,470,70,26,ink,true);
text(s,"CONTINUE",700,335,220,34,20,coral,true); text(s,"Move forward only after the current check passes",700,378,470,80,26,ink,true);
text(s,"Complete the guided practices and at least one challenge before the break.",90,570,1090,48,24,navy,true,"Aptos","center");

s=base("Notebook 2: Friendly Character Classes","A second guided notebook before the technology investigation");
bullets(s,["Read the blueprint and object explanation","Run the working Player example","Complete the Character constructor","Add one method that changes an object","Check that two objects keep separate values","Attempt the PowerUp boss only if time permits"],90,142,1090,24,76);

s=base("Break","10 minutes");
text(s,"Step away from the screen. Return at 10:35.",140,270,1000,70,34,navy,true,"Aptos","center");

s=base("Break and group setup","11:20 to 11:30");
text(s,"Form a group of 2 or 3. Open the Tech Investigation notebook.",140,245,1000,70,32,navy,true,"Aptos","center");
text(s,"Choose one topic together. You may divide the work in any way.",140,345,1000,60,26,muted,false,"Aptos","center");

s=base("Technology behind the screen","Common products raise questions about money, power, privacy, and safety");
bullets(s,["A free app can earn money from advertising","A subscription earns recurring revenue","An app store can charge fees on digital purchases","Design choices can influence user decisions","Market power can make competition difficult","Engineers help create the systems behind these choices"],90,142,1090,24,76);

s=base("Legal language","Use precise words during the discussion");
text(s,"ALLEGATION",90,155,260,34,20,teal,true); text(s,"A claim that has not yet been proven in court",90,198,470,70,26,ink,true);
text(s,"RULING",90,335,260,34,20,teal,true); text(s,"A court's decision on a legal question",90,378,470,70,26,ink,true);
text(s,"SETTLEMENT",700,155,260,34,20,coral,true); text(s,"The parties resolve a case without completing a trial",700,198,470,80,26,ink,true);
text(s,"BUSINESS MODEL",700,335,300,34,20,coral,true); text(s,"How a company earns revenue",700,378,470,70,26,ink,true);
text(s,"Do not describe an allegation as a proven fact.",90,570,1090,48,24,navy,true,"Aptos","center");

s=base("Investigation topics","Choose one topic from the notebook");
text(s,"TIKTOK",90,160,220,34,20,teal,true); text(s,"Advertising and children's privacy",90,198,450,60,24,ink,true);
text(s,"GOOGLE",90,310,220,34,20,teal,true); text(s,"Search advertising and competition",90,348,450,60,24,ink,true);
text(s,"INSTAGRAM",90,460,220,34,20,teal,true); text(s,"Advertising and youth well-being",90,498,450,60,24,ink,true);
text(s,"AMAZON",700,160,220,34,20,coral,true); text(s,"Prime subscriptions and dark patterns",700,198,450,60,24,ink,true);
text(s,"APPLE",700,310,220,34,20,coral,true); text(s,"The App Store and smartphone control",700,348,450,60,24,ink,true);
text(s,"GENERATIVE AI",700,460,260,34,20,coral,true); text(s,"Training data and human creators",700,498,450,60,24,ink,true);

s=base("Research organizer","Complete one shared evidence note");
bullets(s,["Explain how the product makes money","Build a short timeline of what happened","Label claims as allegations, rulings, or settlements","Name at least two groups affected","Record two facts with source links","Recommend one next step and explain a tradeoff"],90,142,1090,24,76);

s=base("Source path","Begin with the explainer; legal documents are optional");
bullets(s,["Read the AP, PBS NewsHour, or Reuters article first","Use it to understand the people, events, and disagreement","Open a legal document only when you want more detail","Check whether the case ended or remains open","Compare the government claim with the company response","Do not sign in or share private account information"],90,142,1090,24,76);

s=base("Share-out and discussion","Each group has two minutes");
bullets(s,["Name the product and its business model","Explain the controversy accurately","Share the strongest evidence you found","Ask the class one question","Listen for a tradeoff or missing viewpoint","Disagree with ideas without attacking people"],90,142,1090,24,76);

s=base("Individual exit ticket","Finish privately before 1:00 PM");
bullets(s,["Which business model surprised you most?","What fact can you verify with a reliable source?","What question do you still have?","What should engineers consider besides whether a product works?"],100,165,1080,26,96);
text(s,"Save your programming and investigation notebooks in Google Drive.",100,605,1080,42,23,blue,true,"Aptos","center");

for(let i=0;i<deck.slides.items.length;i++){
  const slide=deck.slides.items[i];
  const blob=await deck.export({slide,format:"png",scale:1});
  await fs.writeFile(path.join(buildDir,`slide-${String(i+1).padStart(2,"0")}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const montage=await deck.export({format:"webp",montage:true});
await fs.writeFile(path.join(buildDir,"montage.webp"),new Uint8Array(await montage.arrayBuffer()));

const {finalizePresentation}=await import(pathToFileURL(path.join(skillDir,"container_tools","artifact_tool_utils.mjs")).href);
const candidate=path.join(buildDir,"candidate.pptx");
await (await PresentationFile.exportPptx(deck)).save(candidate);
await finalizePresentation({
  explicitTotalSlideCount:16,
  requiredNativeTableOwnerSlides:[],
  requiredNativeChartOwnerSlides:[],
  workspaceDir,
  candidatePath:candidate,
  finalPath,
  pythonExecutable:python,
  integrityValidatorPath:path.join(skillDir,"container_tools","inspect_presentation_package_integrity.py"),
  layoutValidatorPath:path.join(skillDir,"container_tools","inspect_presentation_layout_geometry.py"),
  layoutArgs:["--expected-slide-size-emu","12192000,6858000","--validate-heading-fit"],
  fontPolicy:{basis:"design",families:["Aptos"]},
  verifyArtifactToolImport:true,
  receiptPath:path.join(buildDir,"validation-v7.json"),
});
console.log(finalPath);
