from typing import List, Union
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
import requests
from urllib.parse import urlparse
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
}

def check_file_empty(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return bool(data)
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        return False


def is_amazon_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.netloc.endswith('.amazon.com')


def extract_description(page_content: BeautifulSoup) -> str:
    descriptions = page_content.find_all(class_="a-list-item")[:50]
    description_text = ""
    for description in descriptions:
        description_text += description.get_text().strip()
    return description_text


def extract_image_urls(page_content: BeautifulSoup) -> List[str]:
    img_tag_wrapper = page_content.find_all(class_="imgTagWrapper")
    image_urls = []

    if img_tag_wrapper:
        for img_tag in img_tag_wrapper:
            image_element = img_tag.find("img")

            if image_element:
                img_attr = image_element.attrs
                image_url = img_attr.get('src')
                image_urls.append(image_url)
    else:
        image_urls.append("No Valid Data for Images!!")
    return image_urls


def extract_price_from_url(product_url: str) -> float:
    page = requests.get(product_url, headers=HEADERS)
    page_content = BeautifulSoup(page.content, "html.parser")
    price = float(page_content.find(class_="a-offscreen").get_text().replace("$", "").strip())
    return price


def scrape_amazon_product_url(product_url: str) -> Union[bool, List[dict]]:
    if not is_amazon_url(product_url):
        return False

    page = requests.get(product_url, headers=HEADERS)
    page_content = BeautifulSoup(page.content, "html.parser")

    title = page_content.find(id="productTitle").get_text().strip()
    price = extract_price_from_url(product_url)
    rating_count = page_content.find(id="acrCustomerReviewText").get_text().strip()
    description = extract_description(page_content)
    image_urls = extract_image_urls(page_content)

    product_data = [
        {
            "name": title,
            "price": price,
            "rating_count": rating_count,
            "description": description,
            "images": image_urls,
            "product_url": product_url
        }
    ]
    return product_data

def tracked_product_email_confirmation(product_name, product_price, product_url, email):
        subject = f"Price Drop Alert: {product_name} is now ${product_price}!"
        body = f"""
        <html>
            <body>
                <p>Dear Customer,</p>
                <p>We're excited to inform you that the product you expressed interest in, <strong>{product_name}</strong>, is now being actively tracked by our PriceWize system! This means you will receive timely updates regarding any changes in its price.</p>
                
                <p>Here are the details of the tracked product:</p>
                <ul>
                    <li><strong>Product Name:</strong> {product_name}</li>
                    <li><strong>Product URL:</strong> {product_url}</li>
                    <li><strong>Tracked Price:</strong> ${product_price}</li>
                </ul>
                
                <p>You can expect to receive notifications if there are any price drops or noteworthy changes. Our goal is to ensure you stay informed about the best deals available for the products you love.</p>
                
                <p>If you have any questions or concerns, feel free to reach out to us. Thank you for using PriceWize to find the best prices on your favorite products!</p>
                
                <p>Best regards,<br>PriceWise</p>
            </body>
        </html>
        """
        
        sender_email = "pricetracker23@gmail.com"
        password = "mltj sdrk ibpq mjoe"

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'html'))

        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, email, msg.as_string())
            print(f"Email sent successfully.")
            return True
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")
            return False