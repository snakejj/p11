from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from .. import views

from django.test import RequestFactory
import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


def test_complete_with_term():
    mixer.blend('products.Product', product_name="Nutella", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nuts", nutrition_grade_fr="d", category_id=2)
    get = {"term": "nu"}
    req = RequestFactory().get('/', data=get)
    resp = views.complete(req)

    assert "Nutella" in str(resp.getvalue()), \
        'The product Nutella appear when typing only "nu"'

def test_complete_with_term_and_only_15_results_displayed():
    mixer.blend('products.Product', product_name="Nutella1", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella2", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella3", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella4", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella5", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella6", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella7", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella8", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella9", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella10", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella11", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella12", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella13", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella14", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella15", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella16", nutrition_grade_fr="e", category_id=2)
    get = {"term": "nu"}
    req = RequestFactory().get('/', data=get)
    resp = views.complete(req)

    assert "Nutella16" not in str(resp.getvalue()), \
        'Show only 15 results'


def test_complete_with_term_sorted_by_nutrition_grade():
    mixer.blend('products.Product', product_name="Nutella1", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella2", nutrition_grade_fr="a", category_id=2)
    mixer.blend('products.Product', product_name="Nutella3", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella4", nutrition_grade_fr="b", category_id=2)
    mixer.blend('products.Product', product_name="Nutella5", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella6", nutrition_grade_fr="c", category_id=2)
    mixer.blend('products.Product', product_name="Nutella7", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella8", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella9", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella10", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella11", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella12", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella13", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella14", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella15", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella16", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella17", nutrition_grade_fr="e", category_id=2)
    mixer.blend('products.Product', product_name="Nutella18", nutrition_grade_fr="e", category_id=2)
    get = {"term": "nu"}
    req = RequestFactory().get('/', data=get)
    resp = views.complete(req)

    assert "Nutella2" and "Nutella4" and "Nutella6" not in str(resp.getvalue()), \
        'Only The 15 products with the worst nutrition grade should appear'

def test_complete_without_term():
    get = {"term": ""}
    req = RequestFactory().get('/', data=get)
    resp = views.complete(req)

    assert resp.status_code == 200, \
        'Is working without any term entered'

#


# def test_if_view_favorites_is_displaying_when_logged_in_with_no_favorites_yet_for_this_user(self):
#     user = mixer.blend('auth.User', id=2)
#     mixer.blend('favorites.Favorites', user_id=3)
#     req = RequestFactory().get('/')
#     req.user = user
#
#     resp = views.favorites(req)
#
#     assert resp.status_code == 200, \
#         'Is callable by logged-in user with no prior favorites'
#     assert "Aucuns substituts" in str(resp.getvalue()), \
#         'Is returning a False boolean called empty for the template to display, when logged in,' \
#         ' a text saying there are no substitutes yet'
#
# def test_if_view_favorites_is_displaying_previous_favorites_when_logged_in(self):
#     user = mixer.blend('auth.User', id=2)
#     mixer.blend('favorites.Favorites', user_id=2)
#     req = RequestFactory().get('/')
#     req.user = user
#
#     resp = views.favorites(req)
#
#     assert resp.status_code == 200, 'Is callable by logged-in user with prior favorites'
#     assert "Voici la liste de vos aliments" in str(resp.getvalue()), \
#         'Is returning a True boolean called empty for the template to display the previous favorites'
#
# def test_if_view_favorites_is_saving_favorites_when_logged_in(self):
#     objproduct_initial = mixer.blend('products.Product')
#     objproduct_substitute = mixer.blend('products.Product')
#     user = mixer.blend('auth.User')
#     post = {
#         "user_id": user.id,
#         "product": objproduct_initial.code,
#         "substitute": objproduct_substitute.code
#     }
#     req = RequestFactory().post('/', data=post)
#     req.user = user
#     resp = views.favorites(req)
#
#     assert resp.status_code == 200, \
#         'Should save a new entry in favorites database'
#     assert str(post['product']) and str(post['substitute']) in str(resp.getvalue()), \
#         'Should display the newly saved product on the favorites page'
#
# def test_if_view_favorites_is_preventing_saving_duplicates_in_favorites_when_logged_in(self):
#     objproduct_initial = mixer.blend('products.Product')
#     objproduct_substitute = mixer.blend('products.Product')
#     mixer.blend(
#         'favorites.Favorites',
#         user_id=2,
#         product_id=objproduct_initial.code,
#         substitute_id=objproduct_substitute.code)
#
#     user = mixer.blend('auth.User', user_id=2)
#     post = {
#         "user_id": user.id,
#         "product": objproduct_initial.code,
#         "substitute": objproduct_substitute.code
#     }
#     req = RequestFactory().post('/', data=post)
#     req.user = user
#     resp = views._add_favorites(req)
#
#     assert resp is True, 'Should return True for the boolean called "already exists"'
