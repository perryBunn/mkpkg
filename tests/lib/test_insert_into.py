from mkpkg.lib.helpers import insert_into


def test_insert_template_1():
    template = "[NAME]_v[V]r[R].tar.gz"
    res = insert_into(template, "test", r"\[NAME\]")
    res = insert_into(res, 1 , r"\[V\]")
    res = insert_into(res, 0 , r"\[R\]")
    assert res == "test_v1r0.tar.gz"


def test_insert_template_2():
    template = "[NAME]_v[V]r[R]_[CONTENT].tar.gz"
    res = insert_into(template, "test", r"\[NAME\]")
    res = insert_into(res, 1 , r"\[V\]")
    res = insert_into(res, 0 , r"\[R\]")
    res = insert_into(res, "pytest")
    assert res == "test_v1r0_pytest.tar.gz"


def test_insert_template_3():
    template = "[NAME]_[CONTENT].tar.gz"
    res = insert_into(template, "test", r"\[NAME\]")
    res = insert_into(res, "pytest")
    assert res == "test_pytest.tar.gz"


def test_insert_template_4():
    template = "[NAME]_v[V]r[R]_[DATE].tar.gz"
    res = insert_into(template, "test", r"\[NAME\]")
    res = insert_into(res, 1 , r"\[V\]")
    res = insert_into(res, 0 , r"\[R\]")
    res = insert_into(res, "19700101", r"\[DATE\]")
    assert res == "test_v1r0_19700101.tar.gz"


def test_insert_template_5():
    template = "[NAME]_v[V]r[R]_[CONTENT]_[DATE].tar.gz"
    res = insert_into(template, "test", r"\[NAME\]")
    res = insert_into(res, 1 , r"\[V\]")
    res = insert_into(res, 0 , r"\[R\]")
    res = insert_into(res, "pytest")
    res = insert_into(res, "19700101", r"\[DATE\]")
    assert res == "test_v1r0_pytest_19700101.tar.gz"


def test_insert_template_6():
    template = "[NAME]_[CONTENT]_[DATE].tar.gz"
    res = insert_into(template, "test", r"\[NAME\]")
    res = insert_into(res, "pytest")
    res = insert_into(res, "19700101", r"\[DATE\]")
    assert res == "test_pytest_19700101.tar.gz"


def test_insert_template_7():
    template = "[NAME]_v[V]r[R]_deliv[H]_[DATE].tar.gz"
    res = insert_into(template, "test", r"\[NAME\]")
    res = insert_into(res, 1 , r"\[V\]")
    res = insert_into(res, 0 , r"\[R\]")
    res = insert_into(res, 1, r"\[H\]")
    res = insert_into(res, "19700101", r"\[DATE\]")
    assert res == "test_v1r0_deliv1_19700101.tar.gz"


def test_insert_template_8():
    template = "[NAME]_v[V]r[R]_deliv[H]_[CONTENT]_[DATE].tar.gz"
    res = insert_into(template, "test", r"\[NAME\]")
    res = insert_into(res, 1 , r"\[V\]")
    res = insert_into(res, 0 , r"\[R\]")
    res = insert_into(res, 1, r"\[H\]")
    res = insert_into(res, "pytest")
    res = insert_into(res, "19700101", r"\[DATE\]")
    assert res == "test_v1r0_deliv1_pytest_19700101.tar.gz"
