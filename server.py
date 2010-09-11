#!/usr/bin/env python

import eventlet
import eventlet.db_pool
import eventlet.wsgi
eventlet.monkey_patch()

import MySQLdb



__dbpool = eventlet.db_pool.ConnectionPool(MySQLdb, host='127.0.0.1',
        user='root', passwd='', db='mysql')

def handler(env, start_response):
    conn = None
    try:
        conn = __dbpool.get()
        cursor = conn.cursor()
        result = cursor.execute('''SELECT NOW()''')
        now = cursor.fetchone()
        start_response('200 OK', [('Content-Type', 'text/plain',)])
        return ['Yay: %s\r\n' % now]
    finally:
        if conn:
            __dbpool.put(conn)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8080)), handler)

