# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from datapoint.models import Datapoint


class DatapointTests(APITestCase):
    def setUp(self):
        """
        Set up every test. Create admin user and log in it.  
        """
        self.user = User.objects.create(username='test', is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_create(self):
        """Creates a new object in the database with the fields name, freq,
        date, and value, which is passed in as a json object in a post request.
        The single new entry should be successfully added and have the name
        'test'.
        """
        url = '/datapoints/'
        data = {
            'name': 'test',
            'freq': 'm',
            'date': '2018-01-01',
            'value': 42.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Datapoint.objects.count(), 1)
        self.assertEqual(Datapoint.objects.get().name, 'test')

    def test_list(self):
        """A GET request should recover a list of all items in the database on
        the /datapoints/ endpoint in JSON format.
        """
        Datapoint.objects.create(freq='m', name='BRENT', date='2017-09-20', value=50.25)
        Datapoint.objects.create(freq='d', name='BRENT', date='2017-09-21', value=42.00)

        url = '/datapoints/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve(self):
        """When navigating to a specific datapoint url, the response header
        should match the corresponding id and name for that item in the database.
        """
        datapoint = Datapoint.objects.create(freq='m', name='BRENT', date='2017-09-20', value=50.25)

        url = '/datapoints/{}/'.format(datapoint.pk)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], datapoint.id)
        self.assertEqual(response.data['name'], datapoint.name)

    def test_update(self):
        """When editing the information in a form on a particular datapoint
        url, the existing fields in the database should match the data in the
        response header, and the updated data should also match.
        """
        datapoint = Datapoint.objects.create(freq='m', name='BRENT', date='2017-09-20', value=50.25)

        url = '/datapoints/{}/'.format(datapoint.pk)
        data = {'value': 42.0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], datapoint.id)
        self.assertEqual(response.data['name'], datapoint.name)
        self.assertEqual(response.data['value'], 42.0)

    def test_delete(self):
        """After deleting the item belonging to a particular datapoint url, the
        item should be removed from the database.
        """
        datapoint = Datapoint.objects.create(freq='m', name='BRENT', date='2017-09-20', value=50.25)

        url = '/datapoints/{}/'.format(datapoint.pk)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Datapoint.objects.count(), 0)
