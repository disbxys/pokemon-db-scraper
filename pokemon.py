from bs4 import BeautifulSoup

class Pokemon:

    __slots__ = ('original_data', 'id', 'name', 'types', 'stats')

    def __init__(self, data) -> None:
        self.original_data = data

        self.id = "000"
        self.name = ""
        self.types = []
        self.stats = {
            "total": 0, 
            "hp": 0,
            "atk": 0, "def": 0,
            "sp_atk": 0, "sp_def": 0,
            "spd": 0
        }

        self._process_data()

    
    def gather(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "types": self.types,
            "stats": self.stats
        }


    def _extract_id(self) -> None:
        id_tag = self.original_data.select_one('span[class="infocard-cell-data"]')
        if id_tag.text:
            self.id = id_tag.text
        else:
            self.id = None


    def _extract_name(self) -> None:
        name_tag = self.original_data.select_one('td[class="cell-name"]')

        self.name = name_tag.select_one('[class="ent-name"]').text
        if name_tag.select_one('small[class="text-muted"]'):
            self.name += " | " + name_tag.select_one('[class="text-muted"]').text


    def _extract_types(self) -> None:
        self.types = []
        for types_tag in self.original_data.select('a[class^="type-icon type"]'):
            self.types.append(types_tag.text)


    def _extract_stats(self) -> None:
        self.stats["total"] = self.original_data.select_one('td[class="cell-num cell-total"]').text
        
        stats_tags = self.original_data.select('td[class="cell-num"]')
        self.stats["hp"] = stats_tags[0].text
        self.stats["atk"] = stats_tags[1].text
        self.stats["def"] = stats_tags[2].text
        self.stats["sp_atk"] = stats_tags[3].text
        self.stats["sp_def"] = stats_tags[4].text
        self.stats["spd"] = stats_tags[5].text
    

    def _process_data(self):
        self._extract_id()
        self._extract_name()
        self._extract_types()
        self._extract_stats()