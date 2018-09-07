from django import template
from .. import models

register = template.Library()


@register.inclusion_tag("projects/_apply_btns.html", takes_context=True)
def apply_buttons(context, position):
    user = context["user"]
    user_applications = models.Application.objects.filter(
        candidate=user
    )
    response = {"position": position, "already_apply": False}
    if position in [app.position for app in user_applications]:
        response["already_apply"] = True
    return response
