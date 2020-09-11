from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, P, register
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
        predicate=P('investigations_ordered', 'eq', 'ordered'),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.investigationsordered'])

    investigations_resulted = CrfRule(
        predicate=P('investigations_ordered', 'eq', 'ordered_and_resulted'),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.investigationsresulted'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.patientcallfollowup'
