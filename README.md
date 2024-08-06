# SitemapPY
SitemapPY is a simple Python script that creates a sitemap for your website

# Use this script at your own discretion, only on websites that you own. I am not responsible for any damage, loss of revenue, or downtime caused by improper usage of this script.

## Features

- Crawls and extracts URLs up to a specified depth.
- Avoids duplicate requests and follows internal links only.
- Handles retries with exponential backoff for robustness.
- Generates an XML sitemap with priority levels based on depth.

## Dependencies

- `requests`
- `beautifulsoup4`

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/KawaiiBunga/SitemapPY.git
    cd SitemapPY
    ```

2. **Create a virtual environment (optional but recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Edit the script (sitemappy.py) to set your root URL and output filename:**

    Line 98 -
    ```python
    sitemapGenerator = SitemapGenerator("https://www.example.com", "sitemap.xml") # No trailing / !
    ```
    Line 99 -
    ```python
    sitemapGenerator.crawl("https://www.google.com", 0) # No trailing / !
    ```

2. **Run the script:**
    ```sh
    python sitemappy.py
    ```

3. **Your sitemap will be saved to the specified XML file (`sitemap.xml` in this example).**

## Configuration

- **`max_depth`**: Maximum depth to crawl (default is 2).
- **`max_workers`**: Number of concurrent threads for crawling (default is 1 to avoid rate limiting).

## Example

To generate a sitemap for `https://www.google.com` and save it as `sitemap.xml`, configure and run the script as shown in the usage section.

## Issues

- Do NOT set the concurrent workers too high or the wait time too low, as this script has the ability to get you rate limited SUPER fast. Use this script at your own discretion, only on websites that you own.
- Some websites might need proper headers to be accessed. I do not plan on updating this soon as this script works for my website. If someone wants to implement better headers, open an issue/merge request.

## Credits

This script is evolved from this AMAZING step-by-step guide by Sylvian Saurel to creating a sitemap generator for any website in python. Go check it out:
`https://hackernoon.com/a-step-by-step-guide-to-creating-a-sitemap-generator-in-python`

# If you are unsure of what you are doing, please do NOT change depth, concurrent workers, or time.sleep() events.
