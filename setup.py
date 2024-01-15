#!/usr/bin/env python

from setuptools import setup, find_packages

NAME = "Orange3 Add-on Prototypes"

VERSION = "0.0.1"

DESCRIPTION = "Add-on containing prototype widgets"

PACKAGES = find_packages()

PACKAGE_DATA = {
    'orangecontrib.spectroscopy_prototypes': ['tutorials/*.ows'],
    'orangecontrib.spectroscopy_prototypes.widgets': ['icons/*'],
    'orangecontrib.matrix_prototypes': ['tutorials/*.ows'],
    'orangecontrib.matrix_prototypes.widgets': ['icons/*'],
}

INSTALL_REQUIRES = [
    'Orange3',
]

ENTRY_POINTS = {
    # Entry points that marks this package as an orange add-on. If set, addon will
    # be shown in the add-ons manager even if not published on PyPi.
    'orange3.addon': (
        'spectroscopy_prototypes = orangecontrib.spectroscopy_prototypes',
        'matrix_prototypes = orangecontrib.matrix_prototypes',
    ),
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        # Syntax: any_text = path.to.package.containing.tutorials
        'spectroscopy_prototypes_tutorials = orangecontrib.spectroscopy_prototypes.tutorials',
        'matrix_prototypes_tutorials = orangecontrib.matrix_prototypes.tutorials',
    ),

    # Entry point used to specify packages containing widgets.
    'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        'SpectroscopyPrototypes = orangecontrib.spectroscopy_prototypes.widgets',
        'MatrixPrototypes = orangecontrib.matrix_prototypes.widgets',
    ),

    # Register widget help
    "orange.canvas.help": (
        'html-index-spectroscopy = orangecontrib.spectroscopy_prototypes.widgets:WIDGET_HELP_PATH',
        'html-index-matrix = orangecontrib.matrix_prototypes.widgets:WIDGET_HELP_PATH',
        )
}

NAMESPACE_PACKAGES = ["orangecontrib"]

TEST_SUITE = "orangecontrib.spectroscopy_prototypes.tests.suite"


if __name__ == '__main__':
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS,
        namespace_packages=NAMESPACE_PACKAGES,
        zip_safe=False,
    )
