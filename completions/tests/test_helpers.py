from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from .. import views, helpers

from django.test import RequestFactory, override_settings
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


@override_settings(COMPLETIONS_FIELD=1)
@pytest.mark.xfail(raises=ImproperlyConfigured)
def test_complete_with_improperly_configured_completions_field():

    get = {"term": ""}
    req = RequestFactory().get('/', data=get)
    views.complete(req)


@override_settings(COMPLETIONS_ORDER=1)
@pytest.mark.xfail(raises=ImproperlyConfigured)
def test_complete_with_improperly_configured_field_completions_order():

    get = {"term": ""}
    req = RequestFactory().get('/', data=get)
    views.complete(req)


@override_settings(COMPLETIONS_METHOD=1)
@pytest.mark.xfail(raises=ImproperlyConfigured)
def test_complete_with_improperly_configured_field_completions_method():

    get = {"term": ""}
    req = RequestFactory().get('/', data=get)
    views.complete(req)


@override_settings(COMPLETIONS_MODEL="dsqdsq.dsqdsq")
@pytest.mark.xfail(raises=ImproperlyConfigured)
def test_complete_with_improperly_configured_field_completions_model_lookup_error():

    get = {"term": ""}
    req = RequestFactory().get('/', data=get)
    views.complete(req)

@override_settings(COMPLETIONS_MODEL="dsqdsq-dsqdsq")
@pytest.mark.xfail(raises=ImproperlyConfigured)
def test_complete_with_improperly_configured_field_completions_model_value_error():
    get = {"term": ""}
    req = RequestFactory().get('/', data=get)
    views.complete(req)