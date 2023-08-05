""""""

# Standard library modules.
import functools
import abc

# Third party modules.
from qtpy import QtCore, QtGui, QtWidgets

# Local modules.
from pymontecarlo.options.material import Material, VACUUM
from pymontecarlo.options.composition import \
    generate_name, calculate_density_kg_per_m3, from_formula
from pymontecarlo.program.validator import Validator
from pymontecarlo.util.tolerance import tolerance_to_decimals

from pymontecarlo_gui.options.composition import CompositionTableWidget
from pymontecarlo_gui.widgets.lineedit import \
    ColoredLineEdit, ColoredFloatLineEdit
from pymontecarlo_gui.widgets.periodictable import PeriodicTableWidget
from pymontecarlo_gui.widgets.field import Field, FieldLayout
from pymontecarlo_gui.widgets.color import ColorDialogButton, check_color
from pymontecarlo_gui.widgets.icon import load_icon
from pymontecarlo_gui.util.metaclass import QABCMeta
from pymontecarlo_gui.util.validate import \
    Validable, VALID_BACKGROUND_STYLESHEET, INVALID_BACKGROUND_STYLESHEET

# Globals and constants variables.
DEFAULT_VALIDATOR = Validator()

#--- Mix-ins

class MaterialValidatorMixin:

    def validator(self):
        if not hasattr(self, '_validator'):
            self._validator = DEFAULT_VALIDATOR
        return self._validator

class MaterialAbstractViewMixin(metaclass=QABCMeta):

    @abc.abstractmethod
    def _get_model(self):
        raise NotImplementedError

    def addMaterial(self, material):
        self._get_model().addMaterial(material)

    def removeMaterial(self, material):
        self._get_model().removeMaterial(material)

    def takeMaterial(self, row):
        model = self._get_model()
        model.removeMaterial(model.data(model.createIndex(row, 0), QtCore.Qt.UserRole))

    def clear(self):
        self._get_model().clearMaterials()

    def materials(self):
        return self._get_model().materials()

    def setMaterials(self, materials):
        self._get_model().setMaterials(materials)

    def material(self, row):
        return self._get_model().material(row)

class MaterialVacuumMixin:

    def allowVacuum(self):
        return VACUUM in self.materials()

    def setAllowVacuum(self, allow):
        if allow:
            self.addMaterial(VACUUM)
        else:
            self.removeMaterial(VACUUM)

#--- Validators

class FormulaValidator(QtGui.QRegExpValidator):

    def __init__(self):
        super().__init__(QtCore.QRegExp(r'^[\w ]+$'))

    def validate(self, input, pos):
        state, input, pos = super().validate(input, pos)
        if state == QtGui.QValidator.Invalid:
            return state, input, pos

        try:
            from_formula(input)
        except:
            return QtGui.QValidator.Intermediate, input, pos

        return QtGui.QValidator.Acceptable, input, pos

#--- Widgets

class MaterialNameField(Field):

    def __init__(self):
        super().__init__()

        # Variables
        self._composition = {}

        # Widgets
        self._widget = ColoredLineEdit()
        self._widget.setEnabled(False)
        self._widget.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r"^(?!\s*$).+")))

        self._suffix = QtWidgets.QCheckBox('auto')
        self._suffix.setChecked(True)

        # Signals
        self._widget.textChanged.connect(self.fieldChanged)
        self._suffix.stateChanged.connect(self._on_auto_changed)

    def _on_auto_changed(self, *args):
        self._widget.setEnabled(not self._suffix.isChecked())
        self._update_name()

    def _update_name(self):
        if not self._suffix.isChecked():
            return

        try:
            name = generate_name(self._composition)
        except:
            name = ''

        self.setName(name, user_modified=False)

    def title(self):
        return 'Name'

    def widget(self):
        return self._widget

    def suffixWidget(self):
        return self._suffix

    def name(self):
        return self._widget.text()

    def setName(self, name, user_modified=True):
        self._widget.setText(name)
        self._suffix.setChecked(not user_modified)
        self.fieldChanged.emit()

    def composition(self):
        return self._composition

    def setComposition(self, composition):
        self._composition = composition.copy()
        self._update_name()

