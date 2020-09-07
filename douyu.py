# -*- coding: utf-8 -*-

import argparse
import logging

import requests

logger = logging.getLogger('douyu')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('douyu.log')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


class Douyu(object):
    _donate_url = 'https://www.douyu.com/japi/prop/donate/mainsite/v1'

    def __init__(self, cookie, rid):
        """
        :param cookie: cookie
        :param rid: room id
        """
        self.cookie = cookie
        self.rid = rid
        self.headers = {
            'Origin': 'https://www.douyu.com',
            'Cookie': self.cookie,
            'Referer': 'https://www.douyu.com/{}'.format(rid)
        }

    def donate(self, count):
        data = {'propId': 268, 'propCount': count, 'roomId': self.rid, 'bizExt': '{"yzxq": {}}'}
        r = requests.post(self._donate_url, data=data, headers=self.headers)
        request = r.request
        logger.debug('{method} {url} {headers} {body}'.format(method=request.method, url=request.url,
                                                              headers=request.headers, body=request.body))
        if r.status_code == 200 and r.json()['error'] == 0:
            logger.info('donate {} props to roomid {}'.format(count, self.rid))
        else:
            logger.error(r.json())


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='')
    parse.add_argument('-f', '--file', dest='file', type=str, help='cookies file', metavar='FILE',
                       default='cookies.txt')
    parse.add_argument('-r', '--room', dest='rooms', type=int, action='append', help='room id', metavar='ROOM',
                       default=[])
    parse.add_argument('-n', '--num', dest='nums', type=int, action='append', help='prop num', metavar='NUMBER',
                       default=[])
    args = parse.parse_args()

    rooms = args.rooms
    nums = args.nums

    if len(rooms) != len(nums):
        raise ValueError('room and num must match quantity')

    with open(args.file) as f:
        cookies = f.read()

    for i in range(len(rooms)):
        dy = Douyu(cookies, rooms[i])
        dy.donate(nums[i])
