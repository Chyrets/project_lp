from content.models import Tag


def add_new_tag(tag_form: str, author: str) -> list:
    """Создание новых тегов из строки введенной пользователем"""
    tag_objs = []
    tag_list = list(tag_form.replace(" ", "").split('#'))
    tag_list = [tag for tag in tag_list if len(tag) > 0]

    for tag in tag_list:
        t, created = Tag.objects.get_or_create(title=tag)
        if created:
            t.author = author
            t.save(update_fields=['author'])
        tag_objs.append(t)

    return tag_objs
