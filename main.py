"""Generate the AI_Text_Ranking_2x2x2 Qualtrics survey as a QSF JSON file.

The script builds a deterministic Qualtrics structure with:
- Two Rank Order questions per respondent (News and Fiction), counterbalanced via eight forms.
- Embedded data for FORM, SET_ORDER, A_ORDER, and B_ORDER.
- Optional quotas limiting each form to two completes.

Run this file directly with Python 3 to create AI_Text_Ranking_2x2x2.qsf in the
current directory.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

SURVEY_ID = "SV_AI_Text_Ranking_2x2x2"
SURVEY_NAME = "AI_Text_Ranking_2x2x2"
OUTPUT_FILE = Path("AI_Text_Ranking_2x2x2.qsf")

# -----------------------------------------------------------------------------
# Text placeholders: paste final stimuli here before distributing the survey.
# Each string currently contains a human-readable placeholder.
# -----------------------------------------------------------------------------
news_gpt5_50 = (
    "The city council passed a late-night noise ordinance after months of complaints "
    "from residents near the riverfront entertainment district. The new regulation "
    "aims to reduce noise levels during late hours, particularly on weekends, in "
    "response to concerns about disturbances affecting nearby neighborhoods. "
    "Enforcement will begin next month."
)
news_gpt5_150 = (
    "After months of complaints from residents, the City Council passed a new "
    "late-night noise ordinance aimed at reducing disturbances near the riverfront "
    "entertainment district. The decision came late Thursday evening following a "
    "public hearing where numerous residents voiced concerns about loud music, "
    "amplified sounds, and late-night events disturbing the neighborhood. The "
    "ordinance imposes stricter noise limits during late-night hours, particularly "
    "for venues hosting live music and large gatherings. Council members debated the "
    "balance between supporting local businesses and addressing residents' quality "
    "of life, ultimately voting in favor of the measure with a majority. The new "
    "rules will require businesses to monitor sound levels more closely and "
    "implement noise reduction strategies, such as soundproofing or limiting "
    "outdoor events. City officials emphasized that enforcement will begin with "
    "warnings and gradually increase penalties for repeated violations. Local "
    "business owners have expressed mixed reactions, with some concerned about the "
    "impact on their operations."
)
news_gemini_50 = (
    "City Council passed a new late-night noise ordinance Tuesday, addressing months "
    "of escalating resident complaints about excessive sound near the riverfront "
    "entertainment district. The measure restricts amplified noise after 11 PM on "
    "weekdays and midnight on weekends. Supporters hope the change will restore "
    "peace while critics worry about the impact on local businesses."
)
news_gemini_150 = (
    "After months of mounting resident complaints, the City Council voted 6-1 early "
    "Thursday morning to approve a new late-night noise ordinance targeting the "
    "burgeoning riverfront entertainment district. The measure establishes a strict "
    "11 p.m. cutoff for outdoor amplified sound on weekdays and midnight on weekends "
    "for all venues within a three-block radius of the Riverwalk. Councilmember Sarah "
    "Chen, who introduced the ordinance, cited over 200 formal noise complaints "
    "lodged by nearby apartment and condo residents since the beginning of the year, "
    "stating the new rules were necessary to balance economic vitality with "
    "residential quality-of-life. Business owners in the area, who attended the "
    "lengthy session, expressed concerns that the earlier cutoff times could severely "
    "impact their summer revenue. Enforcement of the new regulation, which carries a "
    "$500 fine for first-time offenders, will begin on June 1. The city's Police "
    "Department will handle the implementation and initial 90-day review of the "
    "ordinance’s impact."
)
fiction_gpt5_50 = (
    "The rain arrived in a furious blur, soaking him before he could reach the train. "
    "Wet fingers fumbled through his pockets—empty. The key, gone. He stood at the "
    "curb, breath tight in his chest, then spotted a torn cardboard box. A shivering "
    "compromise. He slid it under his shirt."
)
fiction_gpt5_150 = (
    "The rain arrived like a curtain dropping, sudden and cold, drenching the streets "
    "in seconds. Martin stood under the small awning of a corner shop, the key to his "
    "apartment nowhere in his pockets. He had slipped it into his jacket "
    "earlier—hadn’t he? Now, only loose change and a crumpled receipt. The water "
    "pooled at his shoes, the weight of the moment pressing as much as the weight of "
    "the downpour. His eyes darted across the street, but the flashing light of a bus "
    "passing by reminded him that he couldn’t go home just yet. He turned, eyes "
    "scanning for something—anything—that might get him inside. A forgotten cardboard "
    "box leaned against the lamppost, and he wrenched it open, finding nothing but "
    "old newspapers. In desperation, he stuffed his hands into a damp alley’s trash "
    "bin, hoping the key had somehow slipped out, only to feel the slick, sharp edge "
    "of a broken bottle instead."
)
fiction_gemini_50 = (
    "The sky split with a sudden, silver deluge. He clutched his leather briefcase, "
    "realizing the brass key, usually clipped to the lining, was gone. Water "
    "immediately soaked his thin linen jacket. A chill set in. He assessed the "
    "five-block distance, calculating if the rusted fire-escape stairs were less "
    "risky than hailing a desperate cab."
)
fiction_gemini_150 = (
    "The evening train screeched to a wet halt, and the skies opened instantly, "
    "dropping sheets of cold, silver rain onto the platform. He yanked his umbrella "
    "open, the cheap plastic momentarily sticking, and hurried toward the street, "
    "picturing the warm, dry air of his apartment. It was only when he reached the "
    "porch light, the water already soaking his trouser cuffs, that his fingers "
    "brushed the empty coin pocket. Panic tightened his chest; the spare key, "
    "usually nested beside three old pennies, was gone. The downpour intensified, "
    "blurring the streetlights into golden smears. Shivering, he glanced at the "
    "narrow, locked window of his kitchen, the pane always a little loose on its "
    "track. He retrieved a forgotten library card from his wallet, its worn edge thin "
    "as paper, and decided on a vertical climb up the slick, moss-covered drainpipe "
    "to the second floor, improvising a desperate, dark route into the dry quiet "
    "inside."
)

NEWS_CHOICES = [
    ("news_gpt5_50", news_gpt5_50, 11),
    ("news_gpt5_150", news_gpt5_150, 12),
    ("news_gemini_50", news_gemini_50, 13),
    ("news_gemini_150", news_gemini_150, 14),
]

FICTION_CHOICES = [
    ("fiction_gpt5_50", fiction_gpt5_50, 21),
    ("fiction_gpt5_150", fiction_gpt5_150, 22),
    ("fiction_gemini_50", fiction_gemini_50, 23),
    ("fiction_gemini_150", fiction_gemini_150, 24),
]

# Latin square orderings (indices correspond to the arrays above, 0-based).
NEWS_ORDERS = [
    [0, 1, 2, 3],
    [1, 2, 3, 0],
    [2, 3, 0, 1],
    [3, 0, 1, 2],
]

FICTION_ORDERS = [
    [0, 2, 1, 3],
    [2, 1, 3, 0],
    [1, 3, 0, 2],
    [3, 0, 2, 1],
]

# -----------------------------------------------------------------------------
# Helper builders
# -----------------------------------------------------------------------------

def make_choice(display: str, variable_name: str, recode: int) -> Dict[str, str]:
    """Create a Qualtrics choice payload."""
    return {
        "Display": display,
        "VariableName": variable_name,
        "Recode": str(recode),
    }


def make_rank_question(
    qid: str, prompt: str, ordered_indices: List[int], base_choices: List[Tuple[str, str, int]]
) -> Dict:
    """Create a Rank Order question element with fixed ordering and recodes."""
    choices: Dict[str, Dict[str, str]] = {}
    recodes: Dict[str, str] = {}

    # Build choices in the exact order requested (positions 1-4).
    for position, base_index in enumerate(ordered_indices, start=1):
        var_name, display, recode_value = base_choices[base_index]
        choices[str(position)] = make_choice(display, var_name, recode_value)
        recodes[str(position)] = str(recode_value)

    return {
        "SurveyID": SURVEY_ID,
        "Element": "SQ",
        "PrimaryAttribute": qid,
        "SecondaryAttribute": prompt,
        "TertiaryAttribute": "1",
        "Payload": {
            "QuestionText": prompt,
            "DefaultChoices": False,
            "DataExportTag": qid,
            "QuestionType": "RO",
            "Selector": "RO",
            "SubSelector": "DRAG_AND_DROP",
            "Configuration": {"QuestionDescriptionOption": "UseText"},
            "Validation": {
                "Settings": {
                    "ForceResponse": "OFF",
                    "Type": "",
                    "RO": {"Type": "NoTie", "ForceRank": "ON"},
                }
            },
            "GradingData": [],
            "Language": [],
            "NextChoiceId": 5,
            "NextAnswerId": 1,
            "Choices": choices,
            "ChoiceOrder": list(range(1, len(ordered_indices) + 1)),
            "Randomization": {
                "Advanced": {
                    "FixedOrder": list(range(1, len(ordered_indices) + 1)),
                    "Randomize": False,
                }
            },
            "RecodeValues": recodes,
            "RecodeValuesEnabled": True,
            "QuestionID": qid,
            "DataVisibility": {"Private": False, "Hidden": False},
        },
    }


def make_block(block_id: str, question_id: str, description: str) -> Dict:
    """Wrap a single question in a block element."""
    return {
        "SurveyID": SURVEY_ID,
        "Element": "BL",
        "PrimaryAttribute": block_id,
        "SecondaryAttribute": description,
        "TertiaryAttribute": None,
        "Payload": {
            "Type": "Standard",
            "SubType": "",
            "Description": description,
            "ID": block_id,
            "BlockElements": [
                {"Type": "Question", "QuestionID": question_id, "Description": description}
            ],
        },
    }


def make_embedded_data(form: int, set_order: str, a_order: int, b_order: int) -> Dict:
    """Create the embedded data flow element holding form metadata."""
    return {
        "Type": "EmbeddedData",
        "FlowID": f"FL_ED_{form}",
        "EmbeddedData": [
            {"Field": "FORM", "Type": "Custom", "Value": str(form)},
            {"Field": "SET_ORDER", "Type": "Custom", "Value": set_order},
            {"Field": "A_ORDER", "Type": "Custom", "Value": str(a_order)},
            {"Field": "B_ORDER", "Type": "Custom", "Value": str(b_order)},
        ],
    }


def make_group_flow(form: int, set_order: str, first_block: str, second_block: str, a_order: int, b_order: int) -> Dict:
    """Build a group flow entry for a single form."""
    return {
        "Type": "Group",
        "FlowID": f"FL_FORM_{form}",
        "Description": f"Form F{form}",
        "Flow": [
            make_embedded_data(form, set_order, a_order, b_order),
            {"Type": "Block", "FlowID": f"FL_FORM_{form}_1", "ID": first_block},
            {"Type": "Block", "FlowID": f"FL_FORM_{form}_2", "ID": second_block},
        ],
    }


def build_flow() -> Dict:
    """Assemble the full survey flow with random assignment to forms."""
    groups = []

    # A->B forms (F1-F4)
    for form_index, order_index in enumerate(range(4), start=1):
        groups.append(
            make_group_flow(
                form=form_index,
                set_order="A-B",
                first_block=f"BL_A{order_index + 1}",
                second_block=f"BL_B{order_index + 1}",
                a_order=order_index + 1,
                b_order=order_index + 1,
            )
        )

    # B->A forms (F5-F8)
    for form_index, order_index in zip(range(5, 9), range(4)):
        groups.append(
            make_group_flow(
                form=form_index,
                set_order="B-A",
                first_block=f"BL_B{order_index + 1}",
                second_block=f"BL_A{order_index + 1}",
                a_order=order_index + 1,
                b_order=order_index + 1,
            )
        )

    return {
        "SurveyID": SURVEY_ID,
        "Element": "FL",
        "PrimaryAttribute": "FL_ROOT",
        "SecondaryAttribute": "Survey Flow",
        "Payload": {
            "Type": "Root",
            "FlowID": "FL_ROOT",
            "Flow": [
                {
                    "Type": "Randomizer",
                    "FlowID": "FL_RANDOMIZER",
                    "EvenPresentation": 1,
                    "Flow": groups,
                    "SubSet": len(groups),
                }
            ],
            "Properties": {"Count": 1},
        },
    }


def build_survey_options() -> Dict:
    """Provide minimal survey options payload."""
    return {
        "SurveyID": SURVEY_ID,
        "Element": "OP",
        "PrimaryAttribute": "Survey Options",
        "SecondaryAttribute": None,
        "Payload": {
            "BackButton": "false",
            "SaveAndContinue": "true",
            "SurveyProtection": "Public",
            "BallotBoxStuffingPrevention": "false",
            "SurveyExpiration": None,
            "SurveyLanguage": "EN",
            "SurveyName": SURVEY_NAME,
        },
    }


def build_quota(form: int) -> Dict:
    """Create an optional quota restricting completes per form."""
    quota_id = f"Quota_FORM_{form}"
    return {
        "Description": f"FORM {form}",
        "QuotaID": quota_id,
        "Logic": [
            {
                "LogicType": "EmbeddedData",
                "Field": "FORM",
                "Operator": "EqualTo",
                "Value": str(form),
            }
        ],
        "QuotaAction": "EndSurvey",
        "Count": 2,
        "Occurrences": "Once",
        "QuotaLogicType": "Simple",
        "DisplayLogic": [],
        "Exceeded": {
            "LogicType": "Action",
            "Action": "EndSurvey",
            "MessageLibraryID": None,
            "MessageID": "MS_Closed",
        },
    }


def build_quotas() -> Dict:
    """Assemble the quota element (optional)."""
    return {
        "SurveyID": SURVEY_ID,
        "Element": "QT",
        "PrimaryAttribute": "Quotas",
        "SecondaryAttribute": None,
        "Payload": {
            "Quotas": [build_quota(form) for form in range(1, 9)],
            "OnBlockedMessage": "MS_Closed",
        },
    }


def build_survey_entry() -> Dict:
    """Provide the top-level SurveyEntry metadata."""
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "SurveyID": SURVEY_ID,
        "SurveyName": SURVEY_NAME,
        "SurveyOwnerID": "UR_AI",
        "SurveyBrandID": "AI",
        "DivisionID": None,
        "SurveyVersion": "1",
        "SurveyActiveResponseSet": "RS_1",
        "SurveyStatus": "Active",
        "SurveyStartDate": now,
        "SurveyCreationDate": now,
        "CreatorID": "UR_AI",
        "LastModified": now,
    }


def build_question_block_elements() -> Tuple[List[Dict], List[Dict]]:
    """Create all questions and blocks for News (A) and Fiction (B)."""
    questions: List[Dict] = []
    blocks: List[Dict] = []

    # News blocks/questions (A1-A4)
    for index, order in enumerate(NEWS_ORDERS, start=1):
        qid = f"QID_A{index}"
        block_id = f"BL_A{index}"
        prompt = "Rank the 4 News texts by human-likeness (1 = most human-like … 4 = least). No ties."
        questions.append(make_rank_question(qid, prompt, order, NEWS_CHOICES))
        blocks.append(make_block(block_id, qid, f"News Order {index}"))

    # Fiction blocks/questions (B1-B4)
    for index, order in enumerate(FICTION_ORDERS, start=1):
        qid = f"QID_B{index}"
        block_id = f"BL_B{index}"
        prompt = "Rank the 4 Fiction texts by human-likeness (1 = most human-like … 4 = least). No ties."
        questions.append(make_rank_question(qid, prompt, order, FICTION_CHOICES))
        blocks.append(make_block(block_id, qid, f"Fiction Order {index}"))

    return questions, blocks


def build_survey() -> Dict:
    """Construct the full QSF payload."""
    questions, blocks = build_question_block_elements()

    survey_elements: List[Dict] = []
    survey_elements.extend(blocks)
    survey_elements.extend(questions)
    survey_elements.append(build_flow())
    survey_elements.append(build_survey_options())
    survey_elements.append(build_quotas())

    return {
        "SurveyEntry": build_survey_entry(),
        "SurveyElements": survey_elements,
    }


def main() -> None:
    payload = build_survey()
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Wrote {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
