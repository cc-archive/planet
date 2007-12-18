#!/usr/bin/env ipython

import unittest, glob, os, shutil
from planet import spider, splice, config
import xml.dom.minidom

workdir = 'tests/work/cc_license'
spider_workdir = 'tests/work/spider/cache'
configfile = 'tests/data/config-%s.ini'


class CCLicenseTest(unittest.TestCase):
    def setUp(self):
        config.load(configfile % 'cc_license')

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
    # okay and ultimately shows up in the feed.  This is also an indirect test
    # of whether the patch to tmpl.py is working.  Second, it tests whether the
    # cc_license.plugin plugin is correctly fetching data from the CC API.  The
    # text "Attribution-Noncommercial-Share Alike 2.5 Colombia" is what the CC
    # API should return for the license URL
    # http://creativecommons.org/licenses/by-nc-sa/2.5/co/, which is set as the
    # default license for configured feed [tests/data/spider/testfeed1a.atom]
    def test_cc_default_license_lookup(self):
        config.load(configfile % 'cc_license')
        for testfeed in testfeeds:
            doc = splice.splice()
            splice.apply(doc.toxml('utf-8'))
        output = open(os.path.join(workdir, 'index.html')).read()
        self.assertTrue('Attribution-Noncommercial-Share Alike 2.5 Colombia' in output)

    # This test uses another one of the static test feeds that came with the
    # default install of Planet Venus.  It has two main purposes.  One is to
    # test whether the default_license configuration option for a blog is
    # working okay and ultimately shows up in the feed.  This is also an
    # indirect test of whether the patch to tmpl.py is working.  Second, it
    # tests whether the cc_license.plugin plugin is will correctly LEAVE ALONE
    # a default_license definition that is NOT a CC license.  The vanilla text
    # 'title="License information">License</a>' is what the patch to tmpl.py
    # inserts, and this should remain unchanged in the index.html file.
    # The test feed is [tests/data/spider/testfeed2.atom]
    def test_non_cc_default_license(self):
        config.load(configfile % 'cc_license')
        for testfeed in testfeeds:
            doc = splice.splice()
            splice.apply(doc.toxml('utf-8'))
        output = open(os.path.join(workdir, 'index.html')).read()
        self.assertTrue('title="License information">License</a>' in output)

    # This test uses a real URL and the config has no default_license
    # specified, and is therefore a test of whether the patch is correctly
    # pulling embedded license data from a feed, also yet another test to make
    # sure that the plugin is correctly looking up license data at the CC API.
    # The configured URL is 'http://techblog.creativecommons.org/feed'.  The CC
    # Techblog is license under 'Attribution 3.0 Unported' and so this text
    # should show up in index.html
    def test_embedded_license(self):
        config.load(configfile % 'cc_license')
        for testfeed in testfeeds:
            doc = splice.splice()
            splice.apply(doc.toxml('utf-8'))
        output = open(os.path.join(workdir, 'index.html')).read()
        self.assertTrue('Attribution 3.0 Unported' in output)
