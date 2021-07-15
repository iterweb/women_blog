menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_post'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]


class DataMixin:

    paginate_by = 3

    def user_context(self, **kwargs):
        context = kwargs

        site_menu = menu.copy()
        if not self.request.user.is_authenticated:
            site_menu.pop(1)

        context['menu'] = site_menu
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
