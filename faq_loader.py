import pandas as pd
import logging


def load_faqs(csv_file):

    try:

        df = pd.read_csv(csv_file)

        faq_text = ""

        for _, row in df.iterrows():

            faq_text += (
                f"Question: {row['Question']}\n"
                f"Answer: {row['Answer']}\n\n"
            )

        return faq_text

    except Exception as e:

        logging.error(f"FAQ Loading Error: {e}")

        return ""