from django import template
from django.http import QueryDict

register = template.Library()


# создание списка из параметорв breakfast/lunch/dinner
# полученных в форме QueryDict из GET-запроса
@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


# изменение строки запроса в соответствии с выбранными тегами
@register.filter(name='get_filter_link')
def get_filter_values(request, tag):
    new_request = request.GET.copy()

    # если тег уже есть в списке, он должен
    # выключиться при нажатии в браузере - удаляем его
    if tag.value in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.value)
        new_request.setlist('filters', filters)
    # если тега ещё нет, то добавляем его в список
    else:
        new_request.appendlist('filters', tag.value)
    # возвращаем новый запрос с помощью метода QueryDict,
    # который формирует строку запроса
    return new_request.urlencode()
