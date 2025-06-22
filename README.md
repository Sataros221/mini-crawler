# 🌐 Internal Link Crawler

This Python script crawls all internal links of a given website, starting from a root URL. It recursively visits links up to a specified depth and saves the discovered URLs to a CSV file.

## 🧰 Features

* Recursively crawls internal links from a starting URL
* Filters out external, email, phone, and JavaScript links
* Handles both HTML and XML documents
* Detects page content type to choose appropriate parser
* Gracefully handles interruptions (`Ctrl+C`) and saves progress
* Outputs results to a `.csv` file (default is `internal_routes.csv`)
* Configurable parameters:

  * User-Agent
  * Request delay
  * Maximum depth

## 🚀 Requirements

* Python 3.6+
* `requests`
* `beautifulsoup4`
* `pandas`
* `lxml`

Install dependencies using:

```bash
pip install -r requirements.txt
```

```text
requests
beautifulsoup4
pandas
lxml
```

</details>

## ⚙️ Usage

```bash
python mini_crawler.py <starting_url> <output_file.csv>
```

### Example

```bash
python mini_crawler.py https://example.com internal_links.csv
```

You will see progress updates, and the script will automatically save results periodically and upon interruption (Ctrl+C).

## 📂 Output

The output is a `.csv` file containing a single column with all discovered internal URLs:

```csv
URL
https://example.com/
https://example.com/about
https://example.com/contact
...
```

## 🛑 Graceful Exit

Press `Ctrl+C` at any time to stop crawling. The current state will be saved to the output file automatically.

## ⚠️ Notes

* The script respects a fixed delay (`1s` by default) between requests to avoid overloading the target server.
* It limits recursion depth to `5` levels.
* Output file name and format are customizable.
* Only links within the same domain are followed.

## 📄 License

This project is released under the [MIT License](LICENSE).

---

### Feel free to contribute or report issues
