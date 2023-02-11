import unittest
import json
from sqlalchemy import func
from flaskr import create_app
from flask import Flask, current_app
from config import TestingConfig
from flaskr.models import Composer


class ComposerTestCase(unittest.TestCase):
    """Configure database connection"""

    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client

        self.new_composer = {
            "name": "Johann Sebastian Bach",
            "years": [1685, 1750],
            "nationality": "Germany"
        }
        # with self.app.app_context():
        #     assert current_app == self.app
        #     self.db.create_all()
        with self.app.app_context():
            assert current_app == self.app
            
            composer = Composer(
                name="Wolfgang Amadeus Mozart",
                years=[1756, 1791],
                nationality="Austria"
            )

            composer.insert()

            self.del_id = Composer.query.all()[0].id

    def tearDown(self):
        with self.app.app_context():
            # print(f"tear down {Composer.query.all()[0].id}")
            if Composer.query.all()[0].id:
                res = self.client().delete("/composers/"+str(Composer.query.all()[0].id))

    def test_create_composer(self):
        """ Test add new composer"""
        res = self.client().post("/composers/create", json=self.new_composer)
        print(f"CREATE COMPOSER data {res.data}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["composers"]))

    def test_get_composer(self):
        """ Test retrieve composer"""
        res = self.client().get("/composers")
        data = json.loads(res.data)
        print(f"GET COMPOSER data {data}")
        self.assertEqual(res.status_code, 200, msg='{0}'.format({res}))
        self.assertTrue(len(data['composers']))

    def test_get_composer_by_id(self):
        res = self.client().get(f"/composers/{self.del_id}")
        data = json.loads(res.data)

        print(f"GET BY ID data {data}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_composer(self):
        """ Test delete question """
        res = self.client().delete("/composers/"+str(self.del_id))
        data = json.loads(res.data)
        print(f"DELETE COMPOSER {data}")
        self.assertEqual(res.status_code, 200, msg='{0}'.format(res))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])
        
class PerformerTestCase(unittest.TestCase):
     def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client

        self.new_performer = {
            "name": "Glen Gould",
            "years": [1932, 1982],
            "nationality": "Canadian"
        }
        # with self.app.app_context():
        #     assert current_app == self.app
        #     self.db.create_all()
        with self.app.app_context():
            assert current_app == self.app
            
            composer = Composer(
                name="Wolfgang Amadeus Mozart",
                years=[1756, 1791],
                nationality="Austria"
            )

            composer.insert()

            self.del_id = Composer.query.all()[0].id

    def test_create_performer(self):
        res = self.client().post("/performers/create", json=self.new_composer)
        data = json.loads(res.data)
        
        
        


if __name__ == "__main__":
    unittest.main()
