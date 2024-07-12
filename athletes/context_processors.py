from .models import Category


def base(request):
    categories = Category.objects.all().order_by('name')
    actual_categories = []
    for category in categories:
        if category.athletes.filter(is_published=True):
            actual_categories.append(category)
    return {'categories': actual_categories}
