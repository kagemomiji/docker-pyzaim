import unittest
import os

from tests.util import env
from pyzaim.exception import *

from pyzaim import OauthInitializer

class TestOauthInitializer(unittest.TestCase):
    def test_init(self):

        # reset environment value
        old_env = env.save()
        env.reset()

        # assert Exception of no consumer id
        with self.assertRaises(NoConsumerIDException):
            oinit = OauthInitializer()
        # set consumer id
        os.environ['CONSUMER_ID'] = "testid"
        # assert Exception of no consumer secret
        with self.assertRaises(NoConsumerSecretException):
            oinit = OauthInitializer()

        # set all env
        env.recover(old_env)

        # initialize
        oinit = OauthInitializer()

        # assert menber field
        self.assertEqual(oinit.get_consumer_id() , os.getenv("CONSUMER_ID"))
        self.assertEqual(oinit.get_consumer_secret() , os.getenv("CONSUMER_SECRET"))

    
    def test_get_authentication_token(self):

        # initialize oauth initializer
        osinit = OauthInitializer()

        osinit.authentication()

        self.assertLessEqual(50,len(osinit.get_oauth_verifier()))
        self.assertLessEqual(50,len(osinit.get_access_token()))
        self.assertLessEqual(50,len(osinit.get_access_token_secret()))



if __name__ == '__main__':
    unittest.main()