from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from .predicates import Predicates

app_label = 'potlako_subject'
pc = Predicates()


@register()
class MissedCallRuleGroup(CrfRuleGroup):

    home_visit = CrfRule(
        predicate=pc.func_home_visit_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.homevisit'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.missedcall'
