import importlib.util, json, threading, unittest, urllib.request, urllib.error
from pathlib import Path
spec=importlib.util.spec_from_file_location('app',Path(__file__).resolve().parents[1]/'server.py');app=importlib.util.module_from_spec(spec);spec.loader.exec_module(app)
class Classroom(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=app.ThreadingHTTPServer(('127.0.0.1',0),app.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.base=f'http://127.0.0.1:{cls.server.server_port}'
 @classmethod
 def tearDownClass(cls): cls.server.shutdown();cls.server.server_close()
 def call(self,path,body=None,teacher=False):
  req=urllib.request.Request(self.base+path,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json',**({'Authorization':'Bearer '+app.TOKEN} if teacher else {})})
  try:
   with urllib.request.urlopen(req) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 def test_classroom_flow(self):
  for path in ['/api/reset','/api/generate','/api/publish','/api/revise','/api/reveal']:
   self.assertEqual(self.call(path,{},False)[0],403)
  self.assertEqual(self.call('/api/private')[0],403)
  for case in app.CASES:
   status,draft=self.call('/api/generate',{'claim':case['claim']},True);self.assertEqual(status,200)
   self.assertEqual(self.call('/api/state')[1]['claim'],'')
   self.call('/api/publish',{},True)
   student=self.call('/api/state')[1];self.assertEqual(student['claim'],case['claim']);self.assertNotIn('guide',student);self.assertNotIn('error',student['proof'])
   self.call('/api/revise',{'counter':case['counter'],'claim':case['repair']},True)
   self.assertEqual(len(self.call('/api/state')[1]['history']),1)
   self.call('/api/reveal',{},True);self.assertEqual(self.call('/api/state')[1]['guide']['error'],case['error'])
   self.call('/api/reset',{},True);self.assertIsNone(self.call('/api/state')[1]['proof']);self.assertNotIn('guide',self.call('/api/state')[1])
  self.assertEqual(self.call('/api/generate',{'claim':'의미가 다른 자유 추측'},True)[0],400)
if __name__=='__main__':unittest.main()
