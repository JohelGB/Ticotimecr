import asyncio,os,sys,edge_tts
async def main(text,out,voice='es-CR-JuanNeural',rate='+8%'):
    c=edge_tts.Communicate(text,voice,rate=rate,proxy=os.environ.get('HTTPS_PROXY'))
    await c.save(out)
if __name__=='__main__': asyncio.run(main(sys.argv[1],sys.argv[2],*(sys.argv[3:])))
