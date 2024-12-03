#!/usr/bin/env python

import redis
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--redis-host', default="localhost")
parser.add_argument('--redis-port', default=6379)
parser.add_argument('--redis-password', default="")
parser.add_argument('--dry-run', default=False, action="store_true")
parser.add_argument('--scan-prefix', default="BROKENFORSURE:")
args = parser.parse_args()

keys_to_unlink = []

redis_client = redis.StrictRedis(
    host=args.redis_host,
    port=args.redis_port,
    password=args.redis_password
)

for key in redis_client.scan_iter("{}*".format(args.scan_prefix)):
    keys_to_unlink.append(key.decode("utf-8"))

if args.dry_run:
    print("DRY RUN - NOT UNLINKING {} keys".format(len(keys_to_unlink)))
    for key in keys_to_unlink:
        print(key)
    print("DRY RUN - NOT UNLINKING {} keys".format(len(keys_to_unlink)))

else:
    pipelines = redis_client.pipeline()
    batch_count = 0
    for key in keys_to_unlink:
        batch_count += 1
        pipelines.unlink(key)
        if batch_count % 1000 == 0:
            pipelines.execute()
            print("Unlinked {} keys".format(batch_count))
            batch_count = 0
    pipelines.execute()
    print("Unlinked {} keys".format(batch_count))