class MaterialFormulaField(Field):

    def __init__(self):
        super().__init__()

        # Widgets
        self._widget = ColoredLineEdit()
        self._widget.setValidator(FormulaValidator())
        self._widget.textChanged.emit('')

        # Signals
        self._widget.textChanged.connect(self.fieldChanged)

    def title(self):
        return 'Formula'

    def widget(self):
        return self._widget

    def formula(self):
        return self._widget.text()

    def setFormula(self, formula):
        self._widget.setText(formula)

class MaterialDensityField(Field):

    def __init__(self):
        super().__init__()

        # Variables
        self._composition = {}

        # Widgets
        self._widget = ColoredFloatLineEdit()
        decimals = tolerance_to_decimals(Material.DENSITY_TOLERANCE_kg_per_m3) + 3
        self._widget.setRange(0.0, float('inf'), decimals)
        self._widget.setValue(0.0)
        self._widget.setEnabled(False)

        self._suffix = QtWidgets.QCheckBox('user defined')
        self._suffix.setChecked(False)

        # Signals
        self._widget.valueChanged.connect(self.fieldChanged)
        self._suffix.stateChanged.connect(self._on_user_defined_changed)

    def _on_user_defined_changed(self, *args):
        self._widget.setEnabled(self._suffix.isChecked())
        self._update_density()

    def _update_density(self):
        if self._suffix.isChecked():
            return

        try:
            density_kg_per_m3 = calculate_density_kg_per_m3(self._composition)
        except:
            density_kg_per_m3 = 0.0

        self.setDensity_kg_per_m3(density_kg_per_m3, user_modified=False)

    def title(self):
        return 'Density [g/cm<sup>3</sup>]'

    def widget(self):
        return self._widget

    def suffixWidget(self):
        return self._suffix

    def density_kg_per_m3(self):
        return self._widget.value() * 1e3

    def setDensity_kg_per_m3(self, density_kg_per_m3, user_modified=True):
        self._widget.setValue(density_kg_per_m3 / 1e3)
        self._suffix.setChecked(user_modified)
        self.fieldChanged.emit()

    def composition(self):
        return self._composition

    def setComposition(self, composition):
        self._composition = composition.copy()
        self._update_density()

class MaterialColorField(Field):

    def __init__(self):
        super().__init__()

        # Widgets
        self._widget = ColorDialogButton()
        self._widget.setColor(next(Material.COLOR_CYCLER))

        # Signals
        self._widget.colorChanged.connect(self.fieldChanged)

    def title(self):
        return 'Color'

    def widget(self):
        return self._widget

    def color(self):
        return self._widget.rgba()

    def setColor(self, color):
        self._widget.setColor(color)

class MaterialWidget(QtWidgets.QWidget, Validable, MaterialValidatorMixin,
                     metaclass=QABCMeta):

    materialsChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def isValid(self):
        if not super().isValid():
            return False

        try:
            materials = self.materials()
        except:
            return False

        if not materials:
            return False

        try:
            for material in materials:
                material = self.validator().validate_material(material, None)
        except Exception:
            return False

        return True

    @abc.abstractmethod
    def materials(self):
        raise NotImplementedError

class MaterialPureWidget(MaterialWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.wdg_periodic_table = PeriodicTableWidget()
        self.wdg_periodic_table.setMultipleSelection(True)

        # Layouts
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.wdg_periodic_table)
        self.setLayout(layout)

        # Signals
        self.wdg_periodic_table.selectionChanged.connect(self.materialsChanged)

    def isValid(self):
        return super().isValid() and bool(self.wdg_periodic_table.selection())

    def materials(self):
        materials = []
        for z in self.wdg_periodic_table.selection():
            materials.append(Material.pure(z))
        return tuple(materials)

