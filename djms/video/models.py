from django.db import models
from django.urls import reverse
from hashlib import md5
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# Validator of file about size and extension
def video_size(value):
    limit = 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MiB.')
video_extension = FileExtensionValidator(['avf'])

class Video(models.Model):
    # about the file
    file = models.FileField(upload_to=r'videos/%Y%m%d', validators=[video_size, video_extension])
    file_md5 = models.CharField(max_length=16, editable=False, unique=True)
    
    # about the site
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    STATES = [('p', '审核中'), ('a', '已通过'), ('r', '被拒绝'), ('i', '可收录')] # included for some unofficial version
    state = models.CharField(max_length=3, choices=STATES, default='p')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    
    # about the video(?)
    software = models.CharField(max_length=16) # todo: make choices for this field
    identification = models.CharField(max_length=16, verbose_name="标识")
    start_time = models.DateTimeField(verbose_name="游戏时间")
    
    # about the game
    MODES = [('beg', '初级'), ('int', '中级'),  ('exp', '高级')]
    mode = models.CharField(max_length=3, choices=MODES)
    nf = models.BooleanField(default=False)
    time = models.DecimalField(max_digits=7, decimal_places=3)
    bv = models.PositiveSmallIntegerField()
    cl = models.PositiveSmallIntegerField()
    ce = models.PositiveSmallIntegerField()
    flags = models.PositiveSmallIntegerField()
    bvs = models.FloatField()
    qg = models.FloatField()
    stnb = models.FloatField()
    ioe = models.FloatField()
    thrp = models.FloatField()
    cls = models.FloatField()
    ces = models.FloatField()
    
    def __str__(self):
        return '{}{}/{}[{}]'.format(self.mode, self.time, self.bv, self.player.pid)
    
    def get_absolute_url(self):
        return reverse("video:video_detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        # calculate md5 before saving the video
        temp = md5()
        for chunk in self.file.chunks():
            temp.update(chunk)
        self.file_md5 = temp.hexdigest()
        super().save(*args, **kwargs)
    
    