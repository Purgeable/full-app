# -*- coding: utf-8 -*-


from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from datapoint.models import Datapoint


class DatapointTests(APITestCase):
    fixtures = ['datapoint_testdata.json']

    def setUp(self):
        """
        Set up every test. Create admin user and log in it.  
        """
        self.user = User.objects.create(username='test', is_staff=True)
        self.client.force_authenticate(user=self.user)

        self.datapoint = Datapoint.objects.create(freq='m', name='BRENT', date='2017-09-20', value=50.25)

        self.url_list = reverse('datapoint-list')
        self.url_detail = reverse('datapoint-detail', args=(self.datapoint.pk,))

    def test_create(self):
        """Creates a new object in the database with the fields name, freq,
        date, and value, which is passed in as a json object in a post request.
        The single new entry should be successfully added and have the name
        'test'.
        """
        data = {
            'name': 'test',
            'freq': 'm',
            'date': '2018-01-01',
            'value': 42.0
        }
        response = self.client.post(self.url_list, data, format='json')
        obj = Datapoint.objects.order_by('id').last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(obj.name, 'test')

    def test_list(self):
        """A GET request should recover a list of all items in the database on
        the /datapoints/ endpoint in JSON format.
        """
        amount = len(Datapoint.objects.all())
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], amount)

    def test_retrieve(self):
        """When navigating to a specific datapoint url, the response header
        should match the corresponding id and name for that item in the database.
        """
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.datapoint.id)
        self.assertEqual(response.data['name'], self.datapoint.name)

    def test_update(self):
        """When editing the information in a form on a particular datapoint
        url, the existing fields in the database should match the data in the
        response header, and the updated data should also match.
        """
        data = {'value': 42.0}
        response = self.client.patch(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.datapoint.id)
        self.assertEqual(response.data['name'], self.datapoint.name)
        self.assertEqual(response.data['value'], 42.0)

    def test_delete(self):
        """After deleting the item belonging to a particular datapoint url, the
        item should be removed from the database.
        """
        response = self.client.delete(self.url_detail)
        amount = len(Datapoint.objects.all())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Datapoint.objects.count(), amount)

    def test_search(self):
        datapoint = Datapoint.objects.create(freq='m', name='TEST', date='2017-09-20', value=50.25)

        response = self.client.get('{}?search={}'.format(self.url_list, datapoint.name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(datapoint.name, response.data['results'][0]['name'], response.data)

    def test_filter(self):
        response = self.client.get('{}?freq={}&name={}&date={}&value={}'.format(
            self.url_list, self.datapoint.freq, self.datapoint.name, self.datapoint.date, self.datapoint.value))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(self.datapoint.name, response.data['results'][0]['name'], response.data)

    def test_order(self):
        datapoint = Datapoint.objects.create(freq='d', name='test', date='2000-01-01', value=42.00)
        amount = len(Datapoint.objects.all())

        response = self.client.get('{}?ordering=name'.format(self.url_list))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], amount)
        self.assertEqual(datapoint.name, response.data['results'][-1]['name'], response.data)

