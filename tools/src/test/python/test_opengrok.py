#!/usr/bin/env python3

#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# See LICENSE.txt included in this distribution for the specific
# language governing permissions and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at LICENSE.txt.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright (c) 2021, Oracle and/or its affiliates. All rights reserved.
#

import logging

from inspect import getmembers, isfunction, signature
from opengrok_tools.utils import opengrok


def test_headers_timout(monkeypatch):
    """
    Test that all functions in the opengrok module propagate the timeout and
    HTTP headers to do_api_call().
    """
    headers_expected = {'foo': 'bar'}
    timeout_expected = 42

    def mock_response(ri, verb, headers, data, timeout):
        assert headers == headers_expected
        assert timeout == timeout_expected

    logger = logging.getLogger("test_headers_timeout")

    for func in getmembers(opengrok, isfunction):
        f = func[1]
        with monkeypatch.context() as m:
            m.setattr("opengrok_tools.utils.restful.do_api_call",
                      mock_response)
            if len(signature(f).parameters) == 5:
                f(logger, "data", "http://localhost:8080/source/api/v1/bah",
                  headers=headers_expected, timeout=timeout_expected)
            elif len(signature(f).parameters) == 4:
                f(logger, "http://localhost:8080/source/api/v1/bah",
                  headers=headers_expected, timeout=timeout_expected)
