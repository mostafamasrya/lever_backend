from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def default_response(status_code, data):
    return {
        "status": "success",
        "code": status_code,
        "message": None,
        "data": data,
    }


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = default_response(status_code, data)

        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["data"] = None
            try:
                response["message"] = data["detail"]
            except KeyError:
                first_item_value = None
                first_item_key = None
                for key, value in data.items():
                    if value:
                        if type(value) == list:
                            first_item_value = value[0]
                            first_item_key = key
                        else:
                            first_item_value = value
                            first_item_key = key
                        break
                response["message"] = first_item_key + " , " +first_item_value
                # if response["message"] == "user with this Phone Number of user already exists.":
                #     response["message"] = "المستخدم برقم الهاتف هذا موجود بالفعل."
                # elif response["message"] == "user with this Second Phone Number of user already exists.":
                #     response["message"] = "رقم الهاتف الثاني هذا موجود بالفعل لمستخدم آخر"
                response["data"] = data

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)