import os, tempfile, unittest
from pathlib import Path
os.environ['DOMUSOS_DB'] = str(Path(tempfile.gettempdir()) / 'domusos_test_suite.sqlite3')
from app import app, init_db
class DomusApiTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): init_db()
 def setUp(self):
  self.client=app.test_client()
  with app.app_context():
   from app import db
   db().execute("DELETE FROM users WHERE email LIKE 'test%@example.com'")
   db().commit()
 def test_health(self): self.assertEqual(self.client.get('/api/health').status_code,200)
 def test_register_login_and_state(self):
  r=self.client.post('/api/register',json={'name':'Test User','email':'test1@example.com','password':'password123'}); self.assertEqual(r.status_code,201)
  self.assertEqual(self.client.get('/api/me').json['user']['email'],'test1@example.com')
  self.assertEqual(self.client.put('/api/state',json={'state':{'demo':True}}).status_code,200)
  self.assertEqual(self.client.get('/api/state').json['state']['demo'],True)
  self.client.post('/api/logout',json={})
  self.assertEqual(self.client.get('/api/state').status_code,401)
  self.assertEqual(self.client.post('/api/login',json={'email':'test1@example.com','password':'password123'}).status_code,200)
 def test_validation_and_duplicate(self):
  self.assertEqual(self.client.post('/api/register',json={'name':'A','email':'bad','password':'123'}).status_code,400)
  self.client.post('/api/register',json={'name':'Test User','email':'test2@example.com','password':'password123'})
  self.assertEqual(self.client.post('/api/register',json={'name':'Test User','email':'test2@example.com','password':'password123'}).status_code,409)
if __name__=='__main__': unittest.main()
