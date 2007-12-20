#!/usr/bin/env ipython

import unittest, glob, os, shutil
from planet import spider, splice, config
import xml.dom.minidom

workdir = 'tests/work/get_license_name'
spider_workdir = 'tests/work/spider/cache'
configfile = 'tests/data/config/get_license_name.ini'


class GetLicenseNameTest(unittest.TestCase):
    def setUp(self):
        config.load(configfile)

        # Re fetch and/or parse the test feeds
        spider.spiderPlanet()
        global testfeeds
        testfeeds = glob.glob(spider_workdir+"/*")

        try:
            os.makedirs(workdir)
        except:
            self.tearDown()
            os.makedirs(workdir)

    def tearDown(self):
        shutil.rmtree(os.path.split(workdir)[0])

    # This test uses one of the static test feeds that came with the default
    # install of Planet Venus.  It has two main purposes.  One is to test
    # whether the default_license configuration option for a blog is working
    # okay and ultimately shows up in the cached feed.  This is also an
    # indirect test of whether the patch to tmpl.py is working.  Second, it
    # tests whether the get_license_name.plugin plugin is correctly fetching
    # the license name. The text "Attribution-Noncommercial-Share Alike 2.5
    # Colombia" is what the CC API should return for the license URL
    # http://creativecommons.org/licenses/by-nc-sa/2.5/co/, which is set as the
    # default_license for configured feed [tests/data/spider/testfeed1a.atom]
    def test_default_license_lookup(self):
        config.load(configfile)
        expected_text = 'Reconocimiento-No comercial-Compartir bajo la' + \
            ' misma licencia 2.5 Colombia'
        for testfeed in testfeeds:
            doc = splice.splice()
            splice.apply(doc.toxml('utf-8'))
        output = open(os.path.join(workdir, 'index.html')).read()
        self.assertTrue(expected_text in output)

    # This test uses another one of the static test feeds that came with the
    # default install of Planet Venus.  It has two main purposes.  One is to
    # test whether the default_license configuration option for a blog is
    # working okay and ultimately shows up in the feed.  This is also an
    # indirect test of whether the patch to tmpl.py is working.  Second, it
    # tests whether the get_license_name.plugin is will correctly and leaves
    # alone a default_license definition that isn't actually a valid license
    # URL.  The vanilla text 'title="License information">License</a>' is what
    # the patch to tmpl.py (and the plugin itself) inserts, and this should
    # remain unchanged in the index.html file.
    # The test feed is [tests/data/spider/testfeed2.atom]
    def test_invalid_default_license(self):
        config.load(configfile)
        for testfeed in testfeeds:
            doc = splice.splice()
            splice.apply(doc.toxml('utf-8'))
        output = open(os.path.join(workdir, 'index.html')).read()
        self.assertTrue('title="License information">License</a>' in output)

    # This test uses a real URL and the config has no default_license
    # specified, and is therefore a test of whether the patch is correctly
    # pulling embedded license data from a feed and also a test to make sure
    # that the plugin is correctly identifying the license name.  The
    # configured URL is 'http://techblog.creativecommons.org/feed'.  The CC
    # Techblog is license under 'Attribution 3.0 Unported' and so this text
    # should show up in index.html
    def test_embedded_license(self):
        config.load(configfile)
        for testfeed in testfeeds:
            doc = splice.splice()
            splice.apply(doc.toxml('utf-8'))
        output = open(os.path.join(workdir, 'index.html')).read()
        self.assertTrue('Attribution 3.0 Unported' in output)
