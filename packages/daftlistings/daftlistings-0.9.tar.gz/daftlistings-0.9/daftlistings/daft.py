from bs4 import BeautifulSoup
import urllib2


class SaleType(object):
    HOUSES = '/houses-for-sale/'
    PROPERTIES = '/property-for-sale/'
    AUCTION = '/houses-for-auction/'
    APARTMENTS = '/apartments-for-sale/'
    COMMERCIAL = '/commercial-property/'


class CommercialType(object):
    OFFICE = '/offices/'
    RETAIL = '/retail-units/'
    OFFICE_SHARE = '/office-share/'
    INDUSTRIAL_UNIT = '/industrial-unit/'
    COMMERCIAL_SITE = '/commercial-site/'
    AGRICULTURAL_LAND = '/agricultural-farm-land/'
    RESTAURANT_BAR_HOTEL = '/restaurant-hotel-bar/'
    INDUSTRIAL_SITE = '/industrial_site/'
    DEV_LAND = '/development-land/'
    INVESTMENT_PROPERTY = '/investment-property/'
    SERVICED_OFFICE = '/serviced-office/'


class RentType(object):
    HOUSES = '/houses-for-rent/'
    APARTMENTS = '/apartments-for-rent/'
    ANY = '/residential-property-for-rent/'
    STUDIO = '/studio-apartments-for-rent/'
    FLAT = '/flats-for-rent/'


class QueryParam(object):
    SALE_AGREED = '&s[area_type]=on&s[agreed]=1&s[advanced]=1'
    SALE_AGREED_WITH_PRICE = '&s%5Bagreed%5D=1&s%5Badvanced%5D=1'
    MIN_PRICE = '&s%5Bmnp%5D='
    MAX_PRICE = '&s%5Bmxp%5D='
    IGNORED_AGENTS = '&s%5Bignored_agents%5D%5B1%5D'
    MIN_BEDS = '&s%5Bmnb%5D='
    MAX_BEDS = '&s%5Bmxb%5D='
    SORT_BY = '&s%5Bsort_by%5D='
    SORT_ORDER = '&s%5Bsort_type%5D='


class Daft:
    _base = 'http://www.daft.ie'
    _opener = urllib2.build_opener()
    _opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    def __init__(self):
        pass

    def get_listings(
            self,
            county,
            area=None,
            offset=0,
            min_price=None,
            max_price=None,
            listing_type='properties',
            sale_agreed=False,
            sale_type='sale',
            min_beds=None,
            max_beds=None,
            sort_by=None,
            sort_order=None,
            commercial_property_type=None
    ):

        """
        :param max_beds: The maximum number of beds.
        :param min_beds: The minimum number of beds.
        :param max_price: The maximum value of the listing
        :param min_price: The minimum value of the listing
        :param county: The county to get listings for.
        :param area: The area in the county to get listings for. If not set then we'll search all areas within the county.
        :param offset: The page number.
        :param listing_type: The listings you'd like to scrape i.e houses, properties, auction, commercial or apartments.
        :param sale_agreed: If set to True, we'll scrape listings that are sale agreed.
        :param sale_type: Retrieve listings of a certain sale type. Can be set to 'sale' or 'rent'.
        :param sort_by: Sorts the listing. Can be set to 'date', 'distance', 'prince' or 'upcoming_viewing'.
        :param sort_order: 'd' for descending, 'a' for ascending.
        :param commercial_property_type
        :return: object
        """

        if area is None:
            area = ''

        query_params = ''
        price = ''

        county = county.replace(" ", "-").lower()
        area = area.replace(" ", "-").lower()

        if min_price:
            if isinstance(min_price, int):
                price += QueryParam.MIN_PRICE + str(min_price)
            else:
                raise Exception('Min price should be integer.')

        if max_price:
            if isinstance(min_price, int):
                price += QueryParam.MAX_PRICE + str(max_price)
            else:
                raise Exception('Max price should be integer.')

        if sale_agreed:
            if min_price or max_price:
                query_params += price + QueryParam.SALE_AGREED_WITH_PRICE
            else:
                query_params += QueryParam.SALE_AGREED
        else:
            if min_price or max_price:
                query_params += price

        if min_price or max_price and sale_type == 'rent':
            query_params += QueryParam.IGNORED_AGENTS

        if min_beds:
            query_params += QueryParam.MIN_BEDS + str(min_beds)

        if max_beds:
            query_params += QueryParam.MAX_BEDS + str(max_beds)

        if sort_by:
            if sort_order:
                query_params += QueryParam.SORT_ORDER + sort_order
                query_params += QueryParam.SORT_BY + sort_by
            else:
                query_params += QueryParam.SORT_ORDER + 'd'
                query_params += QueryParam.SORT_BY + sort_by

        commercial = commercial_property_type if commercial_property_type is not None else ''

        soup = self._call(
            self._base + '/' + county + listing_type + area + commercial + '?offset=' + str(offset) + query_params)
        divs = soup.find_all("div", {"class": "box"})

        listings = []
        [listings.append(Listing(div)) for div in divs]
        return listings

    def _call(self, url):
        return BeautifulSoup(self._opener.open(url), 'html.parser')


