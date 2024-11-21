from typing import TYPE_CHECKING

from qgis.core import QgsApplication
from qgis.gui import QgisInterface
from qgis.processing import execAlgorithmDialog
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface

import wurman_points.resources  # noqa: F401
from wurman_points.about_dialog import AboutDialog
from wurman_points.processing import WurmanPointsAlgorithmProvider

if TYPE_CHECKING:
    assert isinstance(iface, QgisInterface)


class WurmanPointsPlugin:
    def __init__(self, _: QgisInterface):
        self.__provider = None
        self.__action = None

    def initProcessing(self):
        self.__provider = WurmanPointsAlgorithmProvider()
        QgsApplication.processingRegistry().addProvider(self.__provider)

    def initGui(self):
        self.initProcessing()

        self.__action = QAction(
            QIcon(":/plugins/wurman_points/icons/wurman_points.png"),
            self.tr("Create Wurman Points"),
            iface.mainWindow(),
        )
        self.__action.triggered.connect(self.__exec_algorithm)
        menu_name = self.tr("&Wurman Points")
        iface.addPluginToVectorMenu(menu_name, self.__action)

        for action in iface.vectorMenu().actions():
            if action.text() != menu_name:
                continue
            action.setIcon(
                QIcon(":/plugins/wurman_points/icons/wurman_points.png")
            )

        self.__show_help_action = QAction(
            QIcon(":/plugins/wurman_points/icons/wurman_points.png"),
            "Wurman Points",
        )
        self.__show_help_action.triggered.connect(self.__open_about_dialog)
        plugin_help_menu = iface.pluginHelpMenu()
        assert plugin_help_menu is not None
        plugin_help_menu.addAction(self.__show_help_action)

    def unload(self):
        if self.__action:
            iface.removePluginVectorMenu(
                self.tr("&Wurman Points"), self.__action
            )
        if self.__provider:
            QgsApplication.processingRegistry().removeProvider(self.__provider)

    def tr(self, string: str, context: str = "") -> str:
        if context == "":
            context = self.__class__.__name__
        return QgsApplication.translate(context, string)

    def __exec_algorithm(self):
        execAlgorithmDialog("wurman_points:create_wurman_points")

    def __open_about_dialog(self) -> None:
        dialog = AboutDialog("wurman_points")
        dialog.exec()