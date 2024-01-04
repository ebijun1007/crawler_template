import pandas as pd

class CsvPipeline:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        df.to_csv(f"{spider.name}.csv", index=False)
