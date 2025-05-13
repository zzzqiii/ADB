from django.db import models
from django.urls import reverse

class AlgaeSpecies(models.Model):
    name = models.CharField(max_length=255, unique=True)  # The species name (e.g., Microcystis aeruginosa)
    phylum = models.CharField(max_length=100, blank=True, null=True)  # 门
    class_name = models.CharField(max_length=100, blank=True, null=True)  # 纲
    order = models.CharField(max_length=100, blank=True, null=True)  # 目
    family = models.CharField(max_length=100, blank=True, null=True)  # 科
    environment = models.TextField(blank=True, null=True)  # 环境描述
    risk = models.CharField(max_length=50, blank=True, null=True)  # 毒害特性
    description = models.TextField(blank=True, null=True)  # Species-level description
    description_source = models.URLField(max_length=200, blank=True, null=True)  # Description source URL
    image = models.ImageField(upload_to='algae_images/', null=True, blank=True)  # 图片的URL
    image_source = models.URLField(max_length=200, blank=True, null=True)  # 图片来源的URL
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Algae species'

class AlgaeStrain(models.Model):
    species = models.ForeignKey(AlgaeSpecies, on_delete=models.CASCADE, related_name='strains')  # Reference to AlgaeSpecies
    strain = models.CharField(max_length=20, blank=True, null=True)  # Strain identifier (e.g., FACB905, CC638)

    def __str__(self):
        return f"{self.species.name} {self.strain if self.strain else ''}"
        # return self.species.name + " " + str(self.strain)

    def get_absolute_url(self):
        return reverse("algae-detail", kwargs={"pk": self.pk})


class Algae(models.Model):

    def __str__(self):
        return self.name + " " + str(self.strain)

    def get_absolute_url(self):
        return reverse("algae-detail", kwargs={"pk": self.pk})
    
    name = models.CharField(max_length=255)

    #分类
    phylum = models.CharField(max_length=100, blank=True, null=True) #门
    class_name = models.CharField(max_length=100, blank=True, null=True) #纲
    order = models.CharField(max_length=100, blank=True, null=True) #目
    family = models.CharField(max_length=100, blank=True, null=True) #科
    strain = models.CharField(max_length=100, blank=True, null=True) 

    # 环境描述
    environment = models.TextField(blank=True, null=True)

    #毒害特性
    TOXICITY_CHOICES = [
        ('Toxic', 'Toxic'),
        ('Harmful', 'Harmful'),
        ('Both', 'Toxic/Harmful'), 
    ]
    # toxicity_type = models.CharField(max_length=10, choices=TOXICITY_CHOICES, blank=True, null=True)
    toxicity_type = models.CharField(max_length=50, blank=True, null=True)
    # image = models.URLField(max_length=200, blank=True, null=True)  # 图片的URL
    description = models.TextField(blank=True, null=True)  # 说明文字
    image = models.ImageField(upload_to='algae_images/', null=True, blank=True)  # 图片字段
    note = models.TextField(null=True, blank=True)


    
