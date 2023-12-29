from .models import Category


def base(request):
    categories = Category.objects.all()
    return {'categories': categories}


