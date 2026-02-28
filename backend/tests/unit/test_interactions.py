"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_with_zero_item_id() -> None:
    """Граничный случай: item_id=0."""
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 1),
        _make_log(3, 3, 0),
    ]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 2
    assert all(interaction.item_id == 0 for interaction in result)


def test_filter_with_negative_item_id() -> None:
    """Граничный случай: отрицательное значение item_id."""
    interactions = [
        _make_log(1, 1, -1),
        _make_log(2, 2, 1),
        _make_log(3, 3, -1),
    ]
    result = _filter_by_item_id(interactions, -1)
    assert len(result) == 2
    assert all(interaction.item_id == -1 for interaction in result)


def test_filter_no_matches_returns_empty() -> None:
    """Граничный случай: ни один элемент не совпадает с фильтром."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 2),
        _make_log(3, 3, 3),
    ]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_multiple_matches_same_item_id() -> None:
    """Граничный случай: несколько элементов с одинаковым item_id."""
    interactions = [
        _make_log(1, 1, 5),
        _make_log(2, 2, 5),
        _make_log(3, 3, 5),
        _make_log(4, 4, 10),
    ]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 3
    assert all(interaction.item_id == 5 for interaction in result)


def test_filter_with_large_item_id() -> None:
    """Граничный случай: очень большое значение item_id."""
    large_id = 2**31 - 1  # максимальное 32-битное знаковое целое
    interactions = [
        _make_log(1, 1, large_id),
        _make_log(2, 2, 1),
    ]
    result = _filter_by_item_id(interactions, large_id)
    assert len(result) == 1
    assert result[0].item_id == large_id
