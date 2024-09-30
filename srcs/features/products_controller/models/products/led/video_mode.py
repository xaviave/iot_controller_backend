import os

import cv2
from django.core.files.base import ContentFile
from django.db import models

from features.products_controller.models.products.led.led_mode import LedMode


class VideoMode(LedMode):
    video = models.FileField(upload_to="videos/")
    video_low_pixel = models.ImageField(upload_to="video_low_pixels/", null=True, blank=True)

    def generate_video_low_pixel(self, video_matrix_size: tuple) -> ContentFile:
        video_path = os.path.join(self.video.storage.location, self.video.path)
        tmp_path = os.path.join(self.video.storage.location, "tmp")
        output_path = f"""{os.path.join(tmp_path, os.path.splitext(os.path.basename(self.video.name))[0])}.mp4"""

        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        cap = cv2.VideoCapture(video_path)
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), int(cap.get(5)), video_matrix_size)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            resized_frame = cv2.resize(frame, video_matrix_size)
            out.write(resized_frame)

        cap.release()
        out.release()

        with open(output_path, "rb") as video_file:
            content = video_file.read()

        os.remove(output_path)
        return ContentFile(content)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if not self.video_low_pixel:
            self.video_low_pixel.save(
                f"{os.path.splitext(os.path.basename(self.video.name))[0]}.mp4",
                self.generate_video_low_pixel(video_matrix_size=(8, 8)),
                save=False,
            )
            super().save(*args, **kwargs)
