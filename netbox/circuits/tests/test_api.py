from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from django.urls import reverse

from dcim.models import Site
from circuits.models import Circuit, CircuitTermination, CircuitType, Provider, TERM_SIDE_A, TERM_SIDE_Z
from users.models import Token


class ProviderTest(APITestCase):

    def setUp(self):

        user = User.objects.create(username='testuser', is_superuser=True)
        token = Token.objects.create(user=user)
        self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token.key)}

        self.provider1 = Provider.objects.create(name='Test Provider 1', slug='test-provider-1')
        self.provider2 = Provider.objects.create(name='Test Provider 2', slug='test-provider-2')
        self.provider3 = Provider.objects.create(name='Test Provider 3', slug='test-provider-3')

    def test_get_provider(self):

        url = reverse('circuits-api:provider-detail', kwargs={'pk': self.provider1.pk})
        response = self.client.get(url, **self.header)

        self.assertEqual(response.data['name'], self.provider1.name)

    def test_list_providers(self):

        url = reverse('circuits-api:provider-list')
        response = self.client.get(url, **self.header)

        self.assertEqual(response.data['count'], 3)

    def test_create_provider(self):

        data = {
            'name': 'Test Provider 4',
            'slug': 'test-provider-4',
        }

        url = reverse('circuits-api:provider-list')
        response = self.client.post(url, data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.count(), 4)

    def test_update_provider(self):

        data = {
            'name': 'Test Provider X',
            'slug': 'test-provider-x',
        }

        url = reverse('circuits-api:provider-detail', kwargs={'pk': self.provider1.pk})
        response = self.client.put(url, data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Provider.objects.count(), 3)
        self.assertEqual(Provider.objects.get(pk=self.provider1.pk).name, data['name'])
        self.assertEqual(Provider.objects.get(pk=self.provider1.pk).slug, data['slug'])

    def test_delete_provider(self):

        url = reverse('circuits-api:provider-detail', kwargs={'pk': self.provider1.pk})
        response = self.client.delete(url, **self.header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Provider.objects.count(), 2)


class CircuitTypeTest(APITestCase):

    def setUp(self):

        user = User.objects.create(username='testuser', is_superuser=True)
        token = Token.objects.create(user=user)
        self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token.key)}

        self.circuittype1 = CircuitType.objects.create(name='Test Circuit Type 1', slug='test-circuit-type-1')
        self.circuittype2 = CircuitType.objects.create(name='Test Circuit Type 2', slug='test-circuit-type-2')
        self.circuittype3 = CircuitType.objects.create(name='Test Circuit Type 3', slug='test-circuit-type-3')

    def test_get_circuittype(self):

        url = reverse('circuits-api:circuittype-detail', kwargs={'pk': self.circuittype1.pk})
        response = self.client.get(url, **self.header)

        self.assertEqual(response.data['name'], self.circuittype1.name)

    def test_list_circuittypes(self):

        url = reverse('circuits-api:circuittype-list')
        response = self.client.get(url, **self.header)

        self.assertEqual(response.data['count'], 3)

    def test_create_circuittype(self):

        data = {
            'name': 'Test Circuit Type 4',
            'slug': 'test-circuit-type-4',
        }

        url = reverse('circuits-api:circuittype-list')
        response = self.client.post(url, data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CircuitType.objects.count(), 4)

    def test_update_circuittype(self):

        data = {
            'name': 'Test Circuit Type X',
            'slug': 'test-circuit-type-x',
        }

        url = reverse('circuits-api:circuittype-detail', kwargs={'pk': self.circuittype1.pk})
        response = self.client.put(url, data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CircuitType.objects.count(), 3)
        self.assertEqual(CircuitType.objects.get(pk=self.circuittype1.pk).name, data['name'])
        self.assertEqual(CircuitType.objects.get(pk=self.circuittype1.pk).slug, data['slug'])

    def test_delete_circuittype(self):

        url = reverse('circuits-api:circuittype-detail', kwargs={'pk': self.circuittype1.pk})
        response = self.client.delete(url, **self.header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CircuitType.objects.count(), 2)