class MaterialFormulaWidget(MaterialWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.field_formula = MaterialFormulaField()

        self.field_density = MaterialDensityField()

        self.field_color = MaterialColorField()

        # Layouts
        layout = FieldLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLabelField(self.field_formula)
        layout.addLabelField(self.field_density)
        layout.addLabelField(self.field_color)
        self.setLayout(layout)

        # Signals
        self.field_formula.fieldChanged.connect(self._on_formula_changed)
        self.field_formula.fieldChanged.connect(self.materialsChanged)
        self.field_density.fieldChanged.connect(self.materialsChanged)
        self.field_color.fieldChanged.connect(self.materialsChanged)

    def _on_formula_changed(self):
        try:
            composition = from_formula(self.field_formula.formula())
        except:
            composition = {}
        self.field_density.setComposition(composition)

    def isValid(self):
        return super().isValid() and \
            self.field_formula.isValid() and \
            self.field_density.isValid() and \
            self.field_color.isValid()

    def materials(self):
        try:
            formula = self.field_formula.formula()
            density_kg_per_m3 = self.field_density.density_kg_per_m3()
            color = self.field_color.color()
            return (Material.from_formula(formula, density_kg_per_m3, color),)
        except:
            return ()

class MaterialAdvancedWidget(MaterialWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.field_name = MaterialNameField()

        self.field_density = MaterialDensityField()

        self.field_color = MaterialColorField()

        self.tbl_composition = CompositionTableWidget()

        # Layouts
        lyt_top = FieldLayout()
        lyt_top.addLabelField(self.field_name)
        lyt_top.addLabelField(self.field_density)
        lyt_top.addLabelField(self.field_color)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(lyt_top)
        layout.addWidget(self.tbl_composition)
        self.setLayout(layout)

        # Signals
        self.field_name.fieldChanged.connect(self.materialsChanged)
        self.field_density.fieldChanged.connect(self.materialsChanged)
        self.field_color.fieldChanged.connect(self.materialsChanged)
        self.tbl_composition.compositionChanged.connect(self.materialsChanged)
        self.tbl_composition.compositionChanged.connect(self._on_composition_changed)

    def _on_composition_changed(self):
        composition = self.tbl_composition.composition()
        self.field_name.setComposition(composition)
        self.field_density.setComposition(composition)

    def isValid(self):
        return super().isValid() and \
            self.field_name.isValid() and \
            self.field_density.isValid() and \
            self.field_color.isValid() and \
            self.tbl_composition.isValid()

    def materials(self):
        try:
            name = self.field_name.name()

            composition = self.tbl_composition.composition()
            if not composition:
                return ()

            density_kg_per_m3 = self.field_density.density_kg_per_m3()

            color = self.field_color.color()

            return (Material(name, composition, density_kg_per_m3, color),)
        except:
            return ()

    def setMaterial(self, material):
        self.field_name.setName(material.name)
        self.tbl_composition.setComposition(material.composition)
        self.field_density.setDensity_kg_per_m3(material.density_kg_per_m3)
        self.field_color.setColor(material.color)

class MaterialDialog(QtWidgets.QDialog):

    def __init__(self, material_widget_class, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Material')

        # Variables
        self._materials = []

        # Widgets
        self.wdg_material = material_widget_class()

        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | \
                                                  QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        # Layouts
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.wdg_material)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

        # Signals
        self.buttons.accepted.connect(self._on_ok)
        self.buttons.rejected.connect(self._on_cancel)

        self.wdg_material.materialsChanged.connect(self._on_materials_changed)

    def _on_ok(self):
        self._materials.clear()
        self._materials.extend(self.wdg_material.materials())
        self.accept()

    def _on_cancel(self):
        self._materials.clear()
        self.reject()

    def _on_materials_changed(self):
        valid = self.wdg_material.isValid()
        self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(valid)

    def materials(self):
        return self._materials

class MaterialModel(QtCore.QAbstractListModel, MaterialValidatorMixin):

    def __init__(self):
        super().__init__()

        # Variables
        self._materials = []

    def rowCount(self, parent=None):
        return len(self._materials)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        material = self._materials[row]

        if role == QtCore.Qt.DisplayRole:
            return material.name

        elif role == QtCore.Qt.UserRole:
            return material

        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter

        elif role == QtCore.Qt.DecorationRole:
            return check_color(material.color)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False

        if role != QtCore.Qt.EditRole:
            return False

        try:
            self.validator().validate_material(value, None)
        except:
            return False

        row = index.row()
        self._materials[row] = value

        self.dataChanged.emit(index, index)
        return True

    def _add_material(self, material):
        material = self.validator().validate_material(material, None)
        if material in self._materials:
            return False
        self._materials.append(material)
        return True

    def addMaterial(self, material):
        added = self._add_material(material)
        if added:
            self.modelReset.emit()
        return added

    def updateMaterial(self, row, material):
        self._materials[row] = material
        self.modelReset.emit()

    def removeMaterial(self, material):
        if material not in self._materials:
            return False
        self._materials.remove(material)
        self.modelReset.emit()
        return True

    def clearMaterials(self):
        self._materials.clear()
        self.modelReset.emit()

    def hasMaterials(self):
        return bool(self._materials)

    def material(self, row):
        return self._materials[row]

    def materials(self):
        return tuple(self._materials)

    def setMaterials(self, materials):
        self.clearMaterials()
        for material in materials:
            self._add_material(material)
        self.modelReset.emit()

class MaterialToolbar(QtWidgets.QToolBar):

    def __init__(self, listview, parent=None):
        super().__init__(parent)

        # Variables
        self.listview = listview

        # Actions
        self.act_add_pure = self.addAction(QtGui.QIcon.fromTheme("list-add"), "Pure")
        self.act_add_pure.setToolTip('Add pure material')

        self.act_add_formula = self.addAction(load_icon('material-add-formula.svg'), "Formula")
        self.act_add_formula.setToolTip('Add material from a formula')

        self.act_add_material = self.addAction(load_icon('material-add-advanced.svg'), "Advanced")
        self.act_add_material.setToolTip('Add material from composition')

        self.act_remove = QtWidgets.QAction()
        self.act_remove.setIcon(QtGui.QIcon.fromTheme("list-remove"))
        self.act_remove.setToolTip('Remove')
        self.act_remove.setEnabled(False)
        self.act_remove.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.act_remove.setShortcut(QtGui.QKeySequence.Delete)

        self.act_clear = QtWidgets.QAction()
        self.act_clear.setIcon(QtGui.QIcon.fromTheme("edit-clear"))
        self.act_clear.setToolTip('Clear')
        self.act_clear.setEnabled(False)

        # Widgets
        tool_remove = QtWidgets.QToolButton()
        tool_remove.setDefaultAction(self.act_remove)
        self.addWidget(tool_remove)

        tool_clear = QtWidgets.QToolButton()
        tool_clear.setDefaultAction(self.act_clear)
        self.addWidget(tool_clear)

        # Signals
        self.listview.model().modelReset.connect(self._on_data_changed)
        self.listview.selectionModel().selectionChanged.connect(self._on_data_changed)

        self.act_add_pure.triggered.connect(functools.partial(self._on_add_material, MaterialPureWidget))
        self.act_add_formula.triggered.connect(functools.partial(self._on_add_material, MaterialFormulaWidget))
        self.act_add_material.triggered.connect(functools.partial(self._on_add_material, MaterialAdvancedWidget))
        self.act_remove.triggered.connect(self._on_remove_material)
        self.act_clear.triggered.connect(self._on_clear_materials)

    def _on_data_changed(self):
        model = self.listview.model()
        has_rows = model.hasMaterials()

        selection_model = self.listview.selectionModel()
        has_selection = selection_model.hasSelection()

        self.act_remove.setEnabled(has_rows and has_selection)
        self.act_clear.setEnabled(has_rows)

    def _on_add_material(self, material_widget_class):
        dialog = MaterialDialog(material_widget_class)
        dialog.setWindowTitle('Add material')

        if not dialog.exec_():
            return

        for material in dialog.materials():
            self.listview.model().addMaterial(material)

    def _on_remove_material(self):
        selection_model = self.listview.selectionModel()
        if not selection_model.hasSelection():
            return

        indexes = selection_model.selectedIndexes()
        model = self.listview.model()
        for row in reversed([index.row() for index in indexes]):
            model.removeMaterial(model.data(model.createIndex(row, 0), QtCore.Qt.UserRole))

    def _on_clear_materials(self):
        model = self.listview.model()
        model.clearMaterials()

class MaterialsWidget(QtWidgets.QWidget, MaterialAbstractViewMixin):

    materialsChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Variables
        model = MaterialModel()

        # Widgets
        self.listview = QtWidgets.QListView()
        self.listview.setModel(model)

        self.toolbar = MaterialToolbar(self.listview)

        # Layouts
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.listview)
        layout.addWidget(self.toolbar, 0, QtCore.Qt.AlignRight)
        self.setLayout(layout)

        # Signals
        self.listview.doubleClicked.connect(self._on_double_clicked)
        model.dataChanged.connect(self._on_data_changed)
        model.modelReset.connect(self._on_data_changed)

    def _get_model(self):
        return self.listview.model()

    def _on_double_clicked(self, index):
        row = index.row()
        material = self.material(row)

        dialog = MaterialDialog(MaterialAdvancedWidget)
        dialog.setWindowTitle('Edit material')
        dialog.wdg_material.setMaterial(material)

        if not dialog.exec_():
            return

        materials = dialog.materials()
        if not materials:
            return

        assert len(materials) == 1
        self._get_model().updateMaterial(row, materials[0])

    def _on_data_changed(self):
        self.materialsChanged.emit()

class MaterialComboBox(QtWidgets.QWidget,
                       MaterialAbstractViewMixin,
                       MaterialVacuumMixin):

    currentMaterialChanged = QtCore.Signal(Material)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Variables
        model = MaterialModel()

        # Widgets
        self.combobox = QtWidgets.QComboBox()
        self.combobox.setModel(model)
        self.combobox.setEditable(False)
        self.combobox.setCurrentIndex(0)

        # Layouts
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.combobox)
        self.setLayout(layout)

        # Signals
        model.modelReset.connect(self._on_model_reset)
        self.combobox.currentIndexChanged.connect(self._on_current_index_changed)

    def _get_model(self):
        return self.combobox.model()

    def _on_model_reset(self, *args):
        if self.combobox.currentIndex() < 0:
            self.combobox.setCurrentIndex(0)

    def _on_current_index_changed(self, index):
        self.currentMaterialChanged.emit(self.currentMaterial())

    def currentMaterial(self):
        row = self.combobox.currentIndex()
        return self._get_model().material(row)

    def setCurrentMaterial(self, material):
        materials = self.materials()
        try:
            row = materials.index(material)
        except ValueError:
            row = -1
        self.combobox.setCurrentIndex(row)

