import datetime

from nepali_date import NepaliDate


def convert_to_nepali(date):
    en_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    nepali_date = NepaliDate.to_nepali_date(en_date)
    return nepali_date


def convert_to_english( date):
    year, month, day = [int(s) for s in date.split("-") if s.isdigit()]
    nepali_date = NepaliDate(year, month, day)
    en_date = nepali_date.to_english_date()
    return en_date
