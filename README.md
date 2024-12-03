# Random Redis scripts

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

## Scripts

### Scan to Unlink

Looks through the keyspace and removes keys starting with a pattern.
Remove the `--dry-run` to actually remove the keys

```bash
./scan_to_unlink.py --redis-port $REDISPORT --redis-host $REDISHOST --scan-prefix='{MYPREFIX}:' --dry-run
```


