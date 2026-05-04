from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from nigger.models import Nigger

# Create your tests here.

class GetPagesTestCase(TestCase):
    fixtures =['auth_group.json' , 'nigger_nigger.json', 'nigger_category.json', 'nigger_gun.json', 'nigger_tagspost.json', 'users_user.json'  ]
    
    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('nigger/index.html', response.template_name)
        self.assertTemplateUsed(response, 'nigger/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        w = Nigger.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], w[:3])
        
    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 3
        response = self.client.get(path + f'?page={page}')
        w = Nigger.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], w[(page-1)*paginate_by:page*paginate_by])
    
    def test_content_post(self):
        w = Nigger.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)
    
    def tearDown(self):
        "Действия после выполнения каждого теста"
