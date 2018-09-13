from django import template
from .. import models

register = template.Library()


@register.inclusion_tag("projects/_apply_btns.html", takes_context=True)
def apply_buttons(context, position):
    user = context["user"]
    user_applications = models.Application.objects.filter(
        candidate=user
    )

    position_list = [app.position for app in user_applications]
    app_list = [app for app in user_applications]

    response = {"position": position, "already_apply": False}
    if position in position_list:
        response["already_apply"] = True
        response["application"] = app_list[position_list.index(position)]
        print(response['application'])
    return response
