// import React from "react";
import PageMeta from "../common/PageMeta";

// Sample data simulating AI-driven recommendations
const recommendationList = [
  {
    id: 1,
    title: "Focus on high-school memories (1970–1975)",
    description:
      "Encourage the patient to talk about high-school friends, clubs, sports, or teachers. Show any yearbook photos if available.",
  },
  {
    id: 2,
    title: "Review family vacation photos",
    description:
      "Discuss last week’s family trip. Use photos to spark recall of locations, people, and specific activities.",
  },
  {
    id: 3,
    title: "Try a 10-word recall exercise",
    description:
      "Select 10 common objects (e.g., keys, phone, cup, etc.) and ask the patient to recall them after a short interval.",
  },
  {
    id: 4,
    title: "Practice counting backward from 100 by 7s",
    description:
      "Strengthen cognitive function by practicing backward counting. Adjust difficulty based on performance.",
  },
];

export default function SessionPlanning() {
  return (
    <>
      {/* Optional: Page metadata */}
      <PageMeta
        title="Session Planning | MemoryBridge"
        description="AI-driven caregiver recommendations for memory sessions"
      />

      {/* Page container */}
      <div className="p-4 sm:p-6 lg:p-8 space-y-6">
        {/* Page header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white/90">
            Session Planning
          </h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Below are recommended memory exercises and conversation prompts based on
            the patient’s recent performance.
          </p>
        </div>

        {/* Recommendation list */}
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {recommendationList.map((rec) => (
            <div
              key={rec.id}
              className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]"
            >
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
                {rec.title}
              </h3>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                {rec.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
