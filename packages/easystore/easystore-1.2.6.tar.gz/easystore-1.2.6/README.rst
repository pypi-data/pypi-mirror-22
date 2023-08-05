Easystore is a generic interface to call and write to json files using the
abstractions used by redis-client.

## Sample
```
import sys
sys.path.append("..")
import easystore

k = easystore.DiskStore("jam")
k.hset("system", "metrics", {"cpu": "31"})
```
