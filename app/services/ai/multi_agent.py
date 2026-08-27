from pathlib import Path

from app.services.ai.receptionist import route_patient
from app.services.ai.gp_disease import predict_gp_case
from app.services.ai.icu_cdss import analyze_icu_vitals
from app.services.ai.radiologist import analyze_xray
from app.services.ai.patient_education import answer_patient_question
from app.services.ai.pharmacist import analyze_medication_safety
from app.services.ai.mental_health import analyze_mental_health
from app.services.ai.clinical_reasoning import reason_from_symptoms
from app.services.ai.emergency_bfs import bfs_emergency_reasoning
from app.services.ai.oncology_dfs import dfs_oncology_reasoning
from app.services.ai.treatment_rl import optimize_treatment


ROOT = Path(__file__).resolve().parents[3]

DEMO_XRAY = (
    ROOT
    / "data"
    / "week4_demo"
    / "pneumonia.png"
)


SYSTEM_NAME = (
    "iHIS Relevance-Selective "
    "Multi-Agent Clinical Orchestrator"
)

SYSTEM_VERSION = "2.0"


ALL_SPECIALISTS = [
    "Receptionist AI",
    "GP AI",
    "ICU AI",
    "Radiologist AI",
    "Clinical Reasoning AI",
    "Emergency AI",
    "Clinical Pharmacist AI",
    "Psychiatrist AI",
    "Oncologist AI",
    "Treatment Planning AI",
    "Patient Education AI",
]


SCENARIOS = {
    "respiratory": {
        "label": (
            "Synthetic respiratory presentation"
        ),

        "intake_text": (
            "Fever, productive cough, fatigue "
            "and shortness of breath"
        ),

        "duration": "3 days",

        "gp_input": {
            "age": 55,
            "temperature": 38.8,
            "heart_rate": 108,
            "cough": True,
            "sputum": True,
            "dyspnea": True,
            "dysuria": False,
            "urinary_frequency": False,
            "abdominal_pain": False,
            "diarrhea": False,
            "vomiting": False,
            "smoking": True,
        },

        "xray": True,

        "reasoning_symptoms": {
            "fever": True,
            "cough": True,
            "sputum": True,
            "dyspnea": True,
            "chest_pain": False,
            "sore_throat": False,
            "nasal_symptoms": False,
            "fatigue": True,
            "dysuria": False,
            "urinary_frequency": False,
            "lower_abdominal_pain": False,
            "abdominal_pain": False,
            "diarrhea": False,
            "vomiting": False,
            "nausea": False,
            "sweating": False,
            "wheeze": False,
            "chest_tightness": False,
        },

        "pharmacy": {
            "condition": (
                "Suspected bacterial respiratory infection"
            ),
            "current_medications": "paracetamol",
            "allergies": "",
            "renal_impairment": False,
        },

        "education_question": (
            "What should a patient know about pneumonia?"
        ),
    },


    "emergency": {
        "label": (
            "Synthetic emergency neurological presentation"
        ),

        "intake_text": (
            "Sudden one-sided weakness "
            "and slurred speech"
        ),

        "duration": "Today",

        "critical_monitoring": True,

        "vitals": {
            "temperature": 37.0,
            "heart_rate": 105,
            "respiratory_rate": 20,
            "systolic_bp": 170,
            "oxygen_saturation": 96,
        },

        "emergency_symptoms": {
            "chest_pain": False,
            "dyspnea": False,
            "sweating": False,
            "nausea": False,
            "tachycardia": True,
            "hemoptysis": False,
            "wheeze": False,
            "chest_tightness": False,
            "sudden_weakness": True,
            "speech_difficulty": True,
            "seizure": False,
            "altered_consciousness": False,
            "fever": False,
            "hypotension": False,
            "rash": False,
            "swelling": False,
        },
    },


    "mental_health": {
        "label": (
            "Synthetic mental-health presentation"
        ),

        "intake_text": (
            "Low mood, loss of interest, anxiety "
            "and persistent worrying"
        ),

        "duration": "2 weeks",

        "mental_health": {
            "low_interest": 2,
            "depressed_mood": 2,
            "nervous": 2,
            "unable_to_stop_worrying": 2,
        },
    },


    "oncology": {
        "label": (
            "Synthetic oncology presentation"
        ),

        "intake_text": (
            "Persistent cough, weight loss "
            "and long smoking history"
        ),

        "duration": "2 months",

        "oncology_symptoms": {
            "persistent_cough": True,
            "hemoptysis": False,
            "dyspnea": True,
            "chest_pain": False,
            "weight_loss": True,
            "smoking_history": True,
            "rectal_bleeding": False,
            "change_bowel_habit": False,
            "abdominal_pain": False,
            "anemia": False,
            "urinary_obstruction": False,
            "hematuria": False,
            "bone_pain": False,
            "elevated_psa": False,
        },

        "treatment_state": {
            "disease_extent": "Localized",
            "ecog_status": "0",
        },
    },
}


