from bs4 import BeautifulSoup
from pathlib import Path
from requests import HTTPError
from tqdm import tqdm
from urllib.parse import urlparse
import requests
import argparse
import logging


def find_download_url(url: str) -> tuple[str, bool]:
    """
    Find the download url.
    :param url:
    :return: tuple with the url and whether it is an alternate layout
    """
    def find_play_now_button(soup_obj):
        return soup_obj.find('a', {'class': 'btn-playnow'})

    def find_post_toolbar_download(soup_obj):
        return soup_obj.find('a', {'class': 'post_toolbar_download'})

    logging.debug(f'Request podcasts home page: {url}')

    r = requests.get(url)

    if r.status_code == 200:
        logging.debug('Scraping page')
        soup = BeautifulSoup(r.text, features='html.parser')

        play_now_btn = find_play_now_button(soup)

        is_alternate_layout = False

        if play_now_btn is None:
            post_toolbar_download = find_post_toolbar_download(soup)

            href: str = post_toolbar_download.get('href')

            logging.debug(f'Found episode page url: {href}')

            return href, is_alternate_layout
        else:
            logging.debug('Found alternate podcaster home page')

            play_now_button = find_play_now_button(soup)

            href: str = play_now_button.get('href')

            is_alternate_layout = True

            logging.debug(f'Found `playnow` button link: {href}')

            return href, is_alternate_layout


def find_page_download_links(url: str, pages: int) -> list[str | list[str] | None]:
    """
    Scraps the episode pages and yields a url collection for each page it scraps
    :param url: the root episode page url to download from
    :param pages: the number of pages to go back.
    :return: yields a url collection
    """
    url = url.rstrip("/")

    result = urlparse(url)

    prev_request_text = None

    for i in range(pages):
        scrape_url = f'{result.scheme}://{result.hostname}{result.path}?page={i + 1}&ajax=yw0'

        logging.debug(f'scraping episode page: {scrape_url}, page number: {i + 1}')

        req = requests.get(scrape_url)

        req.raise_for_status()

        if req.status_code == 200:
            # There is no way to check if we have reached the end of the pages It just gets the last page with
            # downloads on it. So if the page content is the same as the previous page then we can assume we have
            # reached the end and break out of our loop.
            if req.text == prev_request_text:
                logging.debug('Previous page is the same as the current request page. Stopping page scraping')
                break

            prev_request_text = req.text

            soup = BeautifulSoup(req.text, 'html.parser')

            url_collection = [link.get('href') for link in soup.select('a.download')]

            logging.debug(f'Found {len(url_collection)} download links')

            yield url_collection


def find_episode_page_for_alternate_layout(url: str) -> str:
    """
    Finds the episode link for the alternate author pages. I've only found a handful of these.

    All this does is find the newer episode page link on these pages.
    :param url:
    :return: episode page url
    """

    url = url.rstrip("/")

    req = requests.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')

    return soup.find('a', {'class': 'post_toolbar_download'}).get('href')


def podbean_download(url: str, re_download: bool, destination: Path = None) -> None:
    """
    Downloads our podcast. If the podcast hasn't been downloaded or the user has told the program to re-download the
    files Then downloads the file. If it thinks we have downloaded the file and the re_download file is false then it
    will skip the file and move to the next.

    :param url: the file url
    :param re_download: whether we should just redownload it
    :param destination: where the file should go
    :return:
    """
    filename = url.removesuffix('/').split('/')[-1]

    has_downloaded = download_file(filename, url, destination)

    if has_downloaded and not re_download:
        logging.info(f'{url} is downloaded as {filename}')
    else:
        logging.info(f'Skipping: {filename} already exists in working directory')


def download_file(filename: str, url: str, destination: Path = None) -> bool:
    """
    Downloads the file. This prints us a nice progress bar as the page downloads.

    :param destination:
    :param filename: the filename we are download
    :param url: the url of the download
    :return: None
    """
    filename = filename
    tmp_file_name = f'{filename}.tmp'

    output_dir = destination if destination else Path.cwd()

    file_path = output_dir.joinpath(filename)
    tmp_path = output_dir.joinpath(tmp_file_name)

    if file_path.exists():
        return False

    # remove an existing temp file
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
    def create_or_get_destination_dir(dest: str) -> Path | None:
        """
        Create or gets the destination director. Raises a value error if the path exits and not a directory.
        :param dest:
        :return: destination path
        :raises ValueError
        """
        if not dest:
            return None

        output_dir = Path(dest)

        if output_dir.exists() and not output_dir.is_dir():
            raise ValueError("destination must be a directory")

        output_dir.mkdir(exist_ok=True)

        return output_dir

    try:
        parser = argparse.ArgumentParser(
            description='This will download podcasts from podbean to the current working directory')

        parser.add_argument('-p', '--pages', required=False, default=1, type=int)
        parser.add_argument('-u', '--url', required=True, type=str)
        parser.add_argument('-v', '--verbose', action='store_const', const=True)
        parser.add_argument('-vv', '--vverbose', action='store_const', const=True)
        parser.add_argument('-r', '--redownload', required=False, type=bool)
        parser.add_argument('-d', '--destination', required=False, type=str)

        args = parser.parse_args()

        if args.vverbose:
            logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

        if args.verbose:
            logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

        logging.debug(f'Parsed args. pages: {args.pages}, url: {args.url}, redownload: {args.redownload}, verbose: {args.verbose}')

        destination = create_or_get_destination_dir(args.destination)

        url, is_alternate_page = find_download_url(args.url)

        if is_alternate_page:
            url = find_episode_page_for_alternate_layout(url)

        for url_collection in find_page_download_links(url, args.pages):
            for download_link in url_collection:
                podbean_download(download_link, args.redownload, destination)

    except KeyboardInterrupt:
        exit(0)
    except HTTPError as http_er:
        logging.critical("HTTP Error", http_er)
        exit(1)


if __name__ == '__main__':
    downloader()
