import email, imaplib, os, utils, datetime

class MailRetriever:
    def __init__(self, username:str, password:str, imap_ssl_host:str, mail_subject:str, debug:bool):
        self.username = username
        self.password = password
        self.imap_ssl_host = imap_ssl_host
        self.mail_subject = mail_subject
        self.debug = debug

        self.mail = None
    
    def connect(self) -> bool:
        '''
        Will return false if it did not manage to connect to mailbox
        '''
        self.mail = imaplib.IMAP4_SSL(self.imap_ssl_host)
        status = self.mail.login(
            self.username,
            self.password
        )
        if status[0] == 'OK':
            if self.debug:
                boxes = self.mail.list()
                print(boxes)
            # Automatically selects 'inbox'
            self.mail.select()
            return True
        else:
            return False
    
    def fetch_messages(self):
        data = self.mail.search(None,f'({self.mail_subject})')
        status, mail_ids = data
        if status != "OK":
            return []
        return mail_ids[0].split() # Important to precise [0] because it's a single element list, error otherwise
    
    def download_payslips(self, download_folder:str):
        if not self.connect():
            raise ConnectionError("Error connecting to mailbox")
        
        mail_ids = self.fetch_messages()
        for mail_id in mail_ids:
            # Récupère le mail pour l'id donnée
            status, msg_data = self.mail.fetch(mail_id, '(RFC822)')  # récupère le mail complet
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            # msg.walk() parcourt toutes les parties du mail
            for part in msg.walk():
                # Indique si la partie est une pièce jointe
                content_disposition = part.get("Content-Disposition")
                if content_disposition and "attachment" in content_disposition:
                    # Récupération du nom du fichier
                    filename = part.get_filename()
                    # Vérification si c'est un PDF
                    if filename and filename.lower().endswith(".pdf"):
                        # Téléchargement du fichier
                        filepath = os.path.join(download_folder, filename)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        if self.debug:
                            print(f" -> PDF téléchargé : {filename}")

    def print_emails_content(self) -> None:
        if not self.connect():
            raise ConnectionError("Error connecting to mailbox")
        
        mail_ids = self.fetch_messages()
        for mail_id in mail_ids:
            # Récupère le mail pour l'id donnée
            status, msg_data = self.mail.fetch(mail_id, '(RFC822)')  # récupère le mail complet
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            # msg.walk() parcourt toutes les parties du mail
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        print(part.get_payload(decode=True).decode())
            else:
                print(msg.get_payload(decode=True).decode())
    
    def export_emails_date(self, export_folder:str = "./"):    
        emails_datetime_list = []
        if not self.connect():
            raise ConnectionError("Error connecting to mailbox")
        
        mail_ids = self.fetch_messages()
        for mail_id in mail_ids:
            # Récupère le mail pour l'id donnée
            status, msg_data = self.mail.fetch(mail_id, '(RFC822)')  # récupère le mail complet
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            if self.debug:
                print("Date :", msg["Date"])
            emails_datetime_list.append(msg["Date"])

        date_time_list_sorted = sorted(
            emails_datetime_list, 
            key= lambda x : datetime.datetime.strptime(x, utils.datetime_format()), reverse=False)
        json_datetime_list = utils.json_serialize_list(date_time_list_sorted)
        utils.write_json(f"datetime_list", json_datetime_list, export_folder)
        return emails_datetime_list