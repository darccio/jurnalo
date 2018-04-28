from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import timezone
import hashlib
import codecs


@python_2_unicode_compatible
class Entity(models.Model):
    urn = models.CharField(max_length=128)

    def __str__(self):
        return self.urn


class EntityMeta(models.Model):
    entity = models.ForeignKey(Entity, related_name='meta')
    key = models.CharField(max_length=128)
    value = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)


def _encode_integer(value, bytes=4):
    return codecs.encode(value.to_bytes(bytes, byteorder='little'), 'hex').decode('utf-8')


def _encode_datetime(value):
    ts = value.replace(tzinfo=timezone.utc).timestamp() * 1000000
    return _encode_integer(int(ts), bytes=8)


__record_version__=1

@python_2_unicode_compatible
class Record(models.Model):
    version = models.PositiveSmallIntegerField(default=__record_version__)
    text = models.CharField(max_length=500)
    creator = models.ForeignKey(Entity, related_name='records')
    on_behalf_of = models.ForeignKey(Entity, null=True, related_name='+')
    previous_record = models.ForeignKey('Record', null=True, related_name='next_record')
    created_at = models.DateTimeField()
    passed_at = models.DateTimeField()
    hash = models.CharField(max_length=64)
    uid = models.CharField(max_length=8)
    info_url = models.URLField(null=True)
    related_to = models.ManyToManyField('Record', related_name='related_records')
    protected = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.hash = self.__hashhex__().decode('utf-8')
        self.uid = self.hash[:8]
        super(Record, self).save(*args, **kwargs)

    def __str__(self):
        return self.text

    def __hash__(self):
        return int(self.__hashhex__(), base=16)

    def __hashhex__(self):
        version = _encode_integer(self.version)
        if self.previous_record:
            previous_record_hash = self.previous_record.hash
        else:
            # Genesis record
            previous_record_hash = '0' * 64
        inner_hash = hashlib.sha256(self.text.encode('utf-8') + self.creator.urn.encode('utf-8') + self.on_behalf_of.urn.encode('utf-8') + self.info_url.encode('utf-8')).hexdigest()
        created_at = _encode_datetime(self.created_at)
        passed_at = _encode_datetime(self.passed_at)
        record_hex = version + previous_record_hash + inner_hash + created_at + passed_at
        record = codecs.decode(record_hex, 'hex')
        hash = hashlib.sha256(hashlib.sha256(record).digest()).digest()
        return codecs.encode(hash[::-1], 'hex')


class RecordMeta(models.Model):
    record = models.ForeignKey(Record, related_name='meta')
    key = models.CharField(max_length=128)
    value = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)

