# Liquor Store eCommerce Website
A liquor store eCommerce website made with Python and Flask


## Requirements
* Python 3.8 or higher.
* A stable Internet connection.
* Connection to a MySQL Server (e.g. using phpMyAdmin with XAMPP).
* (Optional) [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) is installed to be able to export HTML files as PDFs.


## Installation


* **Step 1:** Clone the repository with `git clone https://github.com/prime2911/liquor-store-ecommerce-website.git` or any other preferred method.


* **Step 2 (Optional):**
    - Create a [virtual environment folder](https://docs.python.org/3/library/venv.html) in the local repo.
    - Activate your virtual environment.


* **Step 3:**
    - Run `pip install -r requirements.txt` to install the dependencies.
    - After the installation process is finished, run `main.py`.
    - If there are errors, open `flask_uploads.py` look for the line `from werkzeug import secure_filename, FileStorage`, replace it with the following:
    ```
    from werkzeug.utils import secure_filename
    from werkzeug.datastructures import FileStorage
    ```
    - The website's URL is http://localhost:5000.