def select_relevant_agents(case):
    """
    Determine which specialist agents are relevant from
    the structured information available in the case.

    An agent is selected only when its required clinical
    input/context is present.
    """

    selected = [
        "Receptionist AI"
    ]

    reasons = {
        "Receptionist AI": (
            "All patients enter through intake and routing."
        )
    }

    if "gp_input" in case:
        selected.append(
            "GP AI"
        )
        reasons[
            "GP AI"
        ] = (
            "General symptoms and risk factors "
            "are available."
        )

    if (
        case.get(
            "critical_monitoring"
        )
        and "vitals" in case
    ):
        selected.append(
            "ICU AI"
        )
        reasons[
            "ICU AI"
        ] = (
            "The case requires critical vital-sign monitoring."
        )

    if case.get("xray"):
        selected.append(
            "Radiologist AI"
        )
        reasons[
            "Radiologist AI"
        ] = (
            "Imaging data are available."
        )

    if (
        "reasoning_symptoms"
        in case
    ):
        selected.append(
            "Clinical Reasoning AI"
        )
        reasons[
            "Clinical Reasoning AI"
        ] = (
            "A structured symptom set is available "
            "for differential reasoning."
        )

    if (
        "emergency_symptoms"
        in case
    ):
        selected.append(
            "Emergency AI"
        )
        reasons[
            "Emergency AI"
        ] = (
            "Emergency red-flag features are present."
        )

    if "pharmacy" in case:
        selected.append(
            "Clinical Pharmacist AI"
        )
        reasons[
            "Clinical Pharmacist AI"
        ] = (
            "Medication information is available "
            "for safety assessment."
        )

    if (
        "mental_health"
        in case
    ):
        selected.append(
            "Psychiatrist AI"
        )
        reasons[
            "Psychiatrist AI"
        ] = (
            "Mental-health screening responses are available."
        )

    if (
        "oncology_symptoms"
        in case
    ):
        selected.append(
            "Oncologist AI"
        )
        reasons[
            "Oncologist AI"
        ] = (
            "Cancer-related features are present "
            "for DFS pathway reasoning."
        )

    if (
        "oncology_symptoms"
        in case
        and "treatment_state"
        in case
    ):
        selected.append(
            "Treatment Planning AI"
        )
        reasons[
            "Treatment Planning AI"
        ] = (
            "An oncology pathway and structured "
            "treatment state are available."
        )

    if (
        "education_question"
        in case
    ):
        selected.append(
            "Patient Education AI"
        )
        reasons[
            "Patient Education AI"
        ] = (
            "A patient-education question is relevant "
            "to the current case."
        )

    return (
        selected,
        reasons,
    )


def add_agent_card(
    cards,
    name,
    value,
):
    cards.append({
        "name": name,
        "value": value,
    })


