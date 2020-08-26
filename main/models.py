from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    surname = models.CharField(max_length=50, default='')
    patronymic = models.CharField(max_length=50, default='')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    platforms = models.ManyToManyField('PlatformCompany')
    positions = models.ManyToManyField('PositionCompany')
    groups = models.ManyToManyField('Group')
    email_is_validate = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        db_table = "Profile"

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class BirthDate(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    birthday = models.DateField()
    objects = models.Manager()

    class Meta:
        db_table = 'BirthDate'


class Moderator(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    class Meta:
        db_table = 'Moderator'

    def __str__(self):
        return '{} in company \"{}\"'.format(self.profile, self.company)


class SurveyWizard(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    class Meta:
        db_table = 'SurveyWizard'

    def __str__(self):
        return '{} in company \"{}\"'.format(self.profile, self.company)


class ProfilePhoto (models.Model):
    photo = models.ImageField(null=True, upload_to='media/images/', blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        # До удаления записи получаем необходимую информацию
        storage, path = self.photo.storage, self.photo.path
        # Удаляем сначала модель ( объект )
        super(ProfilePhoto, self).delete(*args, **kwargs)
        # Потом удаляем сам файл
        storage.delete(path)

    class Meta:
        db_table = "Profile photo"

    def __str__(self):
        return "Profile: {}".format(self.profile)


class VerificationCode (models.Model):
    email = models.EmailField(default='')
    code = models.CharField(max_length=100, default='')
    objects = models.Manager()

    class Meta:
        db_table = "Verification code"

    def __str__(self):
        return self.code


class Invitation (models.Model):
    TYPE_CHOICES = [
        (0, 'team'),
        (1, 'company'),
    ]

    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='team')
    invitation_group_id = models.IntegerField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    initiator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    objects = models.Manager()

    class Meta:
        db_table = "Invitation"


class Company(models.Model):
    name = models.CharField(max_length=20)
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='+')
    key = models.CharField(max_length=36, unique=True, default='')
    description = models.CharField(max_length=150, default='')
    objects = models.Manager()

    class Meta:
        db_table = "Company"

    def __str__(self):
        return 'Company name: {}, Owner: {}'.format(self.name, self.owner)


class PlatformCompany(models.Model):
    name = models.CharField(max_length=100, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = "Platforms in company"

    def __str__(self):
        return '{}'.format(self.name)


class PositionCompany (models.Model):
    name = models.CharField(max_length=100, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = "Positions in company"

    def __str__(self):
        return '{}'.format(self.name)


class Group(models.Model):
    name = models.CharField(max_length=20, default='')
    description = models.CharField(max_length=150, default='')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+', null=True)
    key = models.CharField(max_length=36, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    class Meta:
        db_table = "Groups"

    def __str__(self):
        return "Group \"{}\" with owner \"{}\"".format(self.name, self.owner)


class TemplatesPoll(models.Model):
    name_poll = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True)
    is_general = models.BooleanField(default=False)
    owner = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Questions')
    color = models.CharField(max_length=20, null=True)  # purple, red, blue, None
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        questions = self.questions.all()
        for question in questions:
            question.delete()
        super(TemplatesPoll, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'Template'

    def __str__(self):
        return self.name_poll


class Poll(models.Model):
    key = models.CharField(max_length=100, default='')
    initiator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+', null=True)
    target = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name_poll = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500, null=True)
    count_passed = models.IntegerField(default=0)
    creation_date = models.DateField(null=True)
    color = models.CharField(max_length=20, null=True)  # purple, red, blue, None
    questions = models.ManyToManyField('Questions')
    is_submitted = models.BooleanField(default=False)
    new_template = models.OneToOneField(TemplatesPoll, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        # TODO удаление ответов
        self.questions.all().delete()
        self.answers_set.all().delete()
        super(Poll, self).delete(*args, **kwargs)

    class Meta:
        db_table = "Poll"

    def __str__(self):
        return "{} : {}".format(self.name_poll, self.creation_date)


class NeedPassPoll(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_viewed = models.BooleanField(default=False)
    is_rendered = models.BooleanField(default=False)
    version = models.IntegerField(default=0)
    objects = models.Manager()

    class Meta:
        db_table = "RespondentPoll"

    def __str__(self):
        return 'Опрос: {}, Пользователь: {}, Просмотрен: {}'.format(self.poll, self.profile, self.is_viewed)


class CreatedPoll(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    poll = models.OneToOneField('Poll', on_delete=models.CASCADE)
    is_viewed = models.BooleanField(default=False)
    is_rendered = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        db_table = "Created polls"

    def __str__(self):
        return 'Опрос: {}, Пользователь: {}'.format(self.poll, self.profile)


class Questions(models.Model):
    settings = models.OneToOneField('Settings', on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=100)
    version = models.IntegerField(default=0)
    ordinal_number = models.IntegerField(default=0)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.settings.delete()
        super(Questions, self).delete(*args, **kwargs)

    class Meta:
        db_table = "Questions"
        ordering = ['ordinal_number']

    def __str__(self):
        return self.text


class Settings(models.Model):
    TYPE_CHOICES = [
        ('small_text', 0),
        ('radio', 1),
        ('range', 2),
        ('checkbox', 3),
    ]

    type = models.CharField(choices=TYPE_CHOICES, default='range', max_length=10)
    min = models.IntegerField(null=True)
    max = models.IntegerField(null=True)
    step = models.IntegerField(null=True)
    answer_choice = models.ManyToManyField('AnswerChoice')
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.answer_choice.all().delete()
        super(Settings, self).delete(*args, **kwargs)

    class Meta:
        db_table = "Questions settings"


class AnswerChoice(models.Model):
    text = models.CharField(max_length=50, default='')
    objects = models.Manager()

    class Meta:
        db_table = "AnswerChoice"

    def __str__(self):
        return self.text


class Answers(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    choices = models.ManyToManyField('Choice')
    range_sum = models.IntegerField(default=0)
    open_answer = models.ManyToManyField('OpenQuestion')
    count_profile_answers = models.IntegerField(default=0)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.choices.all().delete()
        self.open_answer.all().delete()
        super(Answers, self).delete(*args, **kwargs)

    class Meta:
        db_table = "Answer"


class OpenQuestion(models.Model):
    text = models.CharField(max_length=100, default='')
    objects = models.Manager()

    class Meta:
        db_table = 'OpenQuestion'

    def __str__(self):
        return self.text


class Choice(models.Model):
    answer_choice = models.OneToOneField(AnswerChoice, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    objects = models.Manager()

    class Meta:
        db_table = 'Choice'

    def __str__(self):
        return self.answer_choice


class TestTable(models.Model):
    code = models.CharField(max_length=100, default='')

    class Meta:
        db_table = "TestTable"
