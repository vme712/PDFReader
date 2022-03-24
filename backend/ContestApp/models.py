from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from backend.models import DeleteModelMixin


class IdentifierChoices(DjangoChoices):
    inn = ChoiceItem('inn', 'ИНН')
    ogrn = ChoiceItem('ogrn', 'ОГРН')
    sum_pay = ChoiceItem('sum_pay', 'Призовая сумма')
    request_sum_pay = ChoiceItem('request_sum_pay', 'Запрашиваемая сумма')
    ball = ChoiceItem('ball', 'Баллы')


class ContestModel(DeleteModelMixin, models.Model):
    name = models.TextField('Название конкурса')
    link = models.TextField('Ссылка на конкурс')
    add_user = models.ForeignKey('UserProfileApp.User', on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Конкурс'
        verbose_name_plural = 'Конкурсы'

    def __str__(self):
        return self.name


class ContestResultModel(DeleteModelMixin, models.Model):
    contest = models.ForeignKey('ContestApp.ContestModel', on_delete=models.CASCADE, verbose_name='Конкурс')
    file = models.ForeignKey('FilesApp.FileModel', on_delete=models.CASCADE, verbose_name='Файл для распознавания')
    add_user = models.ForeignKey('UserProfileApp.User', on_delete=models.CASCADE, verbose_name='Автор')
    is_draft = models.BooleanField('Черновик', default=True)

    class Meta:
        verbose_name = 'Результат конкурса'
        verbose_name_plural = 'Результаты конкурса'

    def __str__(self):
        return f'{self.contest} - {self.is_draft}'


class ContestResultConfigModel(DeleteModelMixin, models.Model):
    contest_result = models.ForeignKey('ContestApp.ContestResultModel', on_delete=models.CASCADE,
                                       verbose_name='Результаты конкурса')
    is_check = models.BooleanField('Статус проверки конфига', default=False)

    identifier = models.CharField('На основе какого поля производить проверку при переносах строки на новую страницу',
                                  max_length=15, choices=IdentifierChoices.choices)
    page_start = models.PositiveSmallIntegerField('Номер страницы в документе с которой нужно распознавать')
    page_end = models.PositiveSmallIntegerField('Номер страницы в документе до которой нужно распознавать')
    is_winner_table = models.BooleanField('Статус данного фрагмента таблицы, победитель ли тут')

    direction_col_num = models.PositiveSmallIntegerField('Номер столбца с направлением', default=None, null=True)
    org_name_col_num = models.PositiveSmallIntegerField('Номер столбца с названием организации', default=None,
                                                        null=True)
    project_name_col_num = models.PositiveSmallIntegerField('Номер столбца с названием проекта', default=None,
                                                            null=True)
    ball_col_num = models.PositiveSmallIntegerField('Номер столбца с баллами', default=None, null=True)
    request_sum_pay_col_num = models.PositiveSmallIntegerField('Номер столбца с запрашиваемой суммой', default=None,
                                                               null=True)
    inn_col_num = models.PositiveSmallIntegerField('Номер столбца с ИНН', default=None, null=True)
    ogrn_col_num = models.PositiveSmallIntegerField('Номер столбца с ОГРН', default=None, null=True)

    class Meta:
        verbose_name = 'Настройка для распознания результата конкурса'
        verbose_name_plural = 'Настройки для распознания результата конкурса'

    def __str__(self):
        return f'{self.contest_result.id}: {self.page_start}-{self.page_end}'


class ResultModel(DeleteModelMixin, models.Model):
    file_row = models.ManyToManyField('FilesApp.FileModel', verbose_name='Файлы строк')
    contest_result = models.ForeignKey('ContestApp.ContestResultModel', on_delete=models.CASCADE,
                                       verbose_name='Результаты конкурса')
    is_verified = models.BooleanField('Статус проверки', default=False)
    is_download = models.BooleanField('Статус выгрузки', default=False)

    page = models.CharField('Страница', max_length=255)
    inn = models.CharField('ИНН', max_length=255, default='', null=True)
    ogrn = models.CharField('ОГРН', max_length=255, default='', null=True)
    sum_pay = models.CharField('Сумма выплаты', max_length=255, default='', null=True)
    request_sum_pay = models.CharField('Запрашиваемая сумма', max_length=255, default='', null=True)
    ball = models.CharField('Балл', max_length=255, default='', null=True)
    direction = models.TextField('Направление', default='', null=True)
    org_name = models.TextField('Название организации', default='', null=True)
    project_name = models.TextField('Название проекта', default='', null=True)
    is_winner = models.BooleanField('Победитель', default=True)

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    def __str__(self):
        return f'{self.contest_result.id} - {self.page}'
