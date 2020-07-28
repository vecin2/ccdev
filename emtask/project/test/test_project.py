import pytest


# for module in project.modules():
#    module.add_release()
def test_modules_return_modules(emproject):
    emproject.add_sqlmodule("MyTestModule")
    assert "MyTestModule" in [module.name for module in emproject.sqlmodules()]


def test_add_release_to_module(emproject):
    module = emproject.add_sqlmodule("MyTestModule")
    module.add_release("Pacificorp_R_0_0_1")
    module.add_release("Pacificorp_R_0_0_2")

    assert ["Pacificorp_R_0_0_1", "Pacificorp_R_0_0_2"] == [
        release.name for release in module.releases()
    ]


def test_add_release_to_module(emproject):
    module = emproject.add_sqlmodule("MyTestModule")
    module.add_release("Pacificorp_R_0_0_1")

    assert "Pacificorp_R_0_0_1" in [release.name for release in module.releases()]
