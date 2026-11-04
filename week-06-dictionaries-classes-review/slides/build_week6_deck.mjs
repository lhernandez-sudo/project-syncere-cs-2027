import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = process.cwd();
const buildDir = path.join(workspaceDir, ".codex-build", "week6-slides");
const outputDir = path.join(workspaceDir, "week-06-dictionaries-classes-review", "slides");
const finalPath = path.join(outputDir, "week-06-dictionaries-classes-review-v3.pptx");
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
text(s,"Final Foundations Review",72,145,1100,82,52,white,true);
text(s,"Dictionaries and friendly classes",76,242,1050,48,30,"#B8D7F0");
text(s,"Week 6 self-guided Colab session",76,584,1080,36,21,"#D9E8F5");

s=base("Self-guided day","Follow the slides and notebooks in order");
bullets(s,["Keep an individual Google Drive copy of every notebook","Complete your own work; neighbor checks are optional","Read every instruction before running a cell","Treat failed checks as clues","Ask the program assistant for account or safety help","Finish the exit ticket before 1:00 PM"],86,142,1100,23,76);

s=base("Today’s schedule","The class still includes two ten-minute breaks");
bullets(s,["9:00–9:15  Arrive, sign in, and open Week 6","9:15–9:35  Secret Identity Generator icebreaker","9:35–10:25  Notebook 1: Dictionary Arcade","10:25–10:35  Break","10:35–11:20  Finish the dictionary boss","11:20–11:30  Break","11:30–12:15  Notebook 2: Friendly Character Classes","12:15–12:40  Notebook 3: Data Model Showdown","12:40–1:00  Final self-test and exit ticket"],72,126,1140,18,55);

s=base("Google Colab setup","Open notebooks from the Week 6 README");
bullets(s,["Sign into the Google account used for class","Open the current notebook from GitHub","Choose File, then Save a copy in Drive","Rename the copy with your name and notebook number","Work only in the saved copy","Return to the README when the notebook says Finish"],88,142,1090,24,76);

s=base("Icebreaker: Secret Identity Generator","Individual and private, about 20 minutes");
bullets(s,["Run the generator to get a random draft","Reroll until a combination makes you laugh","Customize your alias, power, snack, and weakness","Run the check and repair any unfinished value","Save your identity card in your Drive copy","Sharing with one person is optional"],90,142,1090,24,76,coral);

s=base("Work style today","Independent first; optional help second");
text(s,"1  ATTEMPT",90,155,280,34,20,teal,true); text(s,"Read, predict, and try the task yourself",90,198,470,70,26,ink,true);
text(s,"2  CHECK",90,335,280,34,20,teal,true); text(s,"Run the cell and read every message",90,378,470,70,26,ink,true);
text(s,"3  REPAIR",700,155,280,34,20,coral,true); text(s,"Fix one small issue and run it again",700,198,470,70,26,ink,true);
text(s,"4  OPTIONAL HELP",700,335,320,34,20,coral,true); text(s,"After one repair, quietly compare with a neighbor",700,378,470,80,26,ink,true);
text(s,"No assigned roles, public voting, or required sharing.",90,570,1090,48,24,navy,true,"Aptos","center");

s=base("Dictionary quick reference","A dictionary stores labeled values");
codeBlock(s,'player = {\n    "name": "Ari",\n    "score": 12\n}\n\nplayer["score"] = 15\ncity = player.get("city", "unknown")',72,160,650,390);
text(s,"Use dictionaries for",790,170,350,38,24,teal,true);
text(s,"one profile or record\n\nsettings and configuration\n\ninventory counts\n\ndata returned by an API",790,225,360,290,25,ink,false);

s=base("Notebook 1: Dictionary Arcade","Complete the cells in order");
bullets(s,["Repair the game inventory","Use .get() for optional keys","Loop through key-value pairs with .items()","Build an event record","Complete the snack order functions","Stop only when every integrity check passes"],90,142,1090,24,76);

s=base("Break","10 minutes");
text(s,"Step away from the screen. Return at 10:35.",140,270,1000,70,34,navy,true,"Aptos","center");

s=base("Dictionary boss","One dictionary stores quantities; another stores prices");
codeBlock(s,'prices = {"chips": 2, "juice": 3}\norder = {"chips": 2, "juice": 1}\n\ndef order_total(order_data, price_data):\n    total = 0\n    # loop through the order\n    return total',72,165,720,390);
text(s,"Before editing",850,175,300,38,24,coral,true);
text(s,"Trace one item by hand.\n\nName the key.\n\nName the quantity.\n\nFind the matching price.\n\nMultiply, then accumulate.",850,230,330,300,24,ink,false);

s=base("Break","10 minutes");
text(s,"Reset before classes and objects. Return at 11:30.",140,270,1000,70,34,navy,true,"Aptos","center");

s=base("Class quick reference","A class defines shared data and actions");
codeBlock(s,'class Player:\n    def __init__(self, name):\n        self.name = name\n        self.score = 0\n\n    def earn(self, points):\n        self.score += points',72,160,720,390);
text(s,"Read it this way",850,170,300,38,24,teal,true);
text(s,"Player is the blueprint.\n\nself means this object.\n\nname and score are attributes.\n\nearn is a method.",850,225,330,280,25,ink,false);

s=base("Notebook 2: Friendly Character Classes","Keep the class small and readable");
bullets(s,["Store constructor arguments on self","Create two independent objects","Add methods that update state","Return a useful status string","Build reusable PowerUp objects","Use the checks with multiple objects"],90,142,1090,24,76);

s=base("Notebook 3: Data Model Showdown","Use both structures in one small system");
text(s,"DICTIONARY",90,160,260,34,20,teal,true); text(s,"One club profile with labeled fields",90,202,470,68,27,ink,true);
text(s,"CLASS",90,345,260,34,20,teal,true); text(s,"Many players with shared methods and separate points",90,387,500,82,27,ink,true);
text(s,"FINAL REPORT",700,160,260,34,20,coral,true); text(s,"A dictionary created from the club record and Player objects",700,202,470,90,27,ink,true);
text(s,"The final checks use different test data. Hard-coded answers will fail.",700,390,470,72,25,coral,true);

s=base("Final self-test","12:40 PM");
bullets(s,["Run your own completed final challenge","Create one new test object","Give it a different name and point value","Confirm the output uses the new values","Repair any issue you discover","Add a Markdown note describing the test"],90,142,1090,24,76);

s=base("Exit ticket","Finish before 1:00 PM");
bullets(s,["What problem does a dictionary solve?","When is .get() useful?","What is the difference between a class and an object?","Why should two objects keep separate state?","Which structure could help your capstone?"],100,155,1080,26,88);
text(s,"Save all four notebooks in Google Drive before leaving.",100,605,1080,42,23,blue,true,"Aptos","center");

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
  receiptPath:path.join(buildDir,"validation-v3.json"),
});
console.log(finalPath);
