from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from .models import Survivor, Item
from .serializers import SurvivorSerializer, ItemSerializer
from api.models import Survivor, Item

def test_create_survivor(self):
    # Crie itens de teste no banco de dados
    item1 = Item.objects.create(name="Água", points=4)
    item2 = Item.objects.create(name="Comida", points=3)
    # ...

    client = APIClient()
    url = reverse("create_survivor")
    data = {
        "name": "Test Survivor",
        "age": 30,
        "gender": "M",
        "last_location_latitude": -23.55052,
        "last_location_longitude": -46.633308,
        "items": [
            {
                "item": item1.id,
                "quantity": 2
            },
            {
                "item": item2.id,
                "quantity": 3
            },
            # ... outras informações de itens
        ],
    }
    response = client.post(url, data, format="json")
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Survivor.objects.count(), 1)
    self.assertEqual(Survivor.objects.get().name, "Test Survivor")

def test_create_survivor_invalid_data(self):
    client = APIClient()
    url = reverse("create_survivor")
    data = {
        "name": "",
        "age": -1,
        "gender": "X",
        "last_location_latitude": -200,
        "last_location_longitude": -200,
    }
    response = client.post(url, data, format="json")
    self.assertEqual(response.status_code, 400)

def test_update_survivor_location(self):
    survivor = Survivor.objects.create(
        name="Test Survivor",
        age=30,
        gender="M",
        last_location_latitude=-23.55052,
        last_location_longitude=-46.633308,
    )

    client = APIClient()
    url = reverse("update_survivor_location", args=[survivor.id])
    data = {
        "last_location_latitude": -23.55152,
        "last_location_longitude": -46.634308,
    }
    response = client.patch(url, data, format="json")
    self.assertEqual(response.status_code, 200)
    survivor.refresh_from_db()
    self.assertEqual(survivor.last_location_latitude, -23.55152)
    self.assertEqual(survivor.last_location_longitude, -46.634308)

def test_update_nonexistent_survivor_location(self):
    client = APIClient()
    url = reverse("update_survivor_location", args=[99999])
    data = {
        "last_location_latitude": -23.55152,
        "last_location_longitude": -46.634308,
    }
    response = client.patch(url, data, format="json")
    self.assertEqual(response.status_code, 404)

def test_update_survivor_location_invalid_data(self):
    survivor = Survivor.objects.create(
        name="Test Survivor",
        age=30,
        gender="M",
        last_location_latitude=-23.55052,
        last_location_longitude=-46.633308,
    )

    client = APIClient()
    url = reverse("update_survivor_location", args=[survivor.id])
    data = {
        "last_location_latitude": -200,
        "last_location_longitude": -200,
    }
    response = client.patch(url, data, format="json")
    self.assertEqual(response.status_code, 400)


class TradeTestCase(APITestCase):
    def setUp(self):
        # Create sample survivors and items for testing
        self.survivor1 = Survivor.objects.create(
            name="Survivor 1",
            age=35,
            gender="M",
            last_location_latitude=-23.55052,
            last_location_longitude=-46.633308,
        )

        self.survivor2 = Survivor.objects.create(
            name="Survivor 2",
            age=28,
            gender="F",
            last_location_latitude=-23.55152,
            last_location_longitude=-46.634308,
        )

        self.item1 = Item.objects.create(name="Item 1", points=4)
        self.item2 = Item.objects.create(name="Item 2", points=3)

        self.survivor1.inventory.add(self.item1, through_defaults={"quantity": 2})
        self.survivor1.inventory.add(self.item2, through_defaults={"quantity": 3})
        self.survivor2.inventory.add(self.item1, through_defaults={"quantity": 1})
        self.survivor2.inventory.add(self.item2, through_defaults={"quantity": 2})

    def test_valid_trade(self):
        client = APIClient()
        url = reverse("trade_items")

        data = {
            "trader1_id": self.survivor1.id,
            "trader2_id": self.survivor2.id,
            "trader1_items": [
                {"item_id": self.item1.id, "quantity": 1},
                {"item_id": self.item2.id, "quantity": 2},
            ],
            "trader2_items": [
                {"item_id": self.item1.id, "quantity": 1},
                {"item_id": self.item2.id, "quantity": 1},
            ],
        }

        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Trade successful")

        # Refresh survivor instances from the database
        self.survivor1.refresh_from_db()
        self.survivor2.refresh_from_db()

        # Check if the items were traded correctly
        self.assertEqual(self.survivor1.inventory.get(item=self.item1).quantity, 1)
        self.assertEqual(self.survivor1.inventory.get(item=self.item2).quantity, 1)
        self.assertEqual(self.survivor2.inventory.get(item=self.item1).quantity, 2)
        self.assertEqual(self.survivor2.inventory.get(item=self.item2).quantity, 3)

    # Add more test cases as needed