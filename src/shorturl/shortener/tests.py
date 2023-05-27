from django.test import TestCase
from django.test import Client
from shortener.views.url import * 
from shortener.views.user import * 
from shortener.views.common import *
from shortener.models import URLUser
from django.urls import reverse



class LoginRequiredTest(TestCase):
    def setUp(self):
        # When a view needs login, it redirects to this URL, which has a "next" parameter.
        self.loginRequiredURL = '/accounts/login/?next'
        
    def test_help(self):
        response = self.client.get(reverse("help"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_about(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
                
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
                
    def test_user_edit(self):
        response = self.client.get(reverse("useredit"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
                
    def test_user_list(self):
        response = self.client.get(reverse("userlist"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_url_add_ajax(self):
        response = self.client.get(reverse("urladdajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_load_urls_ajax(self):
        response = self.client.get(reverse("loadurlsajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_url_stats_ajax(self):
        response = self.client.get(reverse("urlstatsajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_url_delete_ajax(self):
        response = self.client.get(reverse("urldeleteajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_user_add_ajax(self):
        response = self.client.get(reverse("useraddajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_load_users_ajax(self):
        response = self.client.get(reverse("loadusersajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_user_toggle_ajax(self):
        response = self.client.get(reverse("usertoggleajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_user_delete_ajax(self):
        response = self.client.get(reverse("userdeleteajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)
        
    def test_user_change_pw_ajax(self):
        response = self.client.get(reverse("userchangepwajax"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)

class AdminRequiredTest(TestCase):
    # Tests that an admin can execute the views but a staff user cannot.

    def setUp(self):
        self.password = 'mypassword' 
        self.my_admin = URLUser.objects.create_superuser('admin', 'admin@example.com', self.password)
        self.my_staff = URLUser.objects.create_user('staff', 'staff@example.com', self.password)
        
    def test_user_list(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        response = c.get(reverse("userlist"))
        self.assertEqual(response.status_code, 200)
        
        c.logout()
        c.login(username=self.my_staff.username, password=self.password)
        response = c.get(reverse("userlist"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

        
class AdminRequiredTestAjax(TestCase):
    # Tests that an admin can execute the views but a staff user cannot.
    # This is for views that expect requests made using Ajax.

    def setUp(self):
        self.password = 'mypassword' 
        self.my_admin = URLUser.objects.create_superuser('admin', 'admin@example.com', self.password)
        self.my_staff = URLUser.objects.create_user('staff', 'staff@example.com', self.password)
        self.loginRequiredURL = '/accounts/login/?next'
        
    def test_user_delete_ajax(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        
        # First tries using a non-ajax post.
        idToDelete = self.my_staff.id
        response = c.post(reverse("userdeleteajax"), {'id': idToDelete})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Request should be Ajax POST" in str(response.content))

        # Then tries using an ajax post. But with a non-existent user.
        idToDelete = self.my_staff.id + self.my_admin.id
        response = c.post(reverse("userdeleteajax"), {'id': idToDelete}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 404)
        
        # Now we try to delete our own user
        idToDelete = self.my_admin.id
        response = c.post(reverse("userdeleteajax"), {'id': idToDelete}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("User cannot delete herself" in str(response.content))
        
        # Finally, we try deleting another user.
        idToDelete = self.my_staff.id
        response = c.post(reverse("userdeleteajax"), {'id': idToDelete}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("User deleted" in str(response.content))

        c.logout()
        c.login(username=self.my_staff.username, password=self.password)
        response = c.post(reverse("userdeleteajax"), {'id': idToDelete}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.loginRequiredURL in response.url)


        
    def test_user_toggle_ajax(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        
        # First tries using a non-ajax post.
        idToToggle = self.my_staff.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Request should be Ajax POST" in str(response.content))

        # Then tries using an ajax post. But with a non-existent user.
        idToToggle = self.my_staff.id + self.my_admin.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 404)
        
        # Now we try to toggle our own user
        idToToggle = self.my_admin.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Cannot change your own user" in str(response.content))
        
        # Finally, we try to change another user.
        idToToggle = self.my_staff.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle}, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("ADMIN" in str(response.content))

        c.logout()
        c.login(username=self.my_staff.username, password=self.password)
        other_staff = URLUser.objects.create_user('staff2', 'staff2@example.com', 'sadasddsf123123sad')
        idToToggle = other_staff.id
        response = c.post(reverse("usertoggleajax"), {'id': idToToggle}, headers={"X-Requested-With": "XMLHttpRequest"})
        #self.assertEqual(reverse('index'), response.url)
        self.assertEqual("", response.userState)
        self.assertEqual(response.status_code, 302)

        
    def test_user_add_ajax(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        
        # First tries using a non-ajax post.
        user_with_repeated_username = {
            'username': self.my_staff.username,
            'email': self.my_staff.email,
            'password1': 'mypassword',
            'password2': 'mypassword',}
        user_with_missmatching_passwords = {
            'username': 'testuser1',
            'email': 'testuser1@example.com',
            'password1': 'mypassword',
            'password2': 'otherpassword',}
        user_with_wrong_email = {
            'username': 'testuser2',
            'email': 'testuser2',
            'password1': 'mypassword',
            'password2': 'mypassword',}
        user_well_formed = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password1': 'asd!#as213',
            'password2': 'asd!#as213',}

        # We try to add a user not using ajax        
        response = c.post(reverse("useraddajax"), user_well_formed)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Request should be Ajax POST" in str(response.content))
        
        # We try to add a user with a username that already exists
        response = c.post(reverse("useraddajax"), user_with_repeated_username, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in str(response.content))
        
        # We try to add a user with passwords that don't match
        response = c.post(reverse("useraddajax"), user_with_missmatching_passwords, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in str(response.content))

        # We try to add a user with a wrong email
        response = c.post(reverse("useraddajax"), user_with_wrong_email, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in str(response.content))

        # We add a user correctly
        response = c.post(reverse("useraddajax"), user_well_formed, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("User created" in str(response.content))

        c.logout()
        c.login(username=self.my_staff.username, password=self.password)
        response = c.post(reverse("useraddajax"), user_well_formed, headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('index'), response.url)



        

class CanChangeHerself(TestCase):
    # Tests method where a user can change her own data, but not other's data.
    pass
    # def userChangePWAjax(request):
    #     def userEdit(request):

    
# def userLoadAjax(request):    
# def userDeleteAjax(request):
# def userList(request):
# def userToggleAjax(request):
# def userAddAjax(request):

    # path("", url.index, name="index"),
    # path("url/add/ajax", url.urlAddAjax, name="urladdajax"),
    # path("url/load/ajax", url.urlLoadAjax, name="loadurlsajax"),
    # path("url/stats/ajax", url.urlStatsAjax, name="urlstatsajax"),
    # path("url/delete/ajax", url.urlDeleteAjax, name="urldeleteajax"),

    # path("user/edit", user.userEdit, name="useredit"),
    # path("user/add/ajax", user.userAddAjax, name="useraddajax"),
    # path("user/load/ajax", user.userLoadAjax, name="loadusersajax"),
    # path("user/list", user.userList, name="userlist"),
    # path("user/toggle/ajax", user.userToggleAjax, name="usertoggleajax"),
    # path("user/delete/ajax", user.userDeleteAjax, name="userdeleteajax"),
    # path("user/changepw/ajax", user.userChangePWAjax, name="userchangepwajax"),



        
