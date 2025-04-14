from dataclasses import dataclass

@dataclass
class EmailMessage:

    email: str
    subject: str
    body: str