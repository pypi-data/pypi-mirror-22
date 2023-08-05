# -*- coding: utf-8 -*-

# MIT License
# 
# Copyright (c) 2017 Tijme Gommers
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from urllib.parse import urlparse

import copy

class HTTPRequestHelper:
    """A helper for the src.http.Request module."""

    @staticmethod
    def patch_with_options(request, options, parent_queue_item=None):
        """Patch the given request with the given options (e.g. user agent).

        Args:
            request (obj): The request to patch.
            options (obj): The options to patch the request with.
            parent_queue_item (obj): The parent queue item object (request/response pair) if exists.

        """

        request.headers = copy.deepcopy(options.identity.headers)
        request.cookies = copy.deepcopy(options.identity.cookies)

        if parent_queue_item != None:
            for cookie in parent_queue_item.request.cookies:
                request.cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)

            for cookie in parent_queue_item.response.cookies:
                request.cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)

    @staticmethod
    def complies_with_scope(queue_item, new_request, scope):
        """Check if the new request complies with the crawling scope.

        Args:
            queue_item (obj): The parent queue item of the new request.
            new_request (obj): The request to check.
            scope (obj): The scope to check.

        Returns:
            bool: True if it complies, False otherwise.

        """

        try:
            parsed_url = urlparse(queue_item.request.url)
            parsed_new_url = urlparse(new_request.url)
        except:
            return False

        subdomain = parsed_url.netloc.split(".")[:-2]
        subdomain_new = parsed_new_url.netloc.split(".")[:-2]

        if scope.protocol_must_match:
            if parsed_url.scheme != parsed_new_url.scheme:
                return False

        if scope.subdomain_must_match:
            if subdomain != subdomain_new:
                return False

        if scope.domain_must_match:
            if parsed_url.netloc != parsed_new_url.netloc:
                return False

        return True