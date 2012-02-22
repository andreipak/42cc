from django.test import TestCase
from testassignment.t1_contact.models import Contact
from models import AuditLogEntry

class AuditLoggerTest(TestCase):
    def setUp(self):
        self._contact = { #copied from fixture
            "bio": "Application Developer, System Administrator \r\nand Researcher in a wide variety of \r\napplications and tools",
            "name": "Andrei",
            "contacts": "Kharkov, Lugovaya st. 30A/2",
            "lastname": "Pak",
            "dateofbirth": "1981-03-13",
            "othercontacts": "http://google.com/profiles/pak.andrei - Google Profile\r\nhttp://pakan.ru - Personal Page",
            "skype": "pak.andrei",
            "jabber": "pak.andrei@gmail.com",
            "email": "pak.andrei@gmail.com",
            #"photo": None
        }


    def test_object_create(self):
        count_before = AuditLogEntry.objects.count()
        contact = Contact.objects.create(**self._contact)
        count_after = AuditLogEntry.objects.count()
        self.assertEqual(count_after - 1, count_before)

        ale = AuditLogEntry.objects.latest('date')
        self.assertNotEquals(ale, None)
        self.assertEquals(ale.model, contact._meta.object_name)
        self.assertEquals(ale.instance, unicode(contact))
        self.assertEquals(ale.action, AuditLogEntry.ACTION_CREATE)

    def test_object_update(self):

        count_before = AuditLogEntry.objects.count()

        contact = Contact.objects.get()
        contact.name = 'Andrey'
        contact.save()

        count_after = AuditLogEntry.objects.count()
        self.assertEqual(count_after - 1, count_before)

        ale = AuditLogEntry.objects.latest('date')
        self.assertNotEquals(ale, None)
        self.assertEquals(ale.model, contact._meta.object_name)
        self.assertEquals(ale.instance, unicode(contact))
        self.assertEquals(ale.action, AuditLogEntry.ACTION_UPDATE)

    def test_object_delete(self):

        count_before = AuditLogEntry.objects.count()

        contact = Contact.objects.get()
        contact.delete()

        count_after = AuditLogEntry.objects.count()
        self.assertEqual(count_after - 1, count_before)

        ale = AuditLogEntry.objects.latest('date')
        self.assertNotEquals(ale, None)
        self.assertEquals(ale.model, contact._meta.object_name)
        self.assertEquals(ale.instance, unicode(contact))
        self.assertEquals(ale.action, AuditLogEntry.ACTION_DELETE)