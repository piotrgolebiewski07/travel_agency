from django import template

register = template.Library()


@register.filter
def review_word(count, language_code="en"):
    count = int(count)

    if language_code == "pl":
        if count == 1:
            return "opinia"
        if count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "opinie"
        return "opinii"

    return "review" if count == 1 else "reviews"

