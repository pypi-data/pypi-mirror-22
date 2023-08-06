#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015,2016 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Required package (on Debian8):
# - BeautifulSoup4: python3-bs4

# Online documentation:
# - BeautifulSoup4: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
# - Urllib:         https://docs.python.org/3/library/internet.html
#                   https://docs.python.org/3/library/urllib.request.html

import argparse
from bs4 import BeautifulSoup
import gzip
import shutil
import time
import urllib.request
from urllib.parse import urljoin

TIME_SLEEP = 1

class Node:
    """Node class.

    This class should be subclassed for each website to crawl. Each subclass
    should redefine "visit", "child_nodes" and "is_final".
    """

    traversed_nodes = []

    def __init__(self, url, depth=0):
        print("Creating node (level {}) {}...".format(depth, url))

        self.url = url
        self.depth = depth

        print("Request", self.url)
        self.html = urllib.request.urlopen(self.url).read()


    @property
    def child_nodes(self):
        child_nodes_set = set()

        if not self.is_final:
            #html = urllib.request.urlopen(self.url).read()
            soup = BeautifulSoup(self.html)

            for anchor in soup.find_all('a'):
                relative_url = anchor.get('href')
                absolute_url = urljoin(self.url, relative_url)
                child_node = Node(absolute_url, self.depth + 1)
                #print(id(child_node))
                child_nodes_set.add(child_node)

        return child_nodes_set


    def visit(self):
        """Do something with node value."""
        print("Visiting {}...".format(self.url))

        # Wait a litte bit
        time.sleep(TIME_SLEEP)      # TODO: randomize time sleep


    @property
    def is_final(self):
        return self.depth >= 1

    def __str__(self):
        return "%s" % self.url

    def __eq__(self, other):
        """
        TODO: doctest

            node1 = Node("http://www.google.com")
            node2 = Node("http://www.google.com")
            traversed_nodes = [node1]
            node2 in traversed_nodes
            >>> True
        """

        return self.url == other.url

    def __hash__(self):
        # See http://stackoverflow.com/questions/1608842/types-that-define-eq-are-unhashable-in-python-3-x
        return id(self)


def walk(node):
    """The graph traversal function"""

    Node.traversed_nodes.append(node)
    
    # Do something with node value...
    node.visit()

    # Recurse on each child node
    for child_node in node.child_nodes:
        if child_node not in Node.traversed_nodes:
            walk(child_node)


def read_html_from_file(file_path):
    """This function can be useful for offline debug"""

    with open(file_path, 'rU') as fd:
        html = fd.read()

    return html


def download_html(url, http_headers_dict={}):
    html = None

    http_request = urllib.request.Request(url, data=None, headers=http_headers_dict)

    with urllib.request.urlopen(http_request) as http_response:
        if http_response.info().get('Content-Encoding') == 'gzip':
            gz_file = gzip.GzipFile(fileobj=http_response)
            #html = gz_file.read().decode('utf-8')
            html = gz_file.read()
        else:
            #html = http_response.read().decode('utf-8')
            html = http_response.read()

    return html


def download_img(img_url, img_output_path, http_headers_dict={}):
    request = urllib.request.Request(img_url, data=None, headers= http_headers_dict)
    with urllib.request.urlopen(request) as response, open(img_output_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='Generic web crawler.')
    parser.add_argument("url", nargs=1, metavar="URL",
                        help="The URL of the webpage to parse.")
    args = parser.parse_args()

    url = args.url[0]

    # TRAVERSE THE GRAPH ######################################################

    start_node = Node(url)
    walk(start_node)

    # PRINT TRAVERSED NODES ###################################################

    print("Traversed nodes:")
    for node in Node.traversed_nodes:
        print(" ", node)


if __name__ == '__main__':
    main()
