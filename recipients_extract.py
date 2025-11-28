import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

def recipients_extract():

    # --- Setup logging ---
    logger = logging.getLogger(__name__)
    logger.info("Starting recipients extract")

    # --- Load environment variables ---
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    SERVER_PREFIX = os.getenv("SERVER_PREFIX")

    if not API_KEY or not SERVER_PREFIX:
        logger.error("Missing API_KEY or SERVER_PREFIX")
        return

    # --- Configure client ---
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    # --- Find the latest campaigns JSON file ---
    data_folder = "data"
    campaign_files = [f for f in os.listdir(data_folder) if f.startswith("mailchimp_campaigns")]

    if not campaign_files:
        logger.error("No campaign extract files found.")
        return

    latest_file = max(campaign_files)  # highest timestamp
    logger.info(f"Using campaign file: {latest_file}")

    with open(os.path.join(data_folder, latest_file), "r") as f:
        campaigns_json = json.load(f)

    campaigns = campaigns_json.get("campaigns", [])

    if not campaigns:
        logger.warning("Campaigns file contains no campaigns.")
        return

    # --- Create output folder for recipients ---
    output_folder = os.path.join("data", "recipients")
    os.makedirs(output_folder, exist_ok=True)

    # --- Loop through each campaign ---
    for camp in campaigns:

        campaign_id = camp.get("id")
        status = camp.get("status")

        if not campaign_id:
            logger.warning("Campaign without ID found — skipping.")
            continue

        # Must be "sent" campaign
        if status != "sent":
            logger.info(f"Skipping campaign {campaign_id} (status = {status})")
            continue

        logger.info(f"Extracting recipients for campaign {campaign_id}")

        all_recipients = []
        offset = 0
        count = 1000  # mailchimp max

        while True:
            try:
                response = client.reports.get_campaign_recipients(
                    campaign_id=campaign_id,
                    offset=offset,
                    count=count
                )
            except ApiClientError as error:
                logger.error(f"Error pulling recipients for {campaign_id}: {error.text}")
                break

            recipients = response.get("recipients", [])
            all_recipients.extend(recipients)

            if len(recipients) < count:
                break  # no more pages

            offset += count

        # Save results
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_folder, f"recipients_{campaign_id}_{ts}.json")

        with open(output_file, "w") as f:
            json.dump(all_recipients, f, indent=2)

        logger.info(f"Saved {len(all_recipients)} recipients for {campaign_id} → {output_file}")
