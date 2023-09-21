from exceptions import NegativeTitlesError
from exceptions import InvalidYearCupError
from exceptions import ImpossibleTitlesError
from datetime import datetime

def data_processing(dict):
    if dict["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")
    
    year_dict = int(dict["first_cup"][:4])
    year = int(datetime.now().year)+1
    date_init = 1930
    year_cop = []
    number_titles = []

    for x in range(date_init, year, 4):
        year_cop.append(x)

    if year_dict not in year_cop:
        raise InvalidYearCupError("there was no world cup this year")
        
    for x in range(year_dict, year, 4):
        number_titles.append(x)
    
    if len(number_titles) < dict["titles"]:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")