class CheckableMaterialModel(MaterialModel):

    def __init__(self):
        super().__init__()

        self._selection = []

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == QtCore.Qt.CheckStateRole:
            row = index.row()
            return QtCore.Qt.Checked if self._selection[row] else QtCore.Qt.Unchecked

        return super().data(index, role)

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsUserCheckable

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False

        if role == QtCore.Qt.CheckStateRole:
            row = index.row()
            self._selection[row] = value == QtCore.Qt.Checked

            self.dataChanged.emit(index, index)
            return True

        return super().setData(index, value, role=role)

    def _add_material(self, material):
        if not super()._add_material(material):
            return False
        self._selection.append(False)
        return True

    def removeMaterial(self, material):
        try:
            row = self._materials.index(material)
        except IndexError:
            return False

        if not super().removeMaterial(material):
            return False

        self._selection.pop(row)
        return True

    def clearMaterials(self):
        self._selection.clear()
        super().clearMaterials()

    def setMaterials(self, materials):
        selected_materials = self.selectedMaterials()

        super().setMaterials(materials)

        self.setSelectedMaterials(selected_materials)

    def selectedMaterials(self):
        return tuple(m for m, s in zip(self._materials, self._selection) if s)

    def setSelectedMaterials(self, materials):
        for row in range(len(self._selection)):
            self._selection[row] = False

        for material in materials:
            try:
                row = self._materials.index(material)
            except ValueError:
                continue
            self._selection[row] = True

        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(len(self._materials), 0))

