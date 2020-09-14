from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, P, PF, register
from .predicates import Predicates

app_label = 'potlako_subject'
pc = Predicates()


@register()
class PatientCallInitialRuleGroup(CrfRuleGroup):
    

    transport = CrfRule(
        predicate=pc.func_intervention_arm,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.transport'])

    medical_conditions = CrfRule(
        predicate=P('medical_conditions', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.medicaldiagnosis'])

    tests_ordered = CrfRule(
        predicate=PF(
            'tests_ordered',
            func=lambda tests_ordered: True if tests_ordered in ['ordered', 'ordered_and_resulted'] else False),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.investigationsordered'])
    
    investigations_resulted = CrfRule(
        predicate=P('tests_ordered', 'eq', 'ordered_and_resulted'),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.investigationsresulted'])


    class Meta:
        app_label = app_label
        source_model = f'{app_label}.patientcallinitial'
