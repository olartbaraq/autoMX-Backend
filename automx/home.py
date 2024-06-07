from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from decouple import config
import requests


bp = Blueprint("home", __name__, url_prefix="/home")

key = config("OPEN_WEATHER_KEY")


@bp.route("/protected", methods=["POST"])
@jwt_required()
def protected():
    if request.method == "POST":
        data = request.get_json()

        # Check if the data is valid
        if not data:
            return jsonify({"error": "No data provided"}), 400

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        error = None

        if not latitude:
            error = "Latitude is required"
        elif not longitude:
            error = "Longitude is required"

        if error is None:
            # talk to weather api to get necessary values

            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={key}&units=metric"
            with requests.Session() as session:
                res = session.get(url=url)
                data = res.json()

            # talk to unsplash
            client_id = config("ACCESS_KEY")
            query = data["current"]["weather"][0]["main"]
            url = f"https://api.unsplash.com/search/photos/?client_id=586839?query={query}"
            print(url)
            with requests.Session() as session:
                res = session.get(url=url)
                data2 = res.json()

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Weather info retrieved successfully",
                        "data": {
                            "location": data["timezone"],
                            "temperature": data["current"]["temp"],
                            "temp_feels_like": data["current"]["feels_like"],
                            "weather": data["current"]["weather"][0]["main"],
                            "weather_description": data["current"]["weather"][0][
                                "description"
                            ],
                            "image": data2,
                        },
                    }
                ),
                200,
            )

        return jsonify({"status": "failure", "error": f"{error}"}), 400
