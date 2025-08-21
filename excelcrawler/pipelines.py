from pathlib import Path
import orjson


class JsonlWriterPipeline:
    def open_spider(self, spider):
        Path("data/pages_jsonl").mkdir(parents=True, exist_ok=True)
        self.file = open(f"data/pages_jsonl/{spider.name}.jsonl", "ab")

    def close_spider(self, spider):
        if hasattr(self, "file"):
            self.file.close()

    def process_item(self, item, spider):
        self.file.write(orjson.dumps(dict(item)) + b"\n")
        return item