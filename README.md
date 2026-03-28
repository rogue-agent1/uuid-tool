# uuid_tool

Generate, validate, and inspect UUIDs (v1, v3, v4, v5).

## Usage

```bash
python3 uuid_tool.py gen                          # Random v4
python3 uuid_tool.py gen -v 1                     # Time-based v1
python3 uuid_tool.py gen -v 5 --name example.com  # Name-based v5
python3 uuid_tool.py gen -n 5 -f upper            # 5 uppercase UUIDs
python3 uuid_tool.py inspect 550e8400-e29b-41d4-a716-446655440000
python3 uuid_tool.py validate <uuid1> <uuid2>
python3 uuid_tool.py batch 100 --format bare
python3 uuid_tool.py nil
```

## Zero dependencies. Single file. Python 3.8+.
