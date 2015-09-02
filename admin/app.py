#!/usr/bin/env python3

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/plain; charset=utf-8')])
    return [b"Hello World"]