class MaterialListWidget(QtWidgets.QWidget,
                         MaterialAbstractViewMixin,
                         MaterialVacuumMixin,
                         Validable):

    selectionChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Variables
        model = CheckableMaterialModel()

        self._requires_selection = True

        # Widgets
        self.listview = QtWidgets.QListView()
        self.listview.setModel(model)
        self.listview.setStyleSheet(INVALID_BACKGROUND_STYLESHEET)

        # Layouts
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.listview)
        self.setLayout(layout)

        # Signals
        model.dataChanged.connect(self._on_data_changed)
        model.modelReset.connect(self._on_data_changed)

    def _on_data_changed(self, *args):
        if self.isValid() or not self.isEnabled():
            self.listview.setStyleSheet(VALID_BACKGROUND_STYLESHEET)
        else:
            self.listview.setStyleSheet(INVALID_BACKGROUND_STYLESHEET)

        self.selectionChanged.emit()

    def _get_model(self):
        return self.listview.model()

    def isValid(self):
        if not super().isValid():
            return False

        if not self._requires_selection:
            return True

        return bool(self.selectedMaterials())

    def selectedMaterials(self):
        return self._get_model().selectedMaterials()

    def setSelectedMaterials(self, materials):
        self._get_model().setSelectedMaterials(materials)

    def requiresSelection(self):
        return self._requires_selection

    def setRequiresSelection(self, answer):
        self._requires_selection = answer
        self._on_data_changed()

