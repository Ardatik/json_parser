from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Product(models.Model):
    class AvailabilityStatus(models.TextChoices):
        IN_STOCK = "In Stock"
        OUT_OF_STOCK = "Out of Stock"
        LOW_STOCK = "Low Stock"

    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )
    discount_percentage = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Процент скидки",
    )
    rating = models.DecimalField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Рейтинг",
    )
    stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        verbose_name="Остаток на складе",
    )
    tags = models.ManyToManyField(Tag, blank=True)
    brand = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Бренд"
    )
    sku = models.CharField(max_length=100, unique=True, verbose_name="Артикул")
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Вес"
    )
    warranty_information = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Гарантия"
    )
    shipping_information = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Доставка"
    )
    availability_status = models.CharField(
        max_length=20, choices=AvailabilityStatus.choices
    )
    minimum_order_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Минимальное количество для заказа",
    )
    images = models.JSONField(default=list, verbose_name="Изображения")
    thumbnail = models.URLField(verbose_name="Миниатюра")
    category = models.CharField(max_length=250, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    @property
    def final_price(self):
        if self.discount_percentage is not None:
            return self.price * (1 - self.discount_percentage / 100)
        return self.price

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["price"]),
            models.Index(fields=["brand"]),
        ]


class Dimension(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="dimensions",
        verbose_name="Товар",
    )
    width = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ширина")
    height = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Высота")
    depth = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Глубина")

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="reviews"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Оценка"
    )
    comment = models.TextField(verbose_name="Комментарий")
    reviewer_name = models.CharField(max_length=250, verbose_name="Имя")
    reviewer_email = models.EmailField(verbose_name="Email")
    date = models.DateTimeField(verbose_name="Дата отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ("product", "reviewer_email")
