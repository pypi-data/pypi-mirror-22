# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from collections import namedtuple

import suds.client
import suds.wsse

DEFAULT_STUDENT_SERVICE_WSDL_URL = 'http://service.integration.it.liu.se/StudentService/2.0/StudentService.svc?singleWsdl'
DEFAULT_STUDENT_SERVICE_PORT = 'BasicHttpBinding_IStudentService'

EXCLUDED_SECTION_CODES = (
    # These student union codes are not considered to be sections and are thus
    # not passed on to the Student object.

    # Legacy membership codes
    'LI10',
    'LI12',
    'LI20',
    'LI21',
    'LI22',
    'LI30',
    'LI40',
    'LI41',
    'LI42',
    'LI50',
    'LI51',
    'LI52',
    'LI80',
    'LI90',

    # Union membership only
    'Cons',  # Consensus
    'LinT',  # LinTek
    'StuF',  # StuFF

    # Independent courses
    'Fri',  # Consensus
    'FriL',  # LinTek
    'FriS',  # StuFF

    # Support membership
    'Stöd',  # Consensus
    'StöL',  # LinTek
    'StöF',  # StuFF
)

NOT_FOUND_MESSAGE = 'Could not find Student in database'

# Using a namedtuple gives us immutability and a more defined API for Sesam's
# results than using a plain dict. Still it offers an easy way of mocking
# responses for testing.
SesamStudent = namedtuple('SesamStudent', (
    'liu_id',
    'name',
    'union',
    'section_code',
    'nor_edu_person_lin',
    'liu_lin',
    'email'
))


class SesamError(Exception):
    def __init__(self, original_exception=None, *args, **kwargs):
        super(SesamError, self).__init__(*args, **kwargs)

        self.original_exception = original_exception


class SesamStudentNotFound(SesamError):
    def __str__(self):
        return 'Student not found'


class SesamStudentServiceClient(suds.client.Client):
    def __init__(self, username, password,
                 url=DEFAULT_STUDENT_SERVICE_WSDL_URL,
                 port=DEFAULT_STUDENT_SERVICE_PORT, **kwargs):
        wsse = suds.wsse.Security()
        wsse.tokens.append(
            suds.wsse.UsernameToken(username, password)
        )

        super(SesamStudentServiceClient, self).__init__(
            url=url,
            port=port,
            wsse=wsse,
            **kwargs
        )

    def get_student(self, nor_edu_person_lin=None, liu_id=None, mifare_id=None,
                    national_id=None, iso_id=None):
        # Removes leading zeros from card numbers
        if iso_id:
            iso_id = str(iso_id).lstrip('0')
        if mifare_id:
            mifare_id = str(mifare_id).lstrip('0')

        request = self.factory.create('ns2:GetStudentRequest')

        request.Identity.IsoNumber = iso_id
        request.Identity.LiUId = liu_id
        request.Identity.MifareNumber = mifare_id
        request.Identity.norEduPersonLIN = nor_edu_person_lin
        request.Identity.norEduPersonNIN = national_id

        try:
            data = self.service.GetStudent(request).Student
        except suds.WebFault as exception:
            if NOT_FOUND_MESSAGE in exception.fault.faultstring:
                raise SesamStudentNotFound(exception)
            raise SesamError(exception)

        return SesamStudent(
            liu_id=str(data.LiUId),
            name=str(data.DisplayName),
            union=str(data.MainUnion) if data.MainUnion else None,
            # This abstraction is a bit ugly. It returns the raw codes from
            # Sesam but not in every case.
            # todo: look for a better abstraction for section_code.
            section_code=str(data.StudentUnion) if (
                data.StudentUnion and
                data.StudentUnion not in EXCLUDED_SECTION_CODES
            ) else None,
            email=str(data.EmailAddress),
            nor_edu_person_lin=uuid.UUID(data.norEduPersonLIN),
            liu_lin=uuid.UUID(data.LiULIN)
        )
