import email, imaplib, os, secret


def dl_bulletins(download_folder:str = "./bulletins_solde_pdf", debug:bool = False) -> None:
    # VARS
    imap_ssl_host = 'imap.gmail.com'
    username = secret.username
    password = secret.password
    MAIL_SUBJECT = 'SUBJECT "RH-TERRE/AIDDA - BMS"'
    # CONFIG
    mail = imaplib.IMAP4_SSL(imap_ssl_host)
    mail.login(username, password)
    boxes = mail.list()
    mail.select()

    # RECUP MSG
    # Récupère les mails avec le sujet du mail type
    data = mail.search(None, f'({MAIL_SUBJECT})')
    # Récupère tous les ID des mails correspondants
    mail_ids = data[1][0].split() # PEUT ETRE PATCHER SI PROBLEME ET STATUS != OK

    for mail_id in mail_ids:
        # Récupère le mail pour l'id donnée
        status, msg_data = mail.fetch(mail_id, '(RFC822)')  # récupère le mail complet
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        if debug:
            print("Date :", msg["Date"])
        
        # This part prints the content of the mail
        #if msg.is_multipart():
        #    for part in msg.walk():
        #        if part.get_content_type() == "text/plain":
        #            print(part.get_payload(decode=True).decode())
        #else:
        #    print(msg.get_payload(decode=True).decode())

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
                    if debug:
                        print(f" -> PDF téléchargé : {filename}")