#
# from coverage import coverage
# #
#
# cov = coverage(branch=True,
#                omit=['config/*', 'venv/*', '*/__init__.py','manager.py', 'hims_server/customlib/*', 'tests/*', '__init__.py'],
#                concurrency='eventlet')
# # concurrency is a string indicating the concurrency library being used in the measured code. Without this, coverage.py will get incorrect results if these libraries are in use. Valid strings are “greenlet”, “eventlet”, “gevent”, “multiprocessing”, or “thread” (the default). This can also be a list of these strings.
#
# cov.start()
#
# import os
# from hims_server.hims_app import log
# import unittest
#
# log.info('start testing')

from tests.unittest.host.test_auth import AuthTestCase
from tests.unittest.guest.test_attraction import AttractionTestCase
from tests.unittest.guest.test_faq import FAQTestCase
from tests.unittest.guest.test_hotel_info import HotelInfoTestCase
from tests.unittest.guest.test_phone import PhoneTestCase
from tests.unittest.guest.test_guest_requirement import GuestRequirementTestCase
from tests.unittest.host.test_requirement import RequirementTestCase
from tests.unittest.guest.test_service import ServiceTestCase

from tests.unittest.host.test_chat import ChatTestCase


#
# test_classes_to_run = [ChatTestCase] #GuestRequirementTestCase, AuthTestCase, AttractionTestCase, FAQTestCase, HotelInfoTestCase, PhoneTestCase]
# loader = unittest.TestLoader()
#
# suites_list = []
# for test_class in test_classes_to_run:
#     suite = loader.loadTestsFromTestCase(test_class)
#     suites_list.append(suite)
#
# big_suite = unittest.TestSuite(suites_list)
#
# runner = unittest.TextTestRunner()
# results = runner.run(big_suite)
#
# log.info('end testing')
#
#
# cov.stop()
# cov.save()
# # print("\n\nCoverage Report:\n")
# cov.report()
#
# # time.sleep(3)
# os._exit(0)