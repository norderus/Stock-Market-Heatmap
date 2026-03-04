import json
import re

# Load original JSON
with open('metadata/companies.json', 'r', encoding='utf-8') as f:
    companies = json.load(f)

# Function to clean company name
def clean_company_name(full_name):
    # Search for text inside quotes (different types of quotes)
    match = re.search(r'"([^"]+)"|“([^”]+)”|«([^»]+)»', full_name)
    if match:
        # Take the first non-empty group
        return next(g for g in match.groups() if g)
    # If there are no quotes, remove the legal form at the beginning
    name = re.sub(r'^(Публичное акционерное общество|ПАО|Акционерное общество|АО|Открытое акционерное общество|ОАО|Закрытое акционерное общество|ЗАО|Корпорация|Компания)\s*', '', full_name, flags=re.IGNORECASE)
    # Remove extra spaces
    return name.strip()

# Dictionary of keywords for determining the sector
# Keys are a list of words (in uppercase), values are the sector name
SECTOR_KEYWORDS = {
    "БАНК|КРЕДИТ|ФИНАНС|ИНВЕСТ": "Финансы",
    "НЕФТ|ГАЗ|ГАЗПРОМ|РОСНЕФТЬ|ЛУКОЙЛ|БАШНЕФТЬ|ТАТНЕФТЬ|СУРГУТНЕФТЕГАЗ": "Нефтегаз",
    "МЕТАЛЛ|СТАЛЬ|ГОК|РУДА|АЛЮМИНИЙ|НОРНИКЕЛЬ|СЕВЕРСТАЛЬ|НЛМК|ММК|МЕЧЕЛ|ТМК|ЧЦЗ": "Металлургия",
    "ЗОЛОТ|ПОЛЮС|АЛРОСА|БУРЯТЗОЛОТО|СЕЛИГДАР|ЮГК": "Добыча",
    "СВЯЗЬ|ТЕЛЕКОМ|МТС|МЕГАФОН|РОСТЕЛЕКОМ|ЦЕНТРАЛЬНЫЙ ТЕЛЕГРАФ|ТАТТЕЛЕКОМ": "Телекоммуникации",
    "ЭНЕРГО|ГИДРО|ИНТЕР РАО|РОССЕТИ|ФСК|МОСЭНЕРГО|ЮНИПРО|ТГК|ЭЛЕКТРО|ГЕНЕРИРУЮЩ": "Энергетика",
    "ТРАНС|АЭРО|АВИА|РЖД|FESCO|ФЛОТ|ПОРТ|ПАРОХОДСТВО|АВТОВАЗ|КАМАЗ|СОЛЛЕРС": "Транспорт и машиностроение",
    "ХИМ|УДОБ|АКРОН|ФОСАГРО|КУЙБЫШЕВАЗОТ|НИЖНЕКАМСКНЕФТЕХИМ|КАЗАНЬОРГСИНТЕЗ": "Химия",
    "ТОРГ|РИТЕЙЛ|МАГНИТ|ЛЕНТА|ДЕТСКИЙ МИР|М.ВИДЕО|ОЗОН|ФИКС ПРАЙС|X5": "Торговля",
    "ПИЩ|ПРОДУКТ|ЧЕРКИЗОВО|РУСАГРО|БЕЛУГА|АБРАУ|ПИВОВАР|КОНДИТЕР": "Пищевая промышленность",
    "СТРОЙ|ДЕВЕЛОП|ПИК|ЛСР|ЭТАЛОН|САМОЛЕТ": "Строительство",
    "IT|ИНФОРМ|СОФТ|ЯНДЕКС|ВК|ЦИАН|ХЭДХАНТЕР|АСТРА|ДИАСОФТ|ГРУППА АРЕНАДАТА": "IT и цифровые технологии",
    "ФАРМ|МЕДИ|БИОТЕХ|ПРОМОМЕД|ОЗОН ФАРМ|ФАРМСИНТЕЗ|ГЕНЕТИКО": "Фармацевтика",
    "МАШИНОСТРО|ЗАВОД|МЕХАНИЧ|ПРИБОР|ЭНЕРГОМАШ|СИЛОВЫЕ МАШИНЫ|РАКЕТНО": "Машиностроение",
    "АПТЕКА|36,6": "Розничная торговля",
    "СТРАХ|РОСГОССТРАХ|РЕНЕССАНС": "Страхование",
}

def guess_sector(name):
    name_upper = name.upper()
    for pattern, sector in SECTOR_KEYWORDS.items():
        if re.search(pattern, name_upper):
            return sector
    return "Unknown"

# Process each company
for ticker, data in companies.items():
    full_name = data['name']
    # Clean the name
    short_name = clean_company_name(full_name)
    data['short_name'] = short_name
    # Determine the sector
    sector = guess_sector(short_name)
    data['sector'] = sector

# Save the updated JSON
with open('metadata/companies_enriched.json', 'w', encoding='utf-8') as f:
    json.dump(companies, f, ensure_ascii=False, indent=2)

print("Updated file: companies_enriched.json")