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
            values = self.exists(
            reference_name=f'{self.app_label}.patientcallinitial',
            subject_identifier=visit.subject_identifier,
            field_name='transport_support')
            
            return onschedule_obj.community_arm == 'Intervention' and values[0] == YES
    
    def func_home_visit_required(self, visit=None, **kwargs):
        """return True if 3 missed visit forms have been completed for
        a given visit"""
        
        values = self.exists(
            reference_name=f'{self.app_label}.missedvisit',
            subject_identifier=visit.subject_identifier,
            field_name='report_datetime')
        
        return len(values) == 3
    
    def func_missed_visit_required(self, visit=None, **kwargs):
        """return True if 3 missed visit forms have been completed for
        a given visit"""
        
        values = self.exists(
            reference_name=f'{self.app_label}.missedvisit',
            subject_identifier=visit.subject_identifier,
            field_name='report_datetime')
        
        return visit.reason == 'missed_quarterly_visit' #and len(values) < 3
