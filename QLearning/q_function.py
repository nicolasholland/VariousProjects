from pymongo import MongoClient
import unittest
import numpy as np

class Q(object):

    def __init__(self, url='127.0.0.1:27017', default=0):
        self.client = MongoClient(url)
        self.db = self.client.qfunc
        self.default = default

    def update(self, state, action, value):
        if isinstance(state, np.ndarray):
            state = state.tostring()

        if isinstance(action, np.ndarray):
            action = action.tostring()

        entry = {
            'state' : state,
            'action' : action,
            'value' : value
        }
        old = self.db.qfunc.find_one({'state': state, 'action': action})
        if  old == None:
            self.db.qfunc.insert_one(entry)
        else:
            self.db.qfunc.update_one({'_id' : old['_id']},
                                     {'$set' : {'value': entry['value']}})

    def __call__(self, state, action):
        if isinstance(state, np.ndarray):
            state = state.tostring()

        if isinstance(action, np.ndarray):
            action = action.tostring()

        entry = self.db.qfunc.find_one({'state': state, 'action': action})

        if entry == None:
            return self.default

        return entry['value']

    def reset(self):
        self.db.qfunc.delete_many({})


class TestQ(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestQ, self).__init__(*args, **kwargs)
        self.q = Q()

    def test_init(self):
        status = self.q.db.command("serverStatus")

        self.assertTrue(status != None)

    def test_Q(self):
        self.q.update('aState', 'anAction', 5)
        val = self.q('aState', 'anAction')

        self.assertEqual(val, 5)

        self.q.update('aState', 'anAction', 8.2)
        val = self.q('aState', 'anAction')

        self.assertEqual(val, 8.2)

        self.q.db.qfunc.delete_one(dict(state='aState', action='anAction',
                                        value=8.2))


    def test_Q_numpy(self):
        state = np.array([0, 3, 2.5])
        action = np.array([2])

        self.q.update(state, action, 3)
        val = self.q(state, action)
        self.assertEqual(val, 3)

        self.q.db.qfunc.delete_one(dict(state=state.tostring(),
                                        action=action.tostring(),
                                        value=3))

if __name__ == '__main__':
    unittest.main()

