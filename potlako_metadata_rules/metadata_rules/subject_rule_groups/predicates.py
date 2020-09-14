from django.apps import apps as django_apps
from edc_metadata_rules import PredicateCollection
from edc_constants.constants import YES

class Predicates(PredicateCollection):
    
    app_label = 'potlako_subject'
    visit_model = f'{app_label}.subjectvisit'
    
    def func_intervention_arm(self, visit=None, **kwargs):
        """return True if participant on Intervention arm and 
        transport_required==YES"""
        onschedule_cls = django_apps.get_model('potlako_subject.onschedule')
        
        try:
            onschedule_obj = onschedule_cls.objects.get(
                subject_identifier=visit.appointment.subject_identifier)
        except onschedule_cls.DoesNotExist:
            return False
        else:
            if visit.visit_code ==  '1000':
                values = self.exists(
                reference_name=f'{self.app_label}.patientcallinitial',
                subject_identifier=visit.subject_identifier,
                field_name='transport_support')
            else:
                values = self.exists(
                reference_name=f'{self.app_label}.patientcallfollowup',
                subject_identifier=visit.subject_identifier,
                field_name='transport_support')
            
            return onschedule_obj.community_arm == 'Intervention' and values[0] == YES