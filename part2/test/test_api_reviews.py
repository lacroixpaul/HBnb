import unittest
from app import create_app

class TestAPIReviews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()  # Crée ton application Flask ici
        cls.client = cls.app.test_client()

    def test_create_review(self):
        response = self.client.post('/reviews/', json={
            'text': 'Amazing place!',
            'rating': 5,
            'user_id': 'user123',
            'place_id': 'place123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Review successfully created', response.json.get('message'))

    def test_get_all_reviews(self):
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)

    def test_get_review_by_id(self):
        review_id = 'some_review_id'  # Remplace par un ID valide
        response = self.client.get(f'/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    # Plus de tests ici...
    
    @classmethod
    def tearDownClass(cls):
        # Nettoyage si nécessaire
        pass

if __name__ == '__main__':
    unittest.main()
