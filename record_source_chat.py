"""Record actual terminal I/O from the supplied chat.py as an asciicast v2 file."""
import json,os,pty,select,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
os.chdir(root)
out=root/'source_evidence'
out.mkdir(exist_ok=True)
master,slave=pty.openpty()
process=subprocess.Popen([sys.executable,'chat.py','--model','llm_runs/source_expanded/model.pt','--transcript','source_evidence/chat_transcript.json'],stdin=slave,stdout=slave,stderr=slave,close_fds=True)
os.close(slave)
start=time.monotonic();events=[];raw='';seen='';prompts=iter(['the customer','a cat','explain quantum teleportation','/quit'])
while True:
 ready,_,_=select.select([master],[],[],1)
 if ready:
  try: data=os.read(master,65536)
  except OSError: break
  if not data: break
  text=data.decode('utf-8',errors='replace');events.append([round(time.monotonic()-start,6),'o',text]);raw+=text;seen+=text
  if seen.endswith('You: '):
   prompt=next(prompts,None)
   if prompt is not None:
    os.write(master,(prompt+'\n').encode());seen=''
 elif process.poll() is not None:break
process.wait();os.close(master)
if process.returncode:raise SystemExit(process.returncode)
(out/'chat.cast').write_text('\n'.join([json.dumps({'version':2,'width':110,'height':30,'timestamp':int(time.time()),'title':'Actual independently sourced expanded 3000-step nanoGPT terminal session'})]+[json.dumps(e) for e in events])+'\n')
(out/'chat_terminal.txt').write_text(raw)
print(raw)
