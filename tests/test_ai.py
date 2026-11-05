import importlib.util, io, json, os, unittest, urllib.error
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('ai_app',Path(__file__).resolve().parents[1]/'server.py');app=importlib.util.module_from_spec(spec);spec.loader.exec_module(app)
class Gemini(unittest.TestCase):
 def test_gemini_request_and_response(self):
  result={k:'検証用' for k in ['error','counter','repair','monster','exception','lemma']};result['steps']=['段階1','段階2','段階3']
  response=io.BytesIO(json.dumps({'choices':[{'message':{'content':json.dumps(result)}}]}).encode())
  with patch.dict(os.environ,{'AI_PROVIDER':'gemini','GEMINI_API_KEY':'test-key','GEMINI_MODEL':'test-model'},clear=True),patch.object(app.urllib.request,'urlopen',return_value=response) as call:
   generated=app.generate('수업용 자유 추측')
   req=call.call_args.args[0]
   self.assertEqual(req.full_url,'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions')
   self.assertEqual(req.get_header('Authorization'),'Bearer test-key')
   self.assertEqual(json.loads(req.data)['model'],'test-model')
   self.assertEqual(generated['source'],'Gemini AI 초안 · 교사 검토 필요')
 def test_quota_error(self):
  error=urllib.error.HTTPError('https://example.test',429,'quota',{},None)
  with patch.dict(os.environ,{'AI_PROVIDER':'gemini','GEMINI_API_KEY':'test-key','GEMINI_MODEL':'test-model'},clear=True),patch.object(app.urllib.request,'urlopen',side_effect=error):
   with self.assertRaisesRegex(ValueError,'한도'):app.generate('다른 자유 추측')
 def test_missing_key(self):
  with patch.dict(os.environ,{'AI_PROVIDER':'gemini'},clear=True):
   with self.assertRaisesRegex(ValueError,'GEMINI_API_KEY'):app.generate('다른 자유 추측')
if __name__=='__main__':unittest.main()
