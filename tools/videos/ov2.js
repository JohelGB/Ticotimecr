const {chromium}=require('playwright');const [,,dataJson,outDir]=process.argv;(async()=>{const d=JSON.parse(dataJson);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/ov2.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.evaluate(x=>setData(x),d);
for(const id of ['brand','title','price','perks','cta']){await p.evaluate(i=>show(i),id);await p.screenshot({path:outDir+'/'+id+'.png',omitBackground:true});}
await p.evaluate(()=>show('tag'));await p.screenshot({path:outDir+'/tag.png',omitBackground:true,clip:{x:0,y:0,width:260,height:330}});await b.close()})();
