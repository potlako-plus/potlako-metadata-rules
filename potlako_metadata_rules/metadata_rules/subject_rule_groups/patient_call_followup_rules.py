from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, PF, register
from .predicates import Predicates

app_label = 'potlako_subject'
pc = Predicates()


@register()
class PatientCallFollowUpRuleGroup(CrfRuleGroup):

    transport = CrfRule(
        predicate=pc.func_intervention_arm,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.transport'])

    investigations_ordered = CrfRule(
        predicate= PF(
            'investigations_ordered',
            func=lambda investigations_ordered: True if investigations_ordered in ['ordered', 'ordered_and_resulted'] else False),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.investigationsordered'])

    investigations_resulted = CrfRule(
        predicate=PF(
            'investigations_ordered', 
            func=lambda investigations_ordered: True if investigations_ordered in ['resulted', 'ordered_and_resulted'] else False),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.investigationsresulted'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.patientcallfollowup'
