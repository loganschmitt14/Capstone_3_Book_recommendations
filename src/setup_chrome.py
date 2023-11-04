import requests
import zipfile
import os
import shutil
import sys

# Detect platform
platform = sys.platform
if platform == 'linux' or platform == 'linux2':
    chrome_url = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chrome-linux64.zip'
    driver_url = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chromedriver-linux64.zip'
elif platform == 'darwin':
    # Assuming you have a mac with intel x64
    chrome_url = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/mac-x64/chrome-mac-x64.zip'
    driver_url = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/mac-x64/chromedriver-mac-x64.zip'
elif platform == 'win32' or platform == 'cygwin':
    chrome_url = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/win32/chrome-win32.zip'
    driver_url = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/win32/chromedriver-win32.zip'
else:
    raise ValueError('Unsupported operating system.')

# Define a function to download and extract files
def download_and_extract(url, extract_to='.'):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    # Extract the zip file
    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    # Clean up the zip file
    os.remove(local_filename)

# Create directories for Chrome and ChromeDriver
chrome_dir = 'chrome_for_testing'
driver_dir = 'chromedriver'
os.makedirs(chrome_dir, exist_ok=True)
os.makedirs(driver_dir, exist_ok=True)

# Download and extract Chrome for Testing
print('Downloading Chrome for Testing...')
download_and_extract(chrome_url, chrome_dir)

# Download and extract ChromeDriver
print('Downloading ChromeDriver...')
download_and_extract(driver_url, driver_dir)

print('Chrome for Testing and ChromeDriver have been installed.')
