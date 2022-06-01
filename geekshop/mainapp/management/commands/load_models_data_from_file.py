from django.core.management.base import BaseCommand
from mainapp.models import Product, Category
import json


class Command(BaseCommand):
    help = 'Загрузка данных из файла формата'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.products_list = {}
        self.categories_list = {}
        self.model_fields = {}

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('file_name', type=str, help='Имя файла для загрузки')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        if not file_name:
            return

        file_data = json.load(open(file_name, encoding='utf-8'))
        if not file_data:
            return

        self.load_data(file_data)

    def init_model_fields(self, model):
        """
        инициализируем сспиоск полей для модели
        :param model: класс модели
        :return:
        """
        _ = []
        for f in model._meta.fields:
            _.append(f.name)
        self.model_fields[model._meta.model_name] = _

    def get_model_by_pk(self, model, pk):
        """
        получим объект модели по первичному ключу из базы
        :param model: класс модели
        :param pk: первичный ключ
        :return: объект модели
        """
        is_new = False
        model_object = None
        if model._meta.model_name == 'category':
            model_object = self.categories_list.get(int(pk))

        if model_object == None:
            model_object = model.objects.filter(pk=int(pk)).first()

        if model_object == None:
            model_object = model()
            model_object.pk = int(pk)
            is_new = True

        return model_object, is_new

    def get_model_fields(self, model_object):
        """
        получим имеющиеся поля модели
        :param model_object: класс модели
        :return: список имен модели
        """
        if model_object._meta.model_name in self.model_fields:
            return self.model_fields[model_object._meta.model_name]
        else:
            self.init_model_fields(model_object)
            return self.model_fields[model_object._meta.model_name]

    def update_model_object(self, model_object, model_fields, model_data, is_new):
        """
        обновим объект модели установив значения различающихся полей
        :param model_object:
        :param model_fields:
        :param model_data:
        :return:
        """
        modified = False
        for field_name in model_data:
            in_value = model_data[field_name]

            if field_name == 'category':
                field_name = 'category_id'

            if in_value != getattr(model_object, field_name):
                setattr(model_object, field_name, in_value)
                modified = True

        if modified:
            model_object.save()

    def load_product(self, model_data):
        """
        загрузка данных продукта
        :param model_data: входящие данные по полям
        :return:
        """
        pk = int(model_data['pk'])
        prod, is_new = self.get_model_by_pk(Product, pk)
        self.update_model_object(prod, self.get_model_fields(Product), model_data['fields'], is_new)

    def load_category(self, model_data):
        """
        загрузка данных категории
        :param model_data: входящие данные файла по полям
        :return:
        """
        modified = False
        pk = int(model_data['pk'])

        cat, is_new = self.get_model_by_pk(Category, pk)
        self.update_model_object(cat, self.get_model_fields(Category), model_data['fields'], is_new)

        # добавим созданную категорию в кеш, чтобы постоянно не выбирать из базы
        self.categories_list[model_data['pk']] = cat

    def load_data(self, file_data):
        for model_data in file_data:
            if model_data['model'].find('Product') > 0:
                self.load_product(model_data)
            elif model_data['model'].find('Category') > 0:
                self.load_category(model_data)