class Listing(Daft):
    def __init__(self, data):
        Daft.__init__(self)
        self.data = data

    def get_price(self):
        try:
            return self.data.find('strong', {'class': 'price'}).text
        except:
            return

    def get_formalised_address(self):
        try:
            t = self.data.find('a').contents[0]
            s = t.split('-')
            a = s[0].strip()
            if 'SALE AGREED' in a:
                a = a.split()
                a = a[3:]
                a = ' '.join([str(x) for x in a])
            return a.lower().title().strip()
        except:
            return

    def get_address_line_1(self):
        formalised_address = self.get_formalised_address()
        if formalised_address is None:
            return
        try:
            address = formalised_address.split(',')
            return address[0].strip()
        except:
            return

    def get_address_line_2(self):
        formalised_address = self.get_formalised_address()
        if formalised_address is None:
            return

        try:
            address = formalised_address.split(',')
            if len(address) == 4:
                return address[1].strip()
            else:
                return
        except:
            return

    def get_town(self):
        formalised_address = self.get_formalised_address()
        if formalised_address is None:
            return
        try:
            address = formalised_address.split(',')
            return address[-2].strip()
        except:
            return

    def get_county(self):
        formalised_address = self.get_formalised_address()
        if formalised_address is None:
            return
        try:
            address = formalised_address.split(',')
            return address[-1].strip()
        except:
            return

    def get_listing_image(self):
        try:
            link = self.get_daft_link()
            soup = self._call(link)
            span = soup.find("span", {"class": "p1"})
            return span.find('img')['src']
        except:
            return

    def get_agent(self):
        try:
            agent = self.data.find('ul', {'class': 'links'}).text
            return agent.split(':')[1].strip()
        except:
            return

    def get_agent_url(self):
        try:
            agent = self.data.find('ul', {'class': 'links'})
            links = agent.find_all('a')
            return links[1]['href']
        except:
            return

    def get_daft_link(self):
        link = self.data.find('a', href=True)
        try:
            return self._base + link['href']
        except:
            return

    def get_dwelling_type(self):
        try:
            info = self.data.find('ul', {"class": "info"}).text
            s = info.split('|')
            return s[0].strip()
        except:
            return

    def get_posted_since(self):
        try:
            info = self.data.find('div', {"class": "date_entered"}).text
            s = info.split(':')
            return s[-1].strip()
        except:
            return

    def get_num_bedrooms(self):
        try:
            info = self.data.find('ul', {"class": "info"}).text
            s = info.split('|')
            nb = s[1].strip()
            return int(nb.split()[0])
        except:
            return

    def get_num_bathrooms(self):
        try:
            info = self.data.find('ul', {"class": "info"}).text
            s = info.split('|')
            nb = s[2].strip()
            return int(nb.split()[0])
        except:
            return
