from sqlalchemy.orm import Session
from ..database import TrackedProducts, SessionLocal
from fastapi import Depends
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import requests
import pandas as pd
import os

class PriceTrackerCron:
    def __init__(self, db: Session = Depends(SessionLocal)):
        self.db = db
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
        }

    @staticmethod
    def is_amazon_url(url: str) -> bool:
        parsed_url = urlparse(url)
        return parsed_url.netloc.endswith('.amazon.com')

    def get_all_tracked_products(self):
        try:
            return self.db.query(TrackedProducts).all()
        finally:
            self.db.close()

    def send_email_price_down(self, product_name, product_price, receiver_email, price_diff):
        subject = f"Price Drop Alert: {product_name} is now ${product_price}!"
        body = f"""
        <html>
            <body>
                <p>Dear User,</p>
                <p>We're excited to inform you that the price of {product_name} has dropped!</p>
                <p>The new price is ${product_price}, which is ${price_diff:.2f} lower than before.</p>
                <p>Hurry up and take advantage of this great deal!</p>
                <p>Best regards,<br>Your Price Tracker</p>
            </body>
        </html>
        """
        
        sender_email = "yenulsanmika7@gmail.com"
        password = "yenSan7%"

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'html'))

        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Email sent successfully.")
            return True
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")
            return False

    def save_product_price_history(self, product_name, current_time, product_price):
        csv_folder = 'products_price_history'
        csv_filename = f'{product_name}_price_history.csv'
        csv_path = os.path.join(csv_folder, csv_filename)

        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)

        if os.path.isfile(csv_path):
            product_price_history = pd.read_csv(csv_path)
        else:
            product_price_history = pd.DataFrame(columns=['Time', 'Price'])

        new_data = {'Time': current_time, 'Price': product_price}
        product_price_history = product_price_history.append(new_data, ignore_index=True)
        product_price_history.to_csv(csv_path, index=False)

        print(f"Price data saved to '{csv_path}'.")
        return True
    
    def track_prices(self):
        tracked_products = self.get_all_tracked_products()

        for product in tracked_products:
            if self.is_amazon_url(product.url):
                product_url = product.url

                try:
                    page = requests.get(product_url, headers=self.headers)
                    page_content = BeautifulSoup(page.content, "html.parser")
                    curr_price = float(page_content.find(class_="a-offscreen").get_text().replace("$", "").strip())
                    
                    if curr_price is not None and curr_price < product.price:
                        product.price = curr_price
                        price_diff = product.price - curr_price

                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        self.db.commit()

                        # Sending an email to tracked email user 
                        success = self.send_email_price_down(product.name, curr_price, product.email, price_diff)
                        # Save product price history in csv
                        if success:
                            self.save_product_price_history(product.name, current_time, curr_price)
                        
                except requests.RequestException as e:
                    print(f"Error updating price for {product.name}: {e}")

pricetracker_tasks = PriceTrackerCron()