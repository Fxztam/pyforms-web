from pyforms_web.web.basewidget                         import BaseWidget
from pyforms_web.web.controls.ControlTextArea           import ControlTextArea
from pyforms_web.web.controls.ControlText               import ControlText
from pyforms_web.web.controls.ControlInteger            import ControlInteger
from pyforms_web.web.controls.ControlFloat              import ControlFloat
from pyforms_web.web.controls.ControlCombo              import ControlCombo
from pyforms_web.web.controls.ControlDate               import ControlDate
from pyforms_web.web.controls.ControlDateTime           import ControlDateTime
from pyforms_web.web.controls.ControlButton             import ControlButton
from pyforms_web.web.controls.ControlQueryList          import ControlQueryList
from pyforms_web.web.controls.ControlMultipleSelection  import ControlMultipleSelection
from pyforms_web.web.controls.ControlEmptyWidget        import ControlEmptyWidget
from pyforms_web.web.controls.ControlFileUpload         import ControlFileUpload
from pyforms_web.web.controls.ControlCheckBox           import ControlCheckBox
from pyforms_web.web.controls.ControlLabel          import ControlLabel

from django.core.exceptions import ValidationError, FieldDoesNotExist
from pyforms_web.web.django_pyforms.model_admin.utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os


class ViewFormAdmin(BaseWidget):

    MODEL     = None  #model to manage
    TITLE     = None  #application title
    INLINES   = []    #sub models to show in the interface
    FIELDSETS = None  #formset of the edit form
    
    def __init__(self, *args, **kwargs):
        """
        Parameters:
            title  - Title of the app.
            model  - Model with the App will represent.
            parent - Variable with the content [model, foreign key id]. It is used to transform the App in an inline App
        """
        BaseWidget.__init__(self, kwargs.get('title', self.TITLE))
        self.model = kwargs.get('model',         self.MODEL)
        self.inlines = kwargs.get('inlines',     self.INLINES)
        self.fieldsets = kwargs.get('fieldsets', self.FIELDSETS)

        # used to configure the interface to inline
        # it will filter the dataset by the foreign key
        self.parent_field = None
        self.parent_pk    = kwargs.get('parent_pk', None)
        self.parent_model = kwargs.get('parent_model', None)
        if self.parent_model and self.parent_pk:
            self.set_parent(self.parent_model, self.parent_pk)
        #######################################################

        self.edit_fields = []
        self.object_pk   = None
        
        self.create_model_formfields()
        pk = kwargs.get('pk', None)
        if pk:
            self.object_pk = pk
            self.show_form()

    #################################################################################
    #################################################################################



    #################################################################################
    #################################################################################
    
    def create_model_formfields(self):
        """
            Create the model edition form
        """     
        fields2show = self.get_visible_fields_names()       
        formset     = []

        for field in self.model._meta.get_fields():
            if field.name not in fields2show: continue #only create this field if is visible
            pyforms_field = None

            if   isinstance(field, models.AutoField): continue
            elif isinstance(field, models.Field) and field.choices:
                pyforms_field = ControlCombo( 
                    field.verbose_name.capitalize(), 
                    items=[ (c[1],c[0]) for c in field.choices]
                )
            elif isinstance(field, models.BigAutoField):                pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.BigIntegerField):             pyforms_field = ControlInteger( field.verbose_name )
            elif isinstance(field, models.BinaryField):                 pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.BooleanField):                pyforms_field = ControlCheckBox( field.verbose_name )
            elif isinstance(field, models.CharField):                   pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.CommaSeparatedIntegerField):  pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.DateTimeField):               pyforms_field = ControlDateTime( field.verbose_name )
            elif isinstance(field, models.DateField):                   pyforms_field = ControlDate( field.verbose_name )
            elif isinstance(field, models.DecimalField):                pyforms_field = ControlFloat( field.verbose_name )
            elif isinstance(field, models.DurationField):               pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.EmailField):                  pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.FileField):                   pyforms_field = ControlFileUpload( field.verbose_name )
            elif isinstance(field, models.FilePathField):               pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.FloatField):                  pyforms_field = ControlFloat( field.verbose_name )
            elif isinstance(field, models.ImageField):                  pyforms_field = ControlFileUpload( field.verbose_name )
            elif isinstance(field, models.IntegerField):                pyforms_field = ControlInteger( field.verbose_name )
            elif isinstance(field, models.GenericIPAddressField):       pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.NullBooleanField):            
                pyforms_field = ControlCombo( 
                    field.verbose_name.capitalize(), 
                    items=[('Unknown', None), ('Yes', True), ('No', False)]
                )
            elif isinstance(field, models.PositiveIntegerField):        pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.PositiveSmallIntegerField):   pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.SlugField):                   pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.SmallIntegerField):           pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.TextField):                   pyforms_field = ControlLabel( field.verbose_name )
            elif isinstance(field, models.TimeField):                   pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.URLField):                    pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.UUIDField):                   pyforms_field = ControlText( field.verbose_name )
            elif isinstance(field, models.ForeignKey):  
                #Foreign key
                pyforms_field = ControlCombo( field.verbose_name )
                for instance in field.related_model.objects.all(): pyforms_field.add_item( str(instance), instance.pk )         
            elif isinstance(field, models.ManyToManyField):
                #Many to Many field
                pyforms_field = ControlMultipleSelection( field.verbose_name )
                for instance in field.related_model.objects.all():
                    pyforms_field.add_item( str(instance), instance.pk )

            if pyforms_field is not None: 
                setattr(self, field.name, pyforms_field)
                formset.append(field.name)
                self.edit_fields.append( pyforms_field )

        #Create the inlines eition forms.
        self.inlines_controls_name  = []
        self.inlines_controls       = []
        for inline in self.inlines:
            pyforms_field = ControlEmptyWidget()
            setattr(self, inline.__name__, pyforms_field)
            self.inlines_controls_name.append(inline.__name__)
            self.inlines_controls.append( pyforms_field )
            formset.append(inline.__name__)
            
        self.formset = self.fieldsets if self.fieldsets else formset


    def hide_form(self):
        for field in self.edit_fields:      field.hide()
        for field in self.inlines_controls: field.hide()
    
    def show_form(self):
        for field in self.edit_fields:      field.show()
        for field in self.inlines_controls: field.show()
        
        obj = self.model.objects.get(pk=self.object_pk)
        fields2show = self.get_visible_fields_names()
        for field in self.model._meta.get_fields():
            if field.name not in fields2show: continue

            if isinstance(field, models.AutoField):                 continue
            elif isinstance(field, models.BigAutoField):            continue
            elif isinstance(field, models.BigIntegerField):         getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.BinaryField):             getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.BooleanField):            getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.CharField):               getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.CommaSeparatedIntegerField):getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.DateField):               getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.DateTimeField):           getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.DecimalField):            getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.DurationField):           getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.EmailField):              getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.FileField):               getattr(self, field.name).value = getattr(obj, field.name).url if getattr(obj, field.name) else None
            elif isinstance(field, models.FilePathField):           getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.FloatField):              getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.ImageField):              getattr(self, field.name).value = getattr(obj, field.name).url if getattr(obj, field.name) else None
            elif isinstance(field, models.IntegerField):            getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.GenericIPAddressField):   getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.NullBooleanField):        getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.PositiveIntegerField):    getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.PositiveSmallIntegerField): getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.SlugField):               getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.SmallIntegerField):       getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.TextField):               getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.TimeField):               getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.URLField):                getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.UUIDField):               getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.ForeignKey):
                v = getattr(obj, field.name)
                getattr(self, field.name).value = str(v.pk) if v else None
            elif isinstance(field, models.ManyToManyField):                 
                getattr(self, field.name).value = [str(o.pk) for o in getattr(obj, field.name).all()]
            
            getattr(self, field.name).enabled = False

        for inline in self.inlines:
            getattr(self, inline.__name__).value = inline( (self.model, self.object_pk) )



    def set_parent(self, parent_model, parent_pk):
        self.parent_pk      = parent_pk
        self.parent_model   = parent_model

        for field in self.model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                if parent_model == field.related_model:
                    self.parent_field = field
                    break


    def get_visible_fields_names(self):
        #return the names of the visible fields
        fields = get_fieldsets_strings(self.fieldsets) if self.fieldsets else [field.name for field in self.model._meta.get_fields()]
        if self.parent_field: fields.remove(self.parent_field.name)
        return fields


