import os
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO,
                    filename='example.log')

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "РќРµ С…РѕС‡Сѓ.",
                "РќРµ Р±СѓРґСѓ.",
                "РћС‚СЃС‚Р°РЅСЊ!",
            ]
        }
        res['response']['text'] = 'РџСЂРёРІРµС‚! РљСѓРїРё СЃР»РѕРЅР°!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'Р»Р°РґРЅРѕ',
        'РєСѓРїР»СЋ',
        'РїРѕРєСѓРїР°СЋ',
        'С…РѕСЂРѕС€Рѕ'
    ]:
        res['response']['text'] = 'РЎР»РѕРЅР° РјРѕР¶РЅРѕ РЅР°Р№С‚Рё РЅР° РЇРЅРґРµРєСЃ.РњР°СЂРєРµС‚Рµ!'
        res['response']['end_session'] = True
        return

    res['response']['text'] = \
        f"Р’СЃРµ РіРѕРІРѕСЂСЏС‚ '{req['request']['original_utterance']}', Р° С‚С‹ РєСѓРїРё СЃР»РѕРЅР°!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Р›Р°РґРЅРѕ",
            "url": "https://market.yandex.ru/search?text=СЃР»РѕРЅ",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # http://127.0.0.1:8080/