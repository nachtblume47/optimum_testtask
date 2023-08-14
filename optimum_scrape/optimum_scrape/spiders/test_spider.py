

import scrapy
import re




class DomainSpider(scrapy.Spider):
    name = 'test_spider'

    custom_settings = {
        'RETRY_TIMES': 1,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404],
    }

    def __init__(self, *args, **kwargs):
        super(DomainSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = self.read_domains_file('domains.txt')
        self.blocked_domains = self.read_domains_file('block_domains.txt')


    def read_domains_file(self, filename):
        #работаем с файлом + set на всякий случай для уникальности
        with open(filename, 'r') as file:
            return set(line.strip() for line in file.readlines())

    def parse(self, response):
        # формируем словарь из результатов поиска в респонсе
        data = {
            'domain': response.url,
            'title': response.css('title::text').get(default='н/д'),
            'description': response.css('meta[name="description"]::attr(content)').get(default='н/д'),
            'email': self.extract_email(response.text),
            'phone': self.extract_phone(response.text),
            'inn': self.extract_inn(response.text),
            'ogrn': self.extract_ogrn(response.text)
        }
        yield data

    def extract_email(self, text):
        # Извлечение электронной почты по шаблону
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group() if match else 'н/д'

    def extract_phone(self, text):
        # Извлечение телефона по шаблону
        phone_pattern = r'\b\+?[7,8](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b'
        match = re.search(phone_pattern, text)
        return match.group() if match else 'н/д'

    def extract_inn(self, text):
        inn_pattern = r'ИНН.*(\d{10})'
        match = re.search(inn_pattern, text)
        return match.group() if match else 'н/д'

    def extract_ogrn(self, text):
        ogrn_pattern = r'ОГРН.*(\d{13})'
        match = re.search(ogrn_pattern, text)
        return match.group() if match else 'н/д'

    def start_requests(self):
        #парсим только то что можно
        for domain in self.allowed_domains:
            if domain not in self.blocked_domains:
                url = f"http://{domain}"
                yield scrapy.Request(url, callback=self.parse)