#创建Chemical模型
class Chemical(models.Model):
    name = models.CharField(max_length=200, unique=True)
    classification = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(null=True, blank=True, max_length=200)
    np_classification = models.CharField(null=True, blank=True, max_length=200)
    casNumber = models.CharField(verbose_name="CAS", max_length=200, blank=True, null=True)
    pubchem_name = models.CharField(max_length=200, blank=True, null=True)
    pubchem_cid = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to='chemical_images/', null=True, blank=True)
    isnp = models.BooleanField()
    smiles = models.TextField(blank=True, null=True)
    InChI = models.TextField(blank=True, null=True)
    origin_choices = [
        ('Plant', 'Plant'),
        ('Microorganism', 'Microorganism'),
        ('Chemical', 'Chemical'),
    ]
    origin = models.CharField(max_length=20, choices=origin_choices, blank=True, null=True)
    pubchem = models.URLField(max_length=200, blank=True, null=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


#创建一个Reference模型，记录文献信息
class Reference(models.Model):
    publication_year = models.IntegerField()

    is_checked = models.BooleanField(default=False)

    author = models.TextField()
    title = models.TextField()
    publication_title = models.CharField(max_length=255, null=True, blank=True)
    doi = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Measurement(models.Model):
    # record = models.ForeignKey(Record, related_name='measurements', on_delete=models.CASCADE)
    time = models.CharField(max_length=255)  # 可以使用CharField来存储时间描述，如'24小时'
    measurement_type = models.CharField(max_length=255)  # 如'EC50' 或 '抑制率'
    effect = models.DecimalField(max_digits=10, decimal_places=4)  # 效果值，如0.05 mg/L
    unit = models.CharField(max_length=50)  # mg/L, mol/L 等

    def __str__(self):
        return f"{self.time} - {self.measurement_type} - {self.effect} {self.unit}"


#创建Record模型，记录每一条抑藻剂的信息，关联藻对对应的抑藻剂化合物和参考文献
class Record(models.Model):
    algae = models.ForeignKey(Algae, on_delete=models.CASCADE, null=True, blank=True)
    algae_strain = models.ForeignKey(AlgaeStrain, on_delete=models.CASCADE, null=True, blank=True)
    chemical = models.ForeignKey(Chemical, on_delete=models.CASCADE)

    measurement = models.CharField(max_length=50, blank=True, null=True) #选择是EC50还是IC50还是Inhibition rate
    effect = models.CharField(max_length=50, blank=True, null=True) #效果值
    unit = models.CharField(max_length=10, blank=True, null=True)   #单位 （mg/L, %）

    initialDensity = models.CharField(max_length=200, blank=True, null=True)
    time = models.CharField(max_length=20, blank=True, null=True)

    response_endpoint = models.CharField(max_length=200, blank=True, null=True) #响应端点

    other_measurements = models.TextField(null=True, blank=True) #其他测量值
    
    cultivationSystem = models.CharField(max_length=200, blank=True, null=True) #培养体系
    Irradiance = models.CharField(max_length=200, blank=True, null=True) #光照强度
    temperature = models.CharField(max_length=200, blank=True, null=True) #温度
    cultureMedium = models.CharField(max_length=200, blank=True, null=True) #培养基

    mechanism = models.TextField(null=True, blank=True)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)

    # measurements = models.ManyToManyField(Measurement, related_name='records', blank=True, null=True)


    def __str__(self) -> str:
        return str(self.chemical) + "_" + str(self.algae_strain)






# class Chemical(models.Model):
#     name = models.CharField(max_length=200, unique=True)
#     classification = models.CharField(max_length=200)
#     source = models.CharField(null=True, blank=True, max_length=200)
#     np_classification = models.CharField(null=True, blank=True, max_length=200)
#     casNumber = models.CharField(verbose_name="CAS", max_length=200)
#     isnp = models.BooleanField(verbose_name = "是否为天然产物")
#     smiles = models.CharField(max_length=200)

#     def __str__(self) -> str:
#         return self.name


# class Reference(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.CharField(max_length=200)
#     publishing_time = models.DateField()
#     doi = models.CharField(max_length=200, unique=True)

#     def __str__(self) -> str:
#         return self.name


# class Algae(models.Model):
#     parentCategory = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
#     key = models.CharField(max_length=200, unique=True)
#     description = models.CharField(max_length=500, null=True)
#     image = models.ImageField(upload_to="uploads/", verbose_name="图片", null=True, blank=True)
#     def data(self):
#         return {'name': self.key, 'description': self.description}

#     def __str__(self) -> str:
#         return self.key



# class Algaecide(models.Model):
#     algae = models.ForeignKey(to="Algae", to_field="key", verbose_name="藻", on_delete=models.CASCADE)
#     chemical = models.ForeignKey(to="Chemical", to_field="name", on_delete=models.CASCADE) #关联到外键
#     #casNumber = models.CharField(verbose_name="CAS")
#     initialDensity = models.CharField(max_length=200)
#     time = models.CharField(max_length=200)
#     ec50 = models.FloatField()
#     cultivationSystem = models.CharField(max_length=200)
#     Irradiance = models.CharField(max_length=200)
#     temperature = models.CharField(max_length=200)
#     cultureMedium = models.CharField(max_length=200)
#     mechenism = models.TextField(null=True, blank=True)

#     reference = models.ForeignKey(to="Reference", to_field="doi", on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.name

    


