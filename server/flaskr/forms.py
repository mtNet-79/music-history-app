from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, AnyOf, URL, Optional

# from app import Genre
# from enum import Enum


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id',
        validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id',
        validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class ComposerForm(FlaskForm):
    from .models import Period, Title, Composer, Performer

    name = StringField(
        'name', validators=[DataRequired()]
    )
    born = IntegerField(
        'born', validators=[DataRequired()]
    )
    deceased = IntegerField(
        'deceased', validators=[DataRequired()]
    )
    nationality = StringField(
        'nationality', validators=[DataRequired()]
    )
    period = SelectField(
        'period',
        choices=[(period.id)(period.name) for period in Period.query.all()]
    )
    performers = SelectField(
        'period',
        choices=[(performer.id)(performer.name)
                 for performer in Performer.query.all()]
    )
    titles = SelectField(
        'title',
        choices=[(title.id)(title.name) for title in Title.query.all()]

    )
    compositions = StringField("compositions")
    contemporaries = SelectField(
        'contemporary',
        choices=[(contemporary.id)(contemporary.name)
                 for contemporary in Composer.query.all()]

    )

    # def __init__(self, genres_choices: list = None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if genres_choices:
    #         self.genres.choices = genres_choices


class PerformerForm(FlaskForm):
    from .models import Period, Title, Composer, Performer

    name = StringField(
        'name', validators=[DataRequired()]
    )
    born = IntegerField(
        'born', validators=[DataRequired()]
    )
    deceased = IntegerField(
        'deceased', validators=[DataRequired()]
    )
    nationality = StringField(
        'nationality', validators=[DataRequired()]
    )
    period = SelectField(
        'period',
        choices=[(period.id)(period.name) for period in Period.query.all()]
    )
    composers = SelectField(
        'period',
        choices=[(composers.id)(composers.name)
                 for composers in Composer.query.all()]
    )
    titles = SelectField(
        'title',
        choices=[(title.id)(title.name) for title in Title.query.all()]

    )
    recordings = StringField("recordings", validators=[Optional()])
    rating = SelectField(
        'rating',
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ]
    )
