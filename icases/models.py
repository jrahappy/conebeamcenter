from django.db import models
from django.urls import reverse
from accounts.models import User as CustomUser


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(
        choices=[
            ("Service", "Service"),
            ("Equipment", "Equipment"),
            ("Instrument", "Instrument"),
            ("Consumable", "Consumable"),
            ("Others", "Others"),
        ],
        max_length=20,
        default="Draft",
    )
    description = models.TextField()
    unitprice = models.DecimalField(max_digits=10, decimal_places=2)
    taxcode = models.CharField(max_length=100)
    taxrate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        choices=[
            ("Draft", "Draft"),
            ("Opened", "Opened"),
            ("Closed", "Closed"),
        ],
        max_length=20,
        default="Opened",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.name)

    class Meta:
        ordering = ["category", "name"]


class ICase(models.Model):
    CATEGORY_CHOICES = [
        ("Normal", "Normal"),
        ("Big", "Big"),
    ]
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_icases", null=True
    )
    provider = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="provider_icases", null=True
    )
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=20, default="Normal"
    )
    target_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    name = models.CharField(max_length=100)
    bodypart = models.CharField(max_length=100, default="", null=True, blank=True)
    description = models.TextField()

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Confirmed", "Confirmed"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
    ]

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        default="Draft",
    )
    tags = models.CharField(max_length=100, default="", null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    appointed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    case_start = models.DateTimeField(null=True, blank=True)
    case_end = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="owner", null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.name)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("icases:icase-detail", kwargs={"pk": self.pk})


class ICaseDetail(models.Model):
    icase = models.ForeignKey(ICase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default="", null=True, blank=True)
    quantity = models.IntegerField(default=1)
    unitprice = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} - {1}".format(self.icase, self.product)

    class Meta:
        ordering = ["created_at"]


FILETYPE_CHOICES = [
    ("Image", "Image"),
    ("Video", "Video"),
    ("Document", "Document"),
    ("Others", "Others"),
]
MODALITY_CHOICES = [
    ("IO Camera", "IOCam"),
    ("IO Xray", "IOXray"),
    ("Panoramic", "Pano"),
    ("CBCT", "CBCT"),
    ("Cephalometric", "Ceph"),
    ("Camera", "Camera"),
    ("Others", "Others"),
]
TOOTH_CHOICES = [
    ("1", "01"),
    ("2", "02"),
    ("3", "03"),
    ("4", "04"),
    ("5", "05"),
    ("6", "06"),
    ("7", "07"),
    ("8", "08"),
    ("9", "09"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
    ("16", "16"),
    ("17", "17"),
    ("18", "18"),
    ("Others", "Others"),
]


def upload_to_icase_id_folder(instance, filename):
    icase_id = instance.icase.id
    new_filename = f"icase_{icase_id}/{filename}"
    return new_filename


class ICaseImage(models.Model):
    icase = models.ForeignKey(ICase, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=upload_to_icase_id_folder, null=True, blank=True
    )
    part = models.CharField(max_length=100, default="", null=True, blank=True)
    bodypart = models.CharField(choices=TOOTH_CHOICES, max_length=10, default="Others")
    filetype = models.CharField(max_length=100, default="")
    modality = models.CharField(
        choices=MODALITY_CHOICES, max_length=20, default="IOCam"
    )
    description = models.CharField(max_length=100, default="", null=True, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} - {1}".format(self.icase, self.image)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ["created_at"]


class TPlan(models.Model):
    icase = models.ForeignKey(ICase, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    terms = models.IntegerField()
    visits = models.IntegerField()
    status = models.CharField(
        choices=[
            ("Draft", "Draft"),
            ("Processing", "Processing"),
            ("Closed", "Closed"),
        ],
        max_length=100,
        default="Draft",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.name)

    class Meta:
        ordering = ["created_at"]


class TPlanDetail(models.Model):
    tplan = models.ForeignKey(TPlan, on_delete=models.CASCADE)
    bodypart = models.CharField(max_length=100)
    treatmentcode = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    description = models.TextField()
    unitprice = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    totalprice = models.DecimalField(max_digits=10, decimal_places=2)
    taxcode = models.CharField(max_length=100)
    taxrate = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    sortingorder = models.IntegerField()
    status = models.CharField(
        choices=[
            ("Draft", "Draft"),
            ("Processing", "Processing"),
            ("Closed", "Closed"),
        ],
        max_length=20,
        default="Draft",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.name)

    class Meta:
        ordering = ["created_at"]
