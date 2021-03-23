# Generated by Django 3.1.4 on 2021-01-03 05:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0006_auto_20210103_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='components',
            name='id',
            field=models.CharField(default=uuid.UUID('7452eff1-53ef-4b15-9ef7-c65077edd962'), max_length=256, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='contest',
            name='id',
            field=models.CharField(default=uuid.UUID('24765e70-4d83-43d1-8780-400fddb97ec9'), max_length=256, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.CharField(default=uuid.UUID('83f50e32-771e-4f3a-85f7-d336ec40788d'), max_length=256, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='round',
            name='id',
            field=models.CharField(default=uuid.UUID('0a1a5bce-a28b-4beb-a678-18235bba1eb2'), max_length=256, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='submission',
            name='id',
            field=models.CharField(default=uuid.UUID('e4746f7e-e378-42a9-afba-0ef57b0be990'), max_length=256, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='submission',
            name='points',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.CharField(default=uuid.UUID('58678ac9-8835-4510-8c84-f1633b0cf1e0'), max_length=256, primary_key=True, serialize=False),
        ),
    ]