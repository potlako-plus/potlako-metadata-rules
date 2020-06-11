from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, P, register

app_label = 'potlako_subject'


@register()
class ClinicianCallFollowUpRuleGroup(CrfRuleGroup):

    transport = CrfRule(
        predicate=P('transport_support', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.transport'])

    investigations = CrfRule(
        predicate=P('investigation_ordered', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.investigations'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.cliniciancallfollowup'
