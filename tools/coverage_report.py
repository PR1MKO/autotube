import sys
import orjson
from collections import Counter
from urllib.parse import urlparse


def main(paths):
    source_counts = Counter()
    locale_counts = Counter()
    canonicals = set()
    prefix_counts = Counter()
    for path in paths:
        with open(path, "rb") as f:
            for line in f:
                item = orjson.loads(line)
                source_counts[item.get("source")] += 1
                locale_counts[item.get("locale")] += 1
                canon = item.get("canonical_url")
                if canon:
                    canonicals.add(canon)
                    parsed = urlparse(canon)
                    prefix = "/".join(parsed.path.split("/")[:3])
                    prefix_counts[prefix] += 1
    print("Counts by source:")
    for k, v in source_counts.items():
        print(f"  {k}: {v}")
    print("Counts by locale:")
    for k, v in locale_counts.items():
        print(f"  {k}: {v}")
    print(f"Unique canonical_url: {len(canonicals)}")
    print("Top 10 path prefixes:")
    for prefix, count in prefix_counts.most_common(10):
        print(f"  {prefix}: {count}")


if __name__ == "__main__":
    main(sys.argv[1:])