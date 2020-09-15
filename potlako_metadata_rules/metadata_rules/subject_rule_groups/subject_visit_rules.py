from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, P, register
from .predicates import Predicates

app_label = 'potlako_subject'
pc = Predicates()

@register()
class SubjectVisitRuleGroup(CrfRuleGroup):

    missed_visit = CrfRule(
        predicate=P('reason', 'eq', 'missed_quarterly_visit'),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.missedvisit'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.subjectvisit'
