import smtplib
from email.message import EmailMessage
from datetime import datetime

# ========= CONFIGURATION =========
GMAIL_USER = "ablainpierre@gmail.com"
GMAIL_APP_PASSWORD = "votre_mot_de_passe_app"  # Mot de passe d'application Gmail
TARGET_NUMBER = " "  # Espace laissé pour le numéro
TO_EMAIL = "destinataire@email.com"  # Email de destination

# ========= FONCTION POUR RÉCUPÉRER LES SMS =========
def get_sms():
    """
   Vraie récupération de SMS
    Retourne une liste de dictionnaires de SMS
    """
    # Exemple de données
    return [
        {
            'number': '+509xxxxxxxx',
            'received': '2024-01-15 14:30:00',
            'type': 'Inbox',
            'body': 'CDM Tech, ceci est un test'
        }
    ]

# ========= CRÉER LE FICHIER DE SAUVEGARDE =========
def create_file(messages):
    time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_number = TARGET_NUMBER.replace("+", "").replace(" ", "")
    filename = f"sms_{safe_number}_{time}.txt"  # Suppression du chemin /sdcard/
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Sauvegarde SMS pour : {TARGET_NUMBER}\n")
        f.write("=" * 50 + "\n\n")
        
        for msg in messages:
            f.write(f"De : {msg.get('number', 'Inconnu')}\n")
            f.write(f"Date : {msg.get('received', 'Inconnue')}\n")
            f.write(f"Type : {msg.get('type', 'Inconnu')}\n")
            f.write(f"Message : {msg.get('body', 'Pas de message')}\n")
            f.write("-" * 40 + "\n")
    
    return filename

# ========= ENVOYER PAR EMAIL =========
def send_email(file_path):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Sauvegarde SMS - {TARGET_NUMBER}"
        msg["From"] = GMAIL_USER
        msg["To"] = TO_EMAIL
        msg.set_content("Voici votre sauvegarde filtrée des SMS.")
        
        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="text",
                subtype="plain",
                filename=file_path
            )
        
        # Utilisation de SMTP_SSL pour plus de sécurité
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        
        print("✅ Email envoyé avec succès !")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Erreur d'authentification. Vérifiez votre mot de passe d'application.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Erreur SMTP : {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {file_path}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return False

# ========= PROGRAMME PRINCIPAL =========
def main():
    global TARGET_NUMBER
    
    # Demander le numéro à l'utilisateur
    print("=== CDM Tech - Sauvegarde SMS ===")
    user_input = input("Entrez le numéro de téléphone (ex: +509xxxxxxxx) : ").strip()
    
    if user_input:
        TARGET_NUMBER = user_input
        print(f"✅ Numéro configuré : {TARGET_NUMBER}")
    else:
        print("❌ Aucun numéro saisi. Utilisation du numéro par défaut.")
    
    try:
        sms = get_sms()
        
        if not sms:
            print("❌ Aucun SMS trouvé.")
            return
        
        # Filtrage des SMS du numéro cible
        filtered_sms = [msg for msg in sms if msg.get('number', '').replace(' ', '').replace('+', '') == 
                       TARGET_NUMBER.replace(' ', '').replace('+', '')]
        
        if not filtered_sms:
            print(f"ℹ️ Aucun SMS trouvé pour le numéro {TARGET_NUMBER}")
            return
        
        file_path = create_file(filtered_sms)
        print(f"📄 Fichier créé : {file_path}")
        
        if send_email(file_path):
            print("🎉 Processus terminé avec succès !")
            
    except Exception as e:
        print(f"❌ Erreur dans le programme principal : {e}")

# ========= FONCTION ALTERNATIVE SIMPLE =========
def send_simple_email(subject, message):
    """
    Fonction alternative pour envoyer un email simple sans pièce jointe
    """
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = TO_EMAIL
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print("✅ Email simple envoyé avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email simple : {e}")
        return False

if __name__ == "__main__":
    main()
    
    # Exemple d'utilisation de la fonction simple
    # send_simple_email("CDM SMS", "À NOUS LA TECH")
