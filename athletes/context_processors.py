from .models import Category


def base(request):
    categories = Category.objects.all().order_by('name')
    return {'categories': categories}