def run_integrated_case(
    case_type="respiratory",
    patient_context=None,
):
    """
    Execute only the agents selected as relevant
    to the current structured case.
    """

    if case_type not in SCENARIOS:
        raise ValueError(
            "Unsupported multi-agent scenario."
        )

    case = SCENARIOS[
        case_type
    ]

    patient_context = (
        patient_context
        or {}
    )

    (
        selected_agents,
        selection_reasons,
    ) = select_relevant_agents(
        case
    )

    skipped_agents = [
        agent
        for agent in ALL_SPECIALISTS
        if agent
        not in selected_agents
    ]

    outputs = {}
    cards = []
    communication_log = []
    integrated_summary = []


    for agent in selected_agents:
        communication_log.append(
            (
                f"Orchestrator -> {agent}: "
                f"{selection_reasons[agent]}"
            )
        )


    if (
        "Receptionist AI"
        in selected_agents
    ):
        receptionist = route_patient(
            case["intake_text"],
            case["duration"],
        )

        outputs[
            "receptionist"
        ] = receptionist

        value = (
            f"{receptionist['recommended_service']} "
            f"({receptionist['urgency']})"
        )

        add_agent_card(
            cards,
            "Receptionist AI",
            value,
        )

        integrated_summary.append(
            (
                "Receptionist routing: "
                f"{value}."
            )
        )


    if (
        "GP AI"
        in selected_agents
    ):
        gp = predict_gp_case(
            case["gp_input"]
        )

        outputs[
            "gp"
        ] = gp

        value = (
            f"{gp['predicted_condition']} "
            f"({gp['confidence'] * 100:.1f}%)"
        )

        add_agent_card(
            cards,
            "GP AI",
            value,
        )

        integrated_summary.append(
            (
                "GP prediction: "
                f"{value}."
            )
        )


    if (
        "ICU AI"
        in selected_agents
    ):
        icu = analyze_icu_vitals(
            case["vitals"]
        )

        outputs[
            "icu"
        ] = icu

        add_agent_card(
            cards,
            "ICU AI",
            icu["status"],
        )

        integrated_summary.append(
            (
                "ICU/CDSS status: "
                f"{icu['status']}."
            )
        )


    if (
        "Radiologist AI"
        in selected_agents
    ):
        if DEMO_XRAY.exists():
            radiology = analyze_xray(
                DEMO_XRAY
            )

        else:
            radiology = {
                "prediction": (
                    "Imaging unavailable"
                ),
                "score": 0.0,
                "interpretation": (
                    "Demonstration image not found."
                ),
            }

        outputs[
            "radiology"
        ] = radiology

        add_agent_card(
            cards,
            "Radiologist AI",
            radiology[
                "prediction"
            ],
        )

        integrated_summary.append(
            (
                "CNN radiology result: "
                f"{radiology['prediction']}."
            )
        )


    if (
        "Clinical Reasoning AI"
        in selected_agents
    ):
        reasoning = (
            reason_from_symptoms(
                case[
                    "reasoning_symptoms"
                ]
            )
        )

        outputs[
            "reasoning"
        ] = reasoning

        value = (
            reasoning[
                "leading_diagnosis"
            ]
            or "No dominant differential"
        )

        add_agent_card(
            cards,
            "Clinical Reasoning AI",
            value,
        )

        integrated_summary.append(
            (
                "Clinical reasoning: "
                f"{value}."
            )
        )


    if (
        "Emergency AI"
        in selected_agents
    ):
        emergency = (
            bfs_emergency_reasoning(
                case[
                    "emergency_symptoms"
                ]
            )
        )

        outputs[
            "emergency"
        ] = emergency

        value = (
            f"{emergency['triage']}"
        )

        if (
            emergency[
                "leading_possibility"
            ]
        ):
            value += (
                " - "
                + emergency[
                    "leading_possibility"
                ]
            )

        add_agent_card(
            cards,
            "Emergency AI",
            value,
        )

        integrated_summary.append(
            (
                "Emergency BFS: "
                f"{value}."
            )
        )


    if (
        "Clinical Pharmacist AI"
        in selected_agents
    ):
        pharmacy = (
            analyze_medication_safety(
                **case[
                    "pharmacy"
                ]
            )
        )

        outputs[
            "pharmacy"
        ] = pharmacy

        add_agent_card(
            cards,
            "Clinical Pharmacist AI",
            pharmacy[
                "safety_status"
            ],
        )

        integrated_summary.append(
            (
                "Medication safety: "
                f"{pharmacy['safety_status']}."
            )
        )


    if (
        "Psychiatrist AI"
        in selected_agents
    ):
        mental = case[
            "mental_health"
        ]

        mental_health = (
            analyze_mental_health(
                mental[
                    "low_interest"
                ],
                mental[
                    "depressed_mood"
                ],
                mental[
                    "nervous"
                ],
                mental[
                    "unable_to_stop_worrying"
                ],
            )
        )

        outputs[
            "mental_health"
        ] = mental_health

        value = (
            "Depression: "
            f"{mental_health['depression_result']}; "
            "Anxiety: "
            f"{mental_health['anxiety_result']}"
        )

        add_agent_card(
            cards,
            "Psychiatrist AI",
            value,
        )

        integrated_summary.append(
            (
                "Mental-health screening: "
                f"{value}."
            )
        )


    if (
        "Oncologist AI"
        in selected_agents
    ):
        oncology = (
            dfs_oncology_reasoning(
                case[
                    "oncology_symptoms"
                ]
            )
        )

        outputs[
            "oncology"
        ] = oncology

        value = (
            oncology[
                "leading_pathway"
            ]
            or "No dominant oncology pathway"
        )

        add_agent_card(
            cards,
            "Oncologist AI",
            value,
        )

        integrated_summary.append(
            (
                "Oncology DFS: "
                f"{value}."
            )
        )


    if (
        "Treatment Planning AI"
        in selected_agents
    ):
        state = case[
            "treatment_state"
        ]

        treatment = (
            optimize_treatment(
                state[
                    "disease_extent"
                ],
                state[
                    "ecog_status"
                ],
            )
        )

        outputs[
            "treatment"
        ] = treatment

        add_agent_card(
            cards,
            "Treatment Planning AI",
            treatment[
                "recommended_strategy"
            ],
        )

        integrated_summary.append(
            (
                "Treatment RL simulation: "
                f"{treatment['recommended_strategy']}."
            )
        )


    if (
        "Patient Education AI"
        in selected_agents
    ):
        education = (
            answer_patient_question(
                case[
                    "education_question"
                ]
            )
        )

        outputs[
            "education"
        ] = education

        add_agent_card(
            cards,
            "Patient Education AI",
            education[
                "generation_status"
            ],
        )

        integrated_summary.append(
            (
                "Patient Education RAG: "
                f"{education['generation_status']}."
            )
        )


    conflict_notes = []

    receptionist = outputs.get(
        "receptionist"
    )

    emergency = outputs.get(
        "emergency"
    )

    if (
        receptionist
        and emergency
        and emergency[
            "triage"
        ] == "Emergency"
        and receptionist[
            "urgency"
        ] not in {
            "Emergency",
            "Urgent",
        }
    ):
        conflict_notes.append(
            (
                "Potential routing conflict: "
                "Emergency AI identified an emergency "
                "while Receptionist AI assigned a "
                "lower urgency."
            )
        )


    if not conflict_notes:
        conflict_notes.append(
            (
                "No explicit cross-agent conflict "
                "was detected in this synthetic scenario."
            )
        )


    communication_log.append(
        (
            "Orchestrator selection complete: "
            f"{len(selected_agents)} relevant "
            "agents invoked; "
            f"{len(skipped_agents)} irrelevant "
            "agents intentionally skipped."
        )
    )


    return {
        "scenario_key": (
            case_type
        ),

        "scenario_label": (
            case["label"]
        ),

        "patient_context": (
            patient_context
        ),

        "selected_agents": (
            selected_agents
        ),

        "skipped_agents": (
            skipped_agents
        ),

        "selection_reasons": (
            selection_reasons
        ),

        "agent_outputs": (
            outputs
        ),

        "agent_cards": (
            cards
        ),

        "communication_log": (
            communication_log
        ),

        "integrated_summary": (
            integrated_summary
        ),

        "conflict_notes": (
            conflict_notes
        ),

        "uncertainty_notes": [
            (
                "The demonstration scenario is synthetic "
                "and is linked to the selected patient "
                "for workflow traceability only."
            ),
            (
                "Only agents with relevant structured "
                "inputs are invoked."
            ),
            (
                "AI outputs are educational decision "
                "support and require human clinical review."
            ),
        ],

        "system_name": (
            SYSTEM_NAME
        ),

        "system_version": (
            SYSTEM_VERSION
        ),

        "disclaimer": (
            "Educational multi-agent clinical "
            "decision-support prototype only. "
            "Not clinically validated."
        ),
    }
