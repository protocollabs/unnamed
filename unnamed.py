#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import asyncio
import socket
import struct
import binascii
import time
import sys
import functools
import argparse
import signal
import os
import uuid
import json
import zlib
import datetime
import urllib.request
import urllib.error
import pprint


def init_v4_rx_fd(conf):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setblocking(False)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(s, "SO_REUSEPORT"):
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.bind(('localhost', 6666))
    print('listen on port 6666')
    return s


def init_v4_tx_fd(conf):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, int(conf['core']['v4-mcast-ttl']))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(conf['l0_top_addr_v4']))
    return sock


def cb_v4_rx(fd, queue):
    try:
        data, addr = fd.recvfrom(1024)
        print(data)
    except socket.error as e:
        print('Expection')
    d = {}
    d["proto"] = "IPv4"
    d["src-addr"]  = addr[0]
    d["src-port"]  = addr[1]
    d["data"]  = data
    try:
        queue.put_nowait(d)
    except asyncio.queues.QueueFull:
        sys.stderr.write("queue overflow, strange things happens")



async def tx_v4(fd, conf, db):
    addr     = conf['core']['v4-mcast-addr']
    port     = int(conf['core']['v4-mcast-port'])
    interval = float(conf['core']['tx-interval'])
    while True:
        try:
            data = ""
            ret = fd.sendto(data, (addr, port))
            emsg = "transmitted OHNDL message via {}:{} of size {}"
            print(emsg.format(addr, port, ret))
        except Exception as e:
            print(str(e))
        await asyncio.sleep(interval)


async def handle_packet(queue, conf, db):
    while True:
        entry = await queue.get()
        data = parse_payload(entry)


async def db_check_outdated(db, conf):
    while True:
        await asyncio.sleep(1)


async def terminal_query_l1_top_addr_loop(db, conf):
    while True:
        await asyncio.sleep(float(conf["terminal_interface_get_interval"]))



def ask_exit(signame, loop):
    sys.stderr.write("got signal %s: exit\n" % signame)
    loop.stop()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--configuration", help="configuration", type=str, default=None)
    args = parser.parse_args()
    if not args.configuration:
        print("Configuration required, please specify a valid file path, exiting now")
        sys.exit(1)
    return args


def load_configuration_file(args):
    config = dict()
    exec(open(args.configuration).read(), config)
    return config


def conf_init():
    args = parse_args()
    return load_configuration_file(args)


def ctx_new():
    return {}

def main():
    conf = conf_init()
    db = ctx_new()

    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(32)

    # RX functionality
    fd = init_v4_rx_fd(conf)
    loop.add_reader(fd, functools.partial(cb_v4_rx, fd, queue))

    # TX side
    #fd = init_v4_tx_fd(conf)
    #asyncio.ensure_future(tx_v4(fd, conf, db))

    # Outputter
    #asyncio.ensure_future(handle_packet(queue, conf, db))

    #asyncio.ensure_future(db_check_outdated(db, conf))


    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                functools.partial(ask_exit, signame, loop))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
