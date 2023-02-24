from bs4 import BeautifulSoup
import grequests, json, requests
from multiprocessing.dummy import Pool as ThreadPool
from termcolor import colored
pool = ThreadPool(100)


scrapers = [
    'http://multiproxy.org/txt_all/proxy.txt',
    'https://www.sslproxies.org/',
    'http://free-proxy.cz/en/',
    'https://www.us-proxy.org/',
    'https://free-proxy-list.net/',
    'https://www.proxy-list.download/api/v0/get?l=en&t=https',
    'https://www.duplichecker.com/free-proxy-list.php',
    'http://www.httptunnel.ge/ProxyListForFree.aspx',
    'https://checkerproxy.net/'
]

rs = (grequests.get(u, timeout=8) for u in scrapers)
rs = grequests.map(rs)
proxies = []

def check(proxy):
    prox = {'http': proxy, 'https': proxy}
    try:
        requests.get('http://httpbin.org/get', proxies=prox, timeout=5)
        print(colored(f'ALIVE | {proxy}', 'green'))
        with open('good.txt', 'a') as proxy_folder:
            proxy_folder.write(proxy + '\n')
    except Exception as e:
        print(colored(f'DEAD | {proxy}', 'red'))


for i in list(range(len(scrapers))):
    if rs[i]:
        html = rs[i].text
        soup = BeautifulSoup(html, 'html.parser')
        scraper = scrapers[i]

        if scraper == 'http://multiproxy.org/txt_all/proxy.txt':
            proxies.extend(html.split('\n'))

        elif scraper == 'https://www.sslproxies.org/':
            tr = soup.find('table', {'class': 'table-striped'})
            prox = list(tr.find_all('tr'))
            prox.pop(0)
            for proxy in prox:
                try:
                    proxy = proxy.find_all('td')
                    ip = str(proxy[0]).replace('</td>', '').replace('<td>', '')
                    port = str(proxy[1]).replace('</td>', '').replace('<td>', '')
                    proxies.append(f'{ip}:{port}')
                except Exception as e:
                    pass

        elif scraper == 'https://free-proxy-list.net/':
            tr = soup.find('table', {'class': 'table-striped'})
            prox = list(tr.find_all('tr'))
            prox.pop(0)
            for proxy in prox:
                try:
                    proxy = proxy.find_all('td')
                    ip = str(proxy[0]).replace('</td>', '').replace('<td>', '')
                    port = str(proxy[1]).replace('</td>', '').replace('<td>', '')
                    proxies.append(f'{ip}:{port}')
                except Exception as e:
                    pass

        elif scraper == 'https://www.us-proxy.org/':
            tr = soup.find('table', {'class': 'table-striped'})
            prox = list(tr.find_all('tr'))
            prox.pop(0)
            for proxy in prox:
                try:
                    proxy = proxy.find_all('td')
                    ip = str(proxy[0]).replace('</td>', '').replace('<td>', '')
                    port = str(proxy[1]).replace('</td>', '').replace('<td>', '')
                    proxies.append(f'{ip}:{port}')
                except Exception as e:
                    pass

        elif scraper == 'https://www.proxy-list.download/api/v0/get?l=en&t=https':
            asd = json.loads(html)[0]
            for proxy in asd['LISTA']:
                proxies.append(f'{proxy.get("IP")}:{proxy.get("PORT")}')

        elif scraper == 'https://www.duplichecker.com/free-proxy-list.php':
            arr = soup.find_all('div', {'class': 'col-md-12 col-sm-12 col-xs-12 result_row mn wb_ba'})
            for thing in arr:
                children = list(thing.children)
                ip = children[1].text
                port = children[3].text
                proxies.append(f'{ip}:{port}')

        elif scraper == 'http://www.httptunnel.ge/ProxyListForFree.aspx':
            table = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_GridViewNEW'})
            for thing in table.find_all('tr'):
                try:
                    proxies.append(thing.td.a.text)
                except AttributeError:
                    pass

        #big one
        elif scraper == 'https://checkerproxy.net/':
            div = soup.find('div', {'class': 'block archive f_right'})
            ali = div.ul.find_all('li')
            for li in ali:
                link = 'https://checkerproxy.net/api/archive/' + li.a['href'].split('/')[2]
                response = requests.get(link)
                asd = json.loads(response.text)
                print(f'Got {len(asd)} proxies from https://checkerproxy.net/')
                for proxy in asd:
                    if proxy['type'] == 1 or proxy['type'] == 2:
                        proxies.append(proxy['addr'])


print('Checking {} Proxies'.format(len(proxies)))

pool.map(check, proxies)
