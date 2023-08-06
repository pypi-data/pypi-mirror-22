# -*- coding: utf-8 -*-
import json
import os

from django.test import TestCase

from opaque_keys.edx.locator import CourseLocator, BlockUsageLocator

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class JsonPayloadTestCase(TestCase):

    def setUp(self):
        # Grab an example payload and make it available to test
        # methods as a raw string and as a JSON dictionary.
        payload_file = os.path.join(os.path.dirname(__file__),
                                    'post.json')
        self.raw_payload = open(payload_file, 'r').read()
        self.json_payload = json.loads(self.raw_payload)


class MockCourseTestCase(TestCase):

    def setUp(self):
        # Set up a mock course
        course_id_string = 'course-v1:org+course+run1'
        cl = CourseLocator.from_string(course_id_string)
        bul = BlockUsageLocator(cl, u'course', u'course')
        course = Mock()
        course.id = cl
        course.system = Mock()
        course.scope_ids = Mock()
        course.scope_id.user_id = None
        course.scope_ids.block_type = u'course'
        course.scope_ids.def_id = bul
        course.scope_ids.usage_id = bul
        course.location = bul
        course.display_name = u'Course - Run 1'

        self.course_id_string = course_id_string
        self.cl = cl
        self.course = course

        email_params = {'registration_url': u'https://localhost:8000/register',  # noqa: E501
                        'course_about_url': u'https://localhost:8000/courses/course-v1:org+course+run1/about',  # noqa: E501
                        'site_name': 'localhost:8000',
                        'course': course,
                        'is_shib_course': None,
                        'display_name': u'Course - Run 1',
                        'auto_enroll': True,
                        'course_url': u'https://localhost:8000/courses/course-v1:org+course+run1/'}  # noqa: E501
        self.email_params = email_params
