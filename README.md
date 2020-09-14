# uuid-by-string
Generate the RFC-4122 Name-Based UUID. Supports 3 (md5) and 5(sha1) versions of UUID. Referenced from [danakt/uuid-by-string: Generates the RFC-4122 Name-Based UUID](https://github.com/danakt/uuid-by-string).

## Install

```bash
$ pip install uuid-by-string
```

## Usage

```python
from uuid_by_string import generate_uuid

uuid = generate_uuid("a string")
# 555d01e6-c832-56b3-a9f9-2bd811905370
uuid_v3 = generate_uuid("❤️", version=3)
# 080c1417-9a0e-3386-a131-a7fa8dbe2c51
uuid_v5 = generate_uuid("❤️", 5)
# f11c13f0-5595-551d-bdee-e6c2e43fd2a9
```

