from django.apps import apps as django_apps
from edc_metadata_rules import PredicateCollection
from edc_constants.constants import YES
from edc_reference.models import Reference


class Predicates(PredicateCollection):
    
    app_label = 'potlako_subject'
    visit_model = f'{app_label}.subjectvisit'
    
    def func_transport_support_required(self, visit=None, **kwargs):
        """return True if participant on Intervention arm and 
        transport_required==YES"""
        onschedule_cls = django_apps.get_model('potlako_subject.onschedule')
        
        try:
            onschedule_obj = onschedule_cls.objects.get(
                subject_identifier=visit.appointment.subject_identifier)
        except onschedule_cls.DoesNotExist:
            return False
        else:
            if visit.visit_code ==  '1000' and visit.visit_code_sequence ==  0:
                transport_support = self.exists(
                reference_name=f'{self.app_label}.patientcallinitial',
                subject_identifier=visit.subject_identifier,
                field_name='transport_support',
                timepoint=visit.visit_code)[0]
            else:
                patient_fu = Reference.objects.filter(
                model=f'{self.app_label}.patientcallfollowup',
                identifier=visit.appointment.subject_identifier,
                report_datetime__gt=visit.report_datetime,
                timepoint=visit.visit_code).order_by(
                '-report_datetime').first()
                
                transport_support = patient_fu.transport_support if patient_fu else None
                    
            
            return onschedule_obj.community_arm == 'Intervention' and transport_support == YES
        
        
    def func_home_visit_required(self, visit=None, **kwargs):
        """return True if 3 missed call records exist for a 
        particular visit"""
        missed_call_cls = django_apps.get_model('potlako_subject.missedcallrecord')
        
        missed_call_records = missed_call_cls.objects.filter(
            missed_call__subject_visit=visit)
                    
        return missed_call_records.count() == 3
