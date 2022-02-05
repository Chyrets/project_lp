from content.models import Tag, PostReaction


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


def _get_reaction(profile, content_type, object_id,):
    """Достаем реакцию из бд если она есть"""
    try:
        post_reaction = PostReaction.objects.get(profile=profile, content_type=content_type, object_id=object_id)
    except PostReaction.DoesNotExist:
        post_reaction = None

    return post_reaction


def add_remove_reaction(profile, content_type, object_id, reaction):
    """Обрабатываем реакцию пользователя"""
    post_reaction = _get_reaction(profile, content_type, object_id)

    # Если нет реакции, то создаем ее
    if not post_reaction:
        if reaction == 1:
            PostReaction.objects.create(
                profile=profile, content_type=content_type, object_id=object_id, reaction=reaction)
        else:
            PostReaction.objects.create(
                profile=profile, content_type=content_type, object_id=object_id, reaction=reaction)
    # Если есть реакция и пользователь хочет ее изменить
    elif post_reaction and post_reaction.reaction != reaction:
        PostReaction.objects.filter(
            profile=profile, content_type=content_type, object_id=object_id).update(reaction=reaction)
    # Если Есть реакция и пользователь хочет ее убрать
    else:
        PostReaction.objects.get(
            profile=profile, content_type=content_type, object_id=object_id, reaction=reaction).delete()
