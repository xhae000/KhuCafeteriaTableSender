import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()



EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS").split(",")

SMTP_SERVER = "smtp.naver.com"
SMTP_PORT = 587

# 경희대학교 학생회관 식당 주간메뉴 페이지 URL
MENU_PAGE_URL = "https://coop.khu.ac.kr/food-menu/%ed%95%99%ec%83%9d%ed%9a%8c%ea%b4%80-%ec%8b%9d%eb%8b%b9-%ec%a3%bc%ea%b0%84%eb%a9%94%eb%89%b4/"

def get_menu_image_url():
    """주간 식단표 이미지 URL을 추출합니다."""
    response = requests.get(MENU_PAGE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('data-src')
        print(src)
        if src and '식단' in src:
            return src
    return None

from email.mime.text import MIMEText  # 위에 추가 필요

def send_email_with_image(image_url):
    """식단표 이미지를 첨부하여 이메일을 전송합니다."""
    # 이미지 다운로드
    image_response = requests.get(image_url)
    image_data = image_response.content

    # 이메일 메시지 구성
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = ", ".join(EMAIL_RECIPIENTS)
    msg['Subject'] = "🦊🍴😺🍴 이번 주 학생회관 학식 식단표 🍚"

    # 본문 텍스트 추가
    body_text = "매주 월요일 오전 8시에 자동으로 발송해줄게!! 😊"
    msg.attach(MIMEText(body_text, "plain"))

    # 이미지 첨부
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(image_data)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename="menu.png")
    msg.attach(part)

    # 메일 전송
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())
        print("이메일 전송 완료")

def main():
    image_url = get_menu_image_url()
    if not image_url:
        print("식단표 이미지를 찾을 수 없습니다.")
        return

    send_email_with_image(image_url)

if __name__ == "__main__":
    main()
