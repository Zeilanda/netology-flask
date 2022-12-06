from app import app
from views import AdvertView


app.add_url_rule("/adverts/", view_func=AdvertView.as_view("adverts"), methods=["POST"])
app.add_url_rule("/adverts/<int:advert_id>",
                 view_func=AdvertView.as_view("adverts_get"),
                 methods=["GET", "PATCH", "DELETE"])
app.run()
