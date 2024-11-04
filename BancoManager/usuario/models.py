
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from dashboard.opciones_models.opciones_models import guardar_images
# ○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○#
#         Lenguajes
Lenguajes = (
    ('America', (
        ('brazilian_portuguese', 'Portugués brasileño'),
        ('canadian_french', 'Francés canadiense'),
        ('english', 'Inglés'),
        ('french_creole', 'Criollo francés'),
        ('haitian_creole', 'Criollo haitiano'),
        ('navajo', 'Navajo'),
        ('quechua', 'Quechua'),
        ('spanish', 'Español'),
    )),
    ('Western Europe', (
        ('catalan', 'Catalán'),
        ('danish', 'Danés'),
        ('dutch', 'Holandés'),
        ('faroese', 'Feroés'),
        ('finnish', 'Finlandés'),
        ('flemish', 'Flamenco'),
        ('french', 'Francés'),
        ('german', 'Alemán'),
        ('greek', 'Griego'),
        ('icelandic', 'Islandés'),
        ('italian', 'Italiano'),
        ('norwegian', 'Noruego'),
        ('portuguese', 'Portugués'),
        ('spanish', 'Español'),
        ('swedish', 'Sueco'),
        ('uk_english', 'Inglés británico / Inglés británico'),
    )),
    ('Central & Eastern Europe', (
        ('belarusian', 'Bielorruso'),
        ('bosnian', 'Bosnio'),
        ('bulgarian', 'Búlgaro'),
        ('croatian', 'Croata'),
        ('czech', 'Checo'),
        ('estonian', 'Estonio'),
        ('hungarian', 'Húngaro'),
        ('latvian', 'Letón'),
        ('lithuanian', 'Lituano'),
        ('macedonian', 'Macedonio'),
        ('polish', 'Polaco'),
        ('romanian', 'Rumano'),
        ('russian', 'Ruso'),
        ('serbian', 'Serbio'),
        ('slovak', 'Eslovaco'),
        ('slovenian', 'Esloveno'),
        ('turkish', 'Turco'),
        ('ukrainian', 'Ucraniano'),
    )),
    ('Africa', (
        ('amharic', 'Amárico (Etiopía)'),
        ('dinka', 'Dinka (Sudán)'),
        ('ibo', 'Ibo (Nigeria)'),
        ('kirundi', 'Kirundi'),
        ('mandinka', 'Mandinka'),
        ('nuer', 'Nuer (Nilo-Sahariano)'),
        ('oromo', 'Oromo (Etiopía)'),
        ('kinyarwanda', 'Kinyarwanda'),
        ('shona', 'Shona (Zimbabue)'),
        ('somali', 'Somalí'),
        ('swahili', 'Suajili'),
        ('tigrigna', 'Tigrigna (Etiopía)'),
        ('wolof', 'Wolof'),
        ('xhosa', 'Xhosa'),
        ('yoruba', 'Yoruba'),
        ('zulu', 'Zulú'),
    )),
    ('Middle East', (
        ('arabic', 'Árabe'),
        ('dari', 'Dari'),
        ('farsi', 'Persa'),
        ('hebrew', 'Hebreo'),
        ('kurdish', 'Kurdo'),
        ('pashtu', 'Pastún'),
        ('punjabi', 'Punyabí'),
        ('urdu_pakistan', 'Urdu (Pakistán)'),
    )),
    ('Central Asia', (
        ('armenian', 'Armenio'),
        ('azerbaijani', 'Azerbaiyano'),
        ('georgian', 'Georgiano'),
        ('kazakh', 'Kazajo'),
        ('mongolian', 'Mongol'),
        ('turkmen', 'Turcomano'),
        ('uzbek', 'Uzbeko'),
    )),
    ('Southeast Asia', (
        ('bengali', 'Bengalí'),
        ('cham', 'Cham'),
        ('chamorro_guam', 'Chamorro (Guam)'),
        ('gujarati_india', 'Guyaratí (India)'),
        ('hindi', 'Hindi'),
        ('indonesian', 'Indonesio'),
        ('khmer_cambodia', 'Jemer (Camboya)'),
        ('kmhmu_laos', 'Kmhmu (Laos)*'),
        ('korean', 'Coreano'),
        ('laotian', 'Laosiano'),
        ('malayalam', 'Malayalam'),
        ('malay', 'Malayo'),
        ('marathi_india', 'Marathi (India)'),
        ('marshallese', 'Marshalés'),
        ('nepali', 'Nepalí'),
        ('sherpa', 'Sherpa*'),
        ('tamil', 'Tamil'),
        ('thai', 'Tailandés'),
        ('tibetan', 'Tibetano'),
        ('trukese_micronesia', 'Trukés (Micronesia)'),
        ('vietnamese', 'Vietnamita'),
    )),
    ('Far East', (
        ('amoy', 'Amoy'),
        ('burmese', 'Birmano'),
        ('cantonese', 'Cantonés'),
        ('chinese', 'Chino'),
        ('chinese_simplified', 'Chino Simplificado'),
        ('chinese_traditional', 'Chino Tradicional'),
        ('chiu_chow', 'Chiu Chow'),
        ('chow_jo', 'Chow Jo'),
        ('fukienese', 'Fukienese'),
        ('hakka_china', 'Hakka (China)'),
        ('hmong', 'Hmong'),
        ('hainanese', 'Hainanés'),
        ('japanese', 'Japonés'),
        ('mandarin', 'Mandarín'),
        ('mien', 'Mien'),
        ('shanghainese', 'Shanghainés*'),
        ('taiwanese', 'Taiwanés'),
        ('taishanese', 'Taishanés'),
    )),
    ('South Pacific', (
        ('fijian', 'Fiyiano'),
        ('palauan', 'Palauano*'),
        ('samoan', 'Samoano'),
        ('tongan', 'Tongano'),
    )),
    ('Philippines', (
        ('bikol', 'Bicol'),
        ('cebuano', 'Cebuano'),
        ('ilocano', 'Ilocano'),
        ('ilongo', 'Ilonggo'),
        ('pampangan', 'Pampango'),
        ('pangasinan', 'Pangasinán'),
        ('tagalog', 'Tagalo'),
        ('visayan', 'Visayan'),
    )),
    ('Idiomas y Servicios Adicionales', (
        ('american_sign_language', 'Lenguaje de Señas Estadounidense'),
        ('braille', 'Braille'),
        ('esperanto', 'Esperanto'),
        ('latin', 'Latín'),
        ('phonetic', 'Fonético'),
        ('real_time_captioning', 'Subtitulación en tiempo real y remota'),
        ('tactile', 'Táctil'),
        ('limited_resources', 'Recursos Limitados Disponibles'),
    )),
)
#♥♠♣♦♥♠♣♦♥♠♣♦♥♠♣♦♥♠♣♦♥♠♣♦♥♠♣♦#
# MODELO USUARIO PERZONALIZADO  
#♥♠♣♦♥♠♣♦♥♠♣♦♥♠♣♦♥♠♣♦♥♠♣♦♥♠♣♦#

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El email debe ser obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True')
        return self._create_user(email, password, **extra_fields)
    
class usuario(AbstractBaseUser, PermissionsMixin):
    # Registro por defecto:
    email = models.EmailField(unique=True)
    # Datos perzonales:
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    # Datos de permisos:
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # Datos de registro:
    imagen_perfil = models.ImageField(upload_to=guardar_images, default="static/img/user/default.png", blank=True, null=True)
    # Configuracion de usuario:
    contenido_adulto = models.BooleanField(default=False)
    idioma = models.CharField(max_length=300, blank=True, choices=(Lenguajes), default="spanish")
    # Datos automaticos:
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    objects = CustomUserManager()
    ip_address = models.GenericIPAddressField(verbose_name='Dirección IP del usuario', blank=True, null=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    def __str__(self):
        return self.email
    def get_short_name(self):
        return self.email or self.email.split('@')[0]
    def get_full_name(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

