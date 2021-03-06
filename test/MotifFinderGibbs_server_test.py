# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from pprint import pprint

from MotifFinderGibbs.MotifFinderGibbsImpl import MotifFinderGibbs
from MotifFinderGibbs.MotifFinderGibbsServer import MethodContext
from MotifFinderGibbs.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class MotifFinderGibbsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('MotifFinderGibbs'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'MotifFinderGibbs',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = MotifFinderGibbs(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_MotifFinderGibbs_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_gibbs(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        params = {
            #'workspace_name': 'arwyer:narrative_1516985493280',
            'workspace_name': 'pranjan77:narrative_1517498855061',
            #'genome_ref': '27852/2/1',
            'genome_ref': '12566/5/3',
            #'featureSet_ref': '27852/3/1',
            'featureSet_ref': '12566/6/1',
            'promoter_length':100,
            'motif_min_length':8,
            'motif_max_length':16
        }

        result = self.getImpl().ExtractPromotersFromFeatureSetandDiscoverMotifs(self.getContext(),params)
        print('RESULT:')
        pprint(result)
        #ret = self.getImpl().run_MotifFinderGibbs(self.getContext(), {'workspace_name': self.getWsName(),
        #                                                            'parameter_1': 'Hello World!'})
