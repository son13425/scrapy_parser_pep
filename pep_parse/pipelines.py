import csv
import datetime as dt
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:

    def open_spider(self, spider):
        self.count_status = Counter()

    def process_item(self, item, spider):
        status = item['status']
        self.count_status[status] = self.count_status.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        total = sum(self.count_status.values())
        results = [('Статус', 'Количество')]
        results.extend(self.count_status.items())
        results.append(('Total', total))
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, dialect='unix', quoting=csv.QUOTE_NONE)
            writer.writerows(results)
