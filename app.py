from flask import Flask, request, jsonify
from geopy.distance import geodesic

app = Flask(__name__)

# Coordenadas da academia (latitude, longitude)
ACADEMIA_LOCATION = (-23.52716605064606, -46.79536548967751)  # Exemplo de localização em São Paulo

# Define o raio de proximidade em metros (100 metros, por exemplo)
MAX_DISTANCE_METERS = 100

@app.route('/confirmar-presenca', methods=['POST'])
def confirmar_presenca():
    # Recebe o JSON da requisição com a localização do usuário
    data = request.get_json()
    
    # Verifica se a localização foi enviada
    if not data or 'location' not in data:
        return jsonify({"error": "Localização não fornecida"}), 400
    
    user_location = data['location']  # Exemplo: [latitude, longitude]
    
    try:
        # Calcula a distância entre a academia e o usuário
        distance = geodesic(ACADEMIA_LOCATION, user_location).meters

        # Verifica se a distância está dentro do limite permitido
        if distance <= MAX_DISTANCE_METERS:
            return jsonify({"status": "Presença confirmada"}), 200
        else:
            return jsonify({"status": "Fora da área permitida"}), 403

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
