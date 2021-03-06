import logging
from typing import Any

from lib.CloudStorage import CloudStorage
from lib.models.file_event import FileEvent
from lib.SendEmail import SendEmail
from lib.SendGrid import SendGrid

# Cold run code
SendGridClient = SendGrid()
CloudStorageClient = CloudStorage()


def emailer(aData: FileEvent, aContext: Any) -> None:
    """HTTP end-point for send email from files uploaded to cloud storage

    Arguments:
        aData {FileEvent} -- The file event that triggered this function
        aContext {Context} -- The context
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f"Processing {aData}")

    try:
        SendEmail(aData, SendGridClient, CloudStorageClient)
    except Exception as lException:
        logging.critical(f"Processing failed: {lException}")
