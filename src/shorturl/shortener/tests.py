from django.test import TestCase
from django.test import Client
from shortener.views.url import * 
from shortener.views.user import * 
from shortener.views.common import *
from shortener.models import URLUser
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class LoginRequiredTest(TestCase):
    def setUp(self):
        # When a view needs login, it redirects to this URL, which has a "next" parameter.
        self.loginRequiredURL = '/accounts/login/?next'
        
    def test_help_requires_login(self):
        response = self.client.get(reverse("help"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_about_requires_login(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
                
    def test_index_requires_login(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
                
    def test_user_edit_requires_login(self):
        response = self.client.get(reverse("useredit"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
                
    def test_user_list_requires_login(self):
        response = self.client.get(reverse("userlist"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_url_add_ajax_requires_login(self):
        response = self.client.get(reverse("urladdajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_load_urls_ajax_requires_login(self):
        response = self.client.get(reverse("loadurlsajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_url_stats_ajax_requires_login(self):
        response = self.client.get(reverse("urlstatsajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_url_delete_ajax_requires_login(self):
        response = self.client.get(reverse("urldeleteajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_user_add_ajax_requires_login(self):
        response = self.client.get(reverse("useraddajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_load_users_ajax_requires_login(self):
        response = self.client.get(reverse("loadusersajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_user_toggle_ajax_requires_login(self):
        response = self.client.get(reverse("usertoggleajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_user_delete_ajax_requires_login(self):
        response = self.client.get(reverse("userdeleteajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_user_change_pw_ajax_requires_login(self):
        response = self.client.get(reverse("userchangepwajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)

class UrlTest(TestCase):

    def setUp(self):
        self.password = 'mypassword' 
        self.my_admin = URLUser.objects.create_superuser('admin', 'admin@example.com', self.password)
        self.my_staff = URLUser.objects.create_user('staff', 'staff@example.com', self.password)
        self.other_user = URLUser.objects.create_user('staff2', 'staff2@example.com', self.password)
        self.loginRequiredURL = '/accounts/login/?next'
        pass

    def test_add_url(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        url = {'original': 'https://matias.banchoff.ar'}
        urlCount = len(ShortenedURL.objects.all())
        response = c.post(reverse("urladdajax"), url, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('URL created' in str(response.content))
        self.assertTrue(len(ShortenedURL.objects.all()) == urlCount + 1)

    def test_add_url_without_ajax(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        url = {'original': 'https://matias.banchoff.ar'}
        urlCount = len(ShortenedURL.objects.all())
        response = c.post(reverse("urladdajax"), url)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Request should be Ajax POST' in str(response.content))
        self.assertTrue(len(ShortenedURL.objects.all()) == urlCount)

    def test_add_url_too_long(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        url = {'original': 'http://matias.banchoff.ar/'+'a'*250}
        urlCount = len(ShortenedURL.objects.all())
        response = c.post(reverse("urladdajax"), url, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Ensure this value has at most 200 characters' in str(response.content))
        self.assertTrue(len(ShortenedURL.objects.all()) == urlCount)

    def test_add_malformed_url(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        url = {'original': 'http:\/matias.banchoff.ar/'}
        urlCount = len(ShortenedURL.objects.all())
        response = c.post(reverse("urladdajax"), url, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Enter a valid URL' in str(response.content))
        self.assertTrue(len(ShortenedURL.objects.all()) == urlCount)

    def test_delete_url(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        url = ShortenedURL.create("https://matias.banchoff.ar", self.my_admin)
        url.save()
        urlCount = len(ShortenedURL.objects.all())
        response = c.post(reverse("urldeleteajax"), {'id': url.id }, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('URL deleted' in str(response.content))
        self.assertTrue(len(ShortenedURL.objects.all()) == urlCount - 1)

    def test_delete_other_users_url(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        url = ShortenedURL.create("https://matias.banchoff.ar", self.other_user)
        url.save()
        urlCount = len(ShortenedURL.objects.all())
        response = c.post(reverse("urldeleteajax"), {'id': url.id }, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue('User does not own this URL' in str(response.content))
        self.assertTrue(len(ShortenedURL.objects.all()) == urlCount)
        c = Client()
        response = c.get(reverse("urldeleteajax"))

    def test_delete_nonexistent_url(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        urlCount = len(ShortenedURL.objects.all())
        response = c.post(reverse("urldeleteajax"), {'id': -1 }, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 404)
        self.assertTrue(len(ShortenedURL.objects.all()) == urlCount)

    def test_get_stats_for_a_url(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        url = ShortenedURL.create("https://matias.banchoff.ar", self.my_staff)
        url.save()
        response = c.post(reverse("urlstatsajax"), {'id': url.id }, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('timesVisited' in str(response.content))

    def test_get_stats_for_a_url_without_ajax(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        url = ShortenedURL.create("https://matias.banchoff.ar", self.my_staff)
        url.save()
        response = c.post(reverse("urlstatsajax"), {'id': url.id })
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Request should be Ajax POST' in str(response.content))

        
    def test_get_stats_for_nonexistent_url(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        response = c.post(reverse("urlstatsajax"), {'id': -1 }, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 404)

    def test_get_stats_for_other_users_url(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        url = ShortenedURL.create("https://matias.banchoff.ar", self.other_user)
        url.save()
        response = c.post(reverse("urlstatsajax"), {'id': url.id }, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue('User does not own this URL' in str(response.content))
    
    def test_url_redirect(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        url = ShortenedURL.create("https://matias.banchoff.ar", self.my_staff)
        url.save()
        response = c.get(reverse("redirectto", args=[url.shortened]))
        self.assertEqual(response.status_code, 302)

    def test_url_redirect_for_other_users_url(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        url = ShortenedURL.create("https://matias.banchoff.ar", self.other_user)
        url.save()
        response = c.get(reverse("redirectto", args=[url.shortened]))
        self.assertEqual(response.status_code, 400)
        self.assertTrue('User does not own this URL' in str(response.content))
    
    def test_url_redirect_for_nonexistent_url(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        response = c.get(reverse("redirectto", args=["a"*32]))
        self.assertEqual(response.status_code, 404)

    def test_url_redirect_for_malformed_url(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        try:
            response = c.get(reverse("redirectto", args=["abcd"]))
            self.fail("NoReverseMatch was not raised")
        except NoReverseMatch:
            pass
        
    def test_url_creates_access(self):
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        url = ShortenedURL.create("https://matias.banchoff.ar", self.my_staff)
        url.save()
        accessCount = len(Access.objects.all())
        response = c.get(reverse("redirectto", args=[url.shortened]))
        self.assertTrue(len(Access.objects.all()) == accessCount + 1)

        
class UserTest(TestCase):

    def setUp(self):
        self.password = 'mypassword' 
        self.my_admin = URLUser.objects.create_superuser('admin', 'admin@example.com', self.password)
        self.my_staff = URLUser.objects.create_user('staff', 'staff@example.com', self.password)
        self.loginRequiredURL = '/accounts/login/?next'
        
    def test_user_list_requires_admin(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        response = c.get(reverse("userlist"))
        self.assertEqual(response.status_code, 200)
        
        c.logout()
        c.login(username=self.my_staff.username, password=self.password)
        response = c.get(reverse("userlist"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        
    def test_admin_can_change_passwords(self):
        # Tests that the admin can change the password to staff
        staff_user = {
            'id': self.my_staff.id,
            'password1': 'fgthyju574635weavd',
            'password2': 'fgthyju574635weavd',
        }
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        response = c.post(reverse("userchangepwajax"), staff_user, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Password changed' in str(response.content))

    def test_user_can_change_own_password(self):
        # Tests that the staff can change her own password 
        staff_user = {
            'id': self.my_staff.id,
            'password1': 'fgthyju574635weavd',
            'password2': 'fgthyju574635weavd',
        }
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        response = c.post(reverse("userchangepwajax"), staff_user, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Password changed' in str(response.content))

    def test_user_cannot_change_other_user_password(self):
        other_user = URLUser.objects.create_user('other', 'other@example.com', 'dsfgthy63524e')
        change_data = {
            'id': other_user.id,
            'password1': 'fgthyju574635weavd',
            'password2': 'fgthyju574635weavd',
        }
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        response = c.post(reverse("userchangepwajax"), change_data, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue('User has no permission' in str(response.content))

        
class UserAjaxTest(TestCase):
    # This is for views that expect requests made using Ajax.
    def setUp(self):
        self.password = 'mypassword' 
        self.my_admin = URLUser.objects.create_superuser('admin', 'admin@example.com', self.password)
        self.my_staff = URLUser.objects.create_user('staff', 'staff@example.com', self.password)
        self.loginRequiredURL = '/accounts/login/?next'

    def test_user_delete_non_ajax_post(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        idToDelete = self.my_staff.id
        response = c.post(reverse("userdeleteajax"), {'id': idToDelete})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Request should be Ajax POST" in str(response.content))

    def test_user_delete_ajax_non_existent_user(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        idToDelete = self.my_staff.id + self.my_admin.id
        response = c.post(reverse("userdeleteajax"), {'id': idToDelete}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 404)

    def test_user_delete_own_user(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        idToDelete = self.my_admin.id
        response = c.post(reverse("userdeleteajax"), {'id': idToDelete}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("User cannot delete herself" in str(response.content))

    def test_user_delete(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        userCount = len(URLUser.objects.all())
        idToDelete = self.my_staff.id
        response = c.post(reverse("userdeleteajax"), {'id': idToDelete}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("User deleted" in str(response.content))
        self.assertTrue(len(URLUser.objects.all()) == userCount-1)
    
    def test_staff_user_cannot_change_other_users(self): 
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        other_staff = URLUser.objects.create_user('staff2', 'staff2@example.com', 'sadasddsf123123sad')
        idToToggle = other_staff.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(reverse('index'), response.url)
        self.assertEqual(response.status_code, 302)
        other_staff.delete()

    def test_user_change_with_non_ajax_post(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        idToToggle = self.my_staff.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Request should be Ajax POST" in str(response.content))
    
    def test_changing_non_existent_user(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        idToToggle = self.my_staff.id + self.my_admin.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 404)

    def test_changing_own_user(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        idToToggle = self.my_admin.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Cannot change your own user" in str(response.content))

    def test_change_another_user(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        idToToggle = self.my_staff.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("ADMIN" in str(response.content))
        
    def test_add_user_with_non_ajax_post(self):
        user_well_formed = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password1': 'asd!#as213',
            'password2': 'asd!#as213',}
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        response = c.post(reverse("useraddajax"), user_well_formed)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Request should be Ajax POST" in str(response.content))

    def test_add_user_with_wrong_username(self):
        user_with_repeated_username = {
            'username': self.my_staff.username,
            'email': self.my_staff.email,
            'password1': 'mypassword',
            'password2': 'mypassword',}
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        response = c.post(reverse("useraddajax"), user_with_repeated_username, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in str(response.content))

    def test_add_user_with_missmatching_passwords(self):
        user_with_missmatching_passwords = {
            'username': 'testuser1',
            'email': 'testuser1@example.com',
            'password1': 'mypassword',
            'password2': 'otherpassword',}
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        response = c.post(reverse("useraddajax"), user_with_missmatching_passwords, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in str(response.content))

    def test_add_user_with_wrong_email(self):
        user_with_wrong_email = {
            'username': 'testuser2',
            'email': 'testuser2',
            'password1': 'mypassword',
            'password2': 'mypassword',}
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        response = c.post(reverse("useraddajax"), user_with_wrong_email, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in str(response.content))

    def test_add_user(self):
        user_well_formed = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password1': 'asd!#as213',
            'password2': 'asd!#as213',}
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        userCount = len(URLUser.objects.all())
        response = c.post(reverse("useraddajax"), user_well_formed, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("User created" in str(response.content))
        self.assertTrue(len(URLUser.objects.all()) == userCount + 1)

    def test_add_user_with_username_too_long(self):
        # Username's length defaults to a max. of 150 chars
        user = {
            'username': 'a'*151,
            'email': 'testuser3@example.com',
            'password1': 'asd!#as213',
            'password2': 'asd!#as213',}
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        userCount = len(URLUser.objects.all())
        response = c.post(reverse("useraddajax"), user, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Ensure this value has at most 150 characters (it has 151)" in str(response.content))
        self.assertTrue(len(URLUser.objects.all()) == userCount)

    def test_add_user_without_valid_email(self):
        user = {
            'username': 'test1',
            'email': 'testuser3@without@email',
            'password1': 'asd!#as213',
            'password2': 'asd!#as213',}
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        userCount = len(URLUser.objects.all())
        response = c.post(reverse("useraddajax"), user, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Enter a valid email address" in str(response.content))
        self.assertTrue(len(URLUser.objects.all()) == userCount)


    def test_non_admin_user_cannot_add_user(self):
        user_well_formed = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password1': 'asd!#as213',
            'password2': 'asd!#as213',}
        
        c = Client()
        c.login(username=self.my_staff.username, password=self.password)
        response = c.post(reverse("useraddajax"), user_well_formed, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('index'), response.url)
        
