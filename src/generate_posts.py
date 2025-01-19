import os
from typing import List, Dict
import airtable
from openai import OpenAI

class InstagramPostGenerator:
    def __init__(self, airtable_api_key: str, openai_api_key: str):
        self.airtable_client = airtable.Airtable(os.getenv('AIRTABLE_BASE_ID'), 'Posts')
        self.openai_client = OpenAI(api_key=openai_api_key)
    
    def generate_caption(self, image_url: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Create engaging Instagram captions that are authentic and compelling."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Generate an engaging Instagram caption for this image."},
                        {"type": "image_url", "image_url": image_url}
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content

    def schedule_post(self, image_url: str, caption: str, scheduled_time: str):
        return self.airtable_client.create({
            'Image': image_url,
            'Caption': caption,
            'ScheduledTime': scheduled_time,
            'Status': 'Scheduled'
        })

    def process_images(self, image_urls: List[str], schedule_times: List[str]):
        for url, time in zip(image_urls, schedule_times):
            caption = self.generate_caption(url)
            self.schedule_post(url, caption, time)