def run(): #pragma: no cover
    import sys
    app = QtWidgets.QApplication(sys.argv)

    widget = MaterialsWidget()

    mainwindow = QtWidgets.QMainWindow()
    mainwindow.setCentralWidget(widget)
    mainwindow.show()

    app.exec_()

def run2(): #pragma: no cover
    import sys
    app = QtWidgets.QApplication(sys.argv)

    material = Material.pure(14)

    widget = MaterialComboBox()
    widget.addMaterial(material)
    widget.addMaterial(Material.pure(14))
    widget.addMaterial(Material.pure(13))
    widget.addMaterial(Material.pure(10))
    widget.setAllowVacuum(False)
    widget.setCurrentMaterial(material)

    mainwindow = QtWidgets.QMainWindow()
    mainwindow.setCentralWidget(widget)
    mainwindow.show()

    app.exec_()

def run3(): #pragma: no cover
    import sys
    app = QtWidgets.QApplication(sys.argv)

    material = Material.pure(14)

    widget = MaterialListWidget()
    widget.addMaterial(material)
    widget.addMaterial(Material.pure(14))
    widget.addMaterial(Material.pure(13))
    widget.addMaterial(Material.pure(10))
    widget.setAllowVacuum(True)
    widget.setSelectedMaterials([material])

    mainwindow = QtWidgets.QMainWindow()
    mainwindow.setCentralWidget(widget)
    mainwindow.show()

    app.exec_()

if __name__ == '__main__': #pragma: no cover
    run()
