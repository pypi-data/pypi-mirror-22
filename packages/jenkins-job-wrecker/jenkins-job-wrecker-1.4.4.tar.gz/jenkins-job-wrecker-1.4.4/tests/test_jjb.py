# -*- coding: utf-8 -*-
from jenkins_job_wrecker.cli import get_xml_root, root_to_yaml
import os
import tempfile
import jenkins_jobs.cmd

fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestJJB(object):

    def run_jjb(self, name, jobname=None):
        filename = os.path.join(fixtures_path, name + '.xml')
        root = get_xml_root(filename=filename)
        if jobname is None:
            jobname = name
        yaml = root_to_yaml(root, jobname)

        # Run this wrecker YAML thru JJB.
        temp = tempfile.NamedTemporaryFile()
        temp.write(yaml)
        temp.flush()
        assert jenkins_jobs.cmd.main(['test', temp.name]) is None
        temp.close()

    def test_ice_setup(self):
        self.run_jjb('ice-setup')

    def test_calamari_clients(self):
        self.run_jjb('calamari-clients')

    def test_non_ascii(self):
        self.run_jjb('non-ascii', 'テスト')
