# Generated by Django 4.1.5 on 2023-01-29 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Api", "0002_alter_category_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Api.order"
            ),
        ),
    ]
