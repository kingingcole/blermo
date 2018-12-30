from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from datetime import date
import dateutil

from django.core.files.storage import default_storage as storage



# Create your models here.
class Profile(models.Model):
    # creating a one to oe rel with a user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')
    dob = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=400, blank=True)
    following = models.ManyToManyField('self', related_name='follows', symmetrical=False, blank=True, null=True)
    #follow = models.ManyToManyField('self', related_name='followed', symmetrical=False)
    joined_at = models.DateField(auto_now_add=True)

    COLLEGE_CHOICES = (
        ('ABSU', 'Abia State University, Uturu, Abia State'),
        ('EBSU', 'Ebonyi State University, Abakaliki'),
        ('UNILAG', 'University of Lagos, Idi Araba, Lagos State'),
        ('OAU', 'Obafemi Awolowo University, Ile Ife, Osun State'),
        ('UNIPORT', 'University of Port-Harcourt, Rivers State'),
        ('UDUSOK', 'Usman Dan Fodiyo University, Sokoto, Sokoto State'),
        ('UI', 'University of Ibadan, Oyo State'),
        ('UNILORIN', 'University of Ilorin, Kwara State'),
        ('UNICAL', 'University of Calabar, Cross River State'),
        ('LASU', 'Lagos State University, Ikeja, Lagos State'),
        ('AAU', 'Ambrose Alli University, Ekpoma, Edo State'),
        ('UNIJOS', 'University of Jos, Plateau State'),
        ('BUK', 'Bayero University, Kano, Kano State'),
        ('OOU', ' Olabisi Onabanjo (formerly Ogun State) University, Ago Iwoye, Ogun State'),
        ('IMSU', 'Imo State University, Owerri, Imo State'),
        ('MADONNA', 'Madonna University Okija'),
        ('UNIBEN', 'University of Benin, Benin-City, Edo State'),
        ('OBA OKUNADE', 'Oba Okunade College of Health Sciences Igbinedion University Okada, Benin -City, Edo State'),
        ('UNN', 'University of Nigeria, Ozara-Ituku. Enugu State'),
        ('UNIZIK', 'Nnamdi Azikiwe University, Nnewi, Anambra State'),
        ('ABU', 'Ahmadu Bello University Zaria, Kaduna State'),
        ('UNIMAID', 'University of Maiduguri, Borno State'),
        ('DELSU', 'Delta State University, Abraka, Delta State'),
        ('ESUT', 'Enugu State University of Science and Technology, Enugu, Enugu State'),
        ('UNIUYO', 'University of Uyo, Uyo, Cross River State'),
        ('BINGHAM UNI', 'Bingham University Karu, Nasarawa.State'),
        ('NIGER-DELTA UNI', 'Niger Delta University, Wilberforce Island, Bayelsa State'),
        ('BENSU', 'Benue State University, Makurdi, Benue State'),
        ('BABCOCK', 'Babcock University Ilishan-Remo, Ogun State'),
        ('UNIABJ', 'University of Abuja'),
        ('AFE-BABALOLA', 'Afe Babalola University Ado-Ekiti, Ekiti State'),
    )

    YEAR_IN_COLLEGE_CHOICES = (
        ('100', '100 Level'),
        ('200', '200 Level'),
        ('300', '300 Level'),
        ('400', '400 Level'),
        ('500', '500 Level'),
        ('600', '600 Level'),
    )

    year_in_college = models.CharField(max_length=3, choices=YEAR_IN_COLLEGE_CHOICES, default='')
    college = models.CharField(max_length=15, choices=COLLEGE_CHOICES, default='')



    # def get_no_of_followers(self):
    #    all_users = User.objects.all()
    #    for user in all_users:
    #        if self in user.profile.follows.all():
    #            self.followers.add(user.profile)
    #    return self.followers.count()
       

    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name



    def calculate_age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        else:
            return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # img = Image.open(self.avatar.path
        img = Image.open(storage.open(self.avatar.name))
        output_size = (200, 200)
        img.thumbnail(output_size)
        # img.save(self.avatar.url)
        fh = storage.open(self.avatar.name, "w")
        format = 'png'  # You need to set the correct image format here
        img.save(fh, format)
        fh.close()

    def __str__(self):
        return f'Profile of ' + self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
