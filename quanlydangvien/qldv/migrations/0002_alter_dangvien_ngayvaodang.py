from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qldv", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dangvien",
            name="NgayVaoDang",
            field=models.DateField(blank=True, null=True),
        ),
    ]