class CircuitTest(APITestCase):

    def setUp(self):

        user = User.objects.create(username='testuser', is_superuser=True)
        token = Token.objects.create(user=user)
        self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token.key)}

        self.provider1 = Provider.objects.create(name='Test Provider 1', slug='test-provider-1')
        self.provider2 = Provider.objects.create(name='Test Provider 2', slug='test-provider-2')
        self.circuittype1 = CircuitType.objects.create(name='Test Circuit Type 1', slug='test-circuit-type-1')
        self.circuittype2 = CircuitType.objects.create(name='Test Circuit Type 2', slug='test-circuit-type-2')
        self.circuit1 = Circuit.objects.create(cid='TEST0001', provider=self.provider1, type=self.circuittype1)
        self.circuit2 = Circuit.objects.create(cid='TEST0002', provider=self.provider1, type=self.circuittype1)
        self.circuit3 = Circuit.objects.create(cid='TEST0003', provider=self.provider1, type=self.circuittype1)

    def test_get_circuit(self):

        url = reverse('circuits-api:circuit-detail', kwargs={'pk': self.circuit1.pk})
        response = self.client.get(url, **self.header)

        self.assertEqual(response.data['cid'], self.circuit1.cid)

    def test_list_circuits(self):

        url = reverse('circuits-api:circuit-list')
        response = self.client.get(url, **self.header)

        self.assertEqual(response.data['count'], 3)

    def test_create_circuit(self):

        data = {
            'cid': 'TEST0004',
            'provider': self.provider1.pk,
            'type': self.circuittype1.pk,
        }

        url = reverse('circuits-api:circuit-list')
        response = self.client.post(url, data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Circuit.objects.count(), 4)

    def test_update_circuit(self):

        data = {
            'cid': 'TEST000X',
            'provider': self.provider2.pk,
            'type': self.circuittype2.pk,
        }

        url = reverse('circuits-api:circuit-detail', kwargs={'pk': self.circuit1.pk})
        response = self.client.put(url, data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Circuit.objects.count(), 3)
        self.assertEqual(Circuit.objects.get(pk=self.circuit1.pk).cid, data['cid'])
        self.assertEqual(Circuit.objects.get(pk=self.circuit1.pk).provider_id, data['provider'])
        self.assertEqual(Circuit.objects.get(pk=self.circuit1.pk).type_id, data['type'])

    def test_delete_circuit(self):

        url = reverse('circuits-api:circuit-detail', kwargs={'pk': self.circuit1.pk})
        response = self.client.delete(url, **self.header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Circuit.objects.count(), 2)


class CircuitTerminationTest(APITestCase):

    def setUp(self):

        user = User.objects.create(username='testuser', is_superuser=True)
        token = Token.objects.create(user=user)
        self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token.key)}

        provider = Provider.objects.create(name='Test Provider', slug='test-provider')
        circuittype = CircuitType.objects.create(name='Test Circuit Type', slug='test-circuit-type')
        self.circuit1 = Circuit.objects.create(cid='TEST0001', provider=provider, type=circuittype)
        self.circuit2 = Circuit.objects.create(cid='TEST0002', provider=provider, type=circuittype)
        self.circuit3 = Circuit.objects.create(cid='TEST0003', provider=provider, type=circuittype)
        self.site1 = Site.objects.create(name='Test Site 1', slug='test-site-1')
        self.site2 = Site.objects.create(name='Test Site 2', slug='test-site-2')
        self.circuittermination1 = CircuitTermination.objects.create(
            circuit=self.circuit1, term_side=TERM_SIDE_A, site=self.site1, port_speed=1000000
        )
        self.circuittermination2 = CircuitTermination.objects.create(
            circuit=self.circuit2, term_side=TERM_SIDE_A, site=self.site1, port_speed=1000000
        )
        self.circuittermination3 = CircuitTermination.objects.create(
            circuit=self.circuit3, term_side=TERM_SIDE_A, site=self.site1, port_speed=1000000
        )

    def test_get_circuittermination(self):

        url = reverse('circuits-api:circuittermination-detail', kwargs={'pk': self.circuittermination1.pk})
        response = self.client.get(url, **self.header)

        self.assertEqual(response.data['id'], self.circuittermination1.pk)

    def test_list_circuitterminations(self):

        url = reverse('circuits-api:circuittermination-list')
        response = self.client.get(url, **self.header)

        self.assertEqual(response.data['count'], 3)

    def test_create_circuittermination(self):

        data = {
            'circuit': self.circuit1.pk,
            'term_side': TERM_SIDE_Z,
            'site': self.site2.pk,
            'port_speed': 1000000,
        }

        url = reverse('circuits-api:circuittermination-list')
        response = self.client.post(url, data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CircuitTermination.objects.count(), 4)

    def test_update_circuittermination(self):

        data = {
            'circuit': self.circuit1.pk,
            'term_side': TERM_SIDE_Z,
            'site': self.site2.pk,
            'port_speed': 1000000,
        }

        url = reverse('circuits-api:circuittermination-detail', kwargs={'pk': self.circuittermination1.pk})
        response = self.client.put(url, data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CircuitTermination.objects.count(), 3)
        self.assertEqual(CircuitTermination.objects.get(pk=self.circuittermination1.pk).site_id, data['site'])
        self.assertEqual(CircuitTermination.objects.get(pk=self.circuittermination1.pk).term_side, data['term_side'])

    def test_delete_circuittermination(self):

        url = reverse('circuits-api:circuittermination-detail', kwargs={'pk': self.circuittermination1.pk})
        response = self.client.delete(url, **self.header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CircuitTermination.objects.count(), 2)