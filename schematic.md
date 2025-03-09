                   Patient Input
                        │
                        ▼
              [Conversation Manager]  ←────────────┐
                        │                          │
                        ▼                          │
         [Goal Alignment & Monitoring Module]      │
       (Set/Update Therapy Goals, Track Emotions)  │
                        │                          │
                        ▼                          │
         [Steering Agent / Modality Selector]      │
      (Dynamically route session based on realtime |
         cues: choose SRT, CST, Narrative, etc.)   │
                   ┌─────┴────────────┐            │
                   │                  │            │
                   ▼                  ▼            │
            [SRT Agent]        [Multi-Modal Therapy Agent]
      (Spaced Recall, Reinforcement)   (CST, Narrative, Reminiscence, etc.)
                                      |            |
                   │                  │            │
                   └─────Conduct Session───────────┤
                        │                         │
                        ▼                         │
            Store Conversation History            │
                 [Memory Bank]                    │
                        │                         │
                        ▼                         │
          [Therapeutic Progress Analyzer]         │
      (Assess Outcomes, Modality Effectiveness,   │
         Emotional State, and Cognitive Metrics)  │
                        │                         │
                        ▼                         │
         ┌── Feedback Loop to Goal Alignment ─────┘
                        │
                        ▼
               [Caregiver Agent]
     (Summarize Session, Report to Clinician,
         Provide Comprehensive Feedback)
