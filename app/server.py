import flask
from errors import HttpError
from flask import jsonify, request, views
from models import Session, Advertisment
from schema import CreateAd, UpdateAd
from sqlalchemy.exc import IntegrityError
from tools import validate

app = flask.Flask("app")


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


def get_ad(ad_id: int):
    ad = request.session.get(Advertisment, ad_id)
    if ad is None:
        raise HttpError(404, "Ad not found")
    return ad


def add_ad(ad: Advertisment):
    try:
        request.session.add(ad)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, "Ad already exists")


class AdView(views.MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, ad_id: int):
        ad = get_ad(ad_id)
        return jsonify(ad.dict)

    def post(self):
        ad_data = validate(CreateAd, request.json)
        ad = Advertisment(**ad_data)
        add_ad(ad)
        return jsonify({"id": ad.id})

    def patch(self, ad_id: int):
        ad = get_ad(ad_id)
        ad_data = validate(UpdateAd, request.json)
        for key, value in ad_data.items():
            setattr(ad, key, value)
            add_ad(ad)
        return jsonify(ad.dict)

    def delete(self, ad_id: int):
        ad = get_ad(ad_id)
        self.session.delete(ad)
        self.session.commit()
        return jsonify({"status": "ok"})


ad_view = AdView.as_view("ad_view")

app.add_url_rule(
    "/ads/<int:ad_id>", view_func=ad_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/ads", view_func=ad_view, methods=["POST"])

if __name__ == "__main__":
    app.run()
