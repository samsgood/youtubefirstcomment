import os
import json
from flask import Flask, request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

# Variables d'environnement
CLIENT_SECRETS_FILE = "oauth2.json"
WEBHOOK_VERIFICATION_TOKEN = "votre_token_de_verification"
CHANNEL_ID = "@marouane53Too"

# Créer un objet service YouTube
youtube = build('youtube', 'v3', credentials=Credentials.from_authorized_user_file(CLIENT_SECRETS_FILE))

# Définir le point de terminaison pour les notifications de push (Webhooks)
@app.route('/webhook', methods=['POST'])
def youtube_webhook():
    request_data = request.json
    if 'challenge' in request_data:
        # Vérification de la configuration initiale du Webhook
        return request_data['challenge'], 200

    if 'type' in request_data and request_data['type'] == 'videoPubished':
        # Réagir à la notification de publication de la vidéo
        video_id = request_data['videoId']
        comment_on_video(video_id, "Votre commentaire automatique ici.")

    return '', 200

# Fonction pour poster un commentaire sur une vidéo YouTube
def comment_on_video(video_id, comment_text):
    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {"snippet": {"textOriginal": comment_text}}
            }
        }
    )
    response = request.execute()
    print(response)

if __name__ == '__main__':
    app.run(debug=True)
