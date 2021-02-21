from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm
import requests
import argparse


def spotify_page_scraper(url: str, pages: int):
    for i in range(pages):
        player_page_link = f'{url}/page/{i + 1}'

        req = requests.get(player_page_link)

        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')

            print(player_page_link)

            url_collection = [link.get('href') for link in soup.find_all('a', {'class': 'btn-playnow'})]

            [spotify_mp3_download(url) for url in url_collection]
        else:
            break


def get_player_page(url: str) -> str:
    req = requests.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')

    return soup.find('a', {'class': 'post_toolbar_download'}).get('href')


def find_download_page(url: str) -> str:
    req = requests.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')

    return soup.find('a', {'class': 'download-btn'}).get('href')


def spotify_mp3_download(url: str):
    player_page = get_player_page(url)

    download_url = find_download_page(player_page)

    filename = url.removesuffix('/').split('/')[-1]

    has_downloaded = download_file(filename, download_url)

    if has_downloaded:
        print(f'{url} is downloaded as {filename}')
    else:
        print('Skipping: {filename} already exists in working directory')

    print()


def download_file(filename: str, url: str) -> bool:
    # TODO: Are the files always mp3?
    filename = filename + '.mp3'
    tmp_file_name = filename + '.tmp'

    cwd = Path.cwd()

    file_path = cwd.joinpath(filename)
    tmp_path = cwd.joinpath(tmp_file_name)

    if file_path.exists():
        return False

    #remove an existing temp file
    if tmp_path.exists():
        tmp_path.unlink()

    with requests.get(url, stream=True) as response:
        response.raise_for_status()

        total = int(response.headers.get('content-length', 0))

        with open(tmp_path, 'wb') as f, tqdm(
            desc=filename,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                size = f.write(chunk)
                bar.update(size)

    tmp_path.replace(filename)

    return True


def downloader():
    try:
        parser = argparse.ArgumentParser(
            description='This will download podcasts from podbean to the current working directory')

        parser.add_argument('-p', '--pages', required=False, default=1, type=int)
        parser.add_argument('-u', '--url', required=True, type=str)

        args = parser.parse_args()

        spotify_page_scraper(args.url, args.pages)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    downloader()
