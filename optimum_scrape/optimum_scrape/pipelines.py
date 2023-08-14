# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import csv


class IntoCSVPipeline:
    def open_spider(self, spider):
        self.file = open('output.csv', 'w', newline='\n', encoding='windows-1251')
        self.csv_writer = csv.DictWriter(self.file, fieldnames=
        ['domain', 'title', 'description', 'email', 'phone', 'inn', 'ogrn'], delimiter=';')
        self.csv_writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        item['title'] = item.get('title', 'н/д')
        item['description'] = item.get('description', 'н/д')
        item['email'] = item.get('email', 'н/д')
        item['phone'] = item.get('phone', 'н/д')
        item['inn'] = item.get('inn', 'н/д')
        item['ogrn'] = item.get('ogrn', 'н/д')

        # Преобразование значений в строки
        item = {key: str(value) for key, value in item.items()}

        self.csv_writer.writerow(item)
        return item
