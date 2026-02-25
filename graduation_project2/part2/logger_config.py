"""
כל הודעה תכלול את התאריך והשעה, רמת החומרה של ההודעה ואת הטקסט של ההודעה
"""
import logging

logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
