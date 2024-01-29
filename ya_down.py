import sys, requests
from tqdm import tqdm

API_ENDPOINT = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'

url = sys.argv[1]

def _get_real_direct_link(sharing_link):
    pk_request = requests.get(API_ENDPOINT.format(sharing_link))
    
    # Returns None if the link cannot be "converted"
    return pk_request.json().get('href')


def _extract_filename(direct_link):
    for chunk in direct_link.strip().split('&'):
        if chunk.startswith('filename='):
            return chunk.split('=')[1]
    return None


def download_yadisk_link(sharing_link, filename=None):
    direct_link = _get_real_direct_link(sharing_link)
    if direct_link:
        # Try to recover the filename from the link
        filename = filename or _extract_filename(direct_link)
        
        download = requests.get(direct_link, stream=True)
        total_size = int(download.headers.get("Content-Length", 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)

        with open(filename, 'wb') as out_file:
            for data in download.iter_content(block_size):
                progress_bar.update(len(data))
                out_file.write(data)
    else:
        print('Failed to download "{}"'.format(sharing_link))

download_yadisk_link(url)
