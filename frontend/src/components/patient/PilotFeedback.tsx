// PilotFeedback.tsx
import { useState } from "react";
import PageMeta from "../common/PageMeta";

/** Single AI response structure (returned by /start_session) */
interface AIResponseData {
    response_id: string;
    text: string;
}

/** Possible rating categories */
type RatingCategory =
    | "clarity"
    | "therapeutic_value"
    | "empathy"
    | "personalization"
    | "consistency"
    | "safety";

/** A map of category => numeric rating (1-5) */
interface Ratings {
    [key: string]: number | undefined;
}

/** Detailed feedback for one AI response */
interface DetailedFeedbackItem {
    ratings: Ratings;
    feedback: string;
}

/** Final feedback payload for /submit_feedback */
interface FinalResponse {
    response_id: string;
    text: string;
    rank: number | null;
    ratings: Ratings;
    feedback: string;
}

/** The top-level object we send to /submit_feedback */
interface FeedbackPayload {
    session_id: string;
    patient_id: string;
    prompt: string;
    ai_responses: FinalResponse[];
}

export default function PilotFeedback() {
    // --------------------------
    // State: Prompt & AI Responses
    // --------------------------
    const [patientPrompt, setPatientPrompt] = useState<string>("");
    const [aiResponses, setAiResponses] = useState<AIResponseData[]>([]);

    // For ranking (e.g., ["res1", "res2", "res3"])
    const [rankSequence, setRankSequence] = useState<string[]>([]);

    // Which response is selected for detailed rating
    const [selectedResponse, setSelectedResponse] = useState<string | null>(null);

    // Store feedback (ratings + text) for each response
    // Keyed by response_id, e.g. { "res1": { ratings: {...}, feedback: "" }, ... }
    const [detailedFeedback, setDetailedFeedback] = useState<{
        [responseId: string]: DetailedFeedbackItem;
    }>({});

    // --------------------------
    // 1. Fetch Multiple Responses from /start_session
    // --------------------------
    async function handleFetchResponses() {
        if (!patientPrompt.trim()) {
            alert("Please enter a prompt first.");
            return;
        }

        try {
            const res = await fetch("http://127.0.0.1:8000/start_session", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    prompt: patientPrompt,
                    patient_id: "patient_1",
                }),
            });
            if (!res.ok) {
                throw new Error("Failed to fetch responses from backend.");
            }
            const data = await res.json();
            // data.responses => array of { response_id, text }

            setAiResponses(data.responses || []);

            // Initialize detailedFeedback for each response
            const newFeedback: { [id: string]: DetailedFeedbackItem } = {};
            (data.responses || []).forEach((resp: AIResponseData) => {
                newFeedback[resp.response_id] = {
                    ratings: {},
                    feedback: "",
                };
            });
            setDetailedFeedback(newFeedback);

            // Reset rank sequence and selected response
            setRankSequence([]);
            setSelectedResponse(null);
        } catch (error) {
            console.error("Error fetching multiple responses:", error);
        }
    }

    // --------------------------
    // 2. Ranking Logic
    // --------------------------
    function handleRankClick(responseId: string) {
        setRankSequence((prev) => {
            const index = prev.indexOf(responseId);
            if (index !== -1) {
                // Un-rank if already in the sequence
                const newSeq = [...prev];
                newSeq.splice(index, 1);
                return newSeq;
            }
            // Add if there's room
            if (prev.length < 3) {
                return [...prev, responseId];
            }
            return prev;
        });
    }

    function getRankLabel(responseId: string): number | null {
        const index = rankSequence.indexOf(responseId);
        return index === -1 ? null : index + 1;
    }

    function handleResetRanks() {
        setRankSequence([]);
    }

    // --------------------------
    // 3. Detailed Feedback Logic
    // --------------------------
    function handleSelectResponse(responseId: string | null) {
        setSelectedResponse(responseId);
    }

    function handleRatingChange(
        responseId: string,
        category: RatingCategory,
        value: number
    ) {
        setDetailedFeedback((prev) => ({
            ...prev,
            [responseId]: {
                ...prev[responseId],
                ratings: {
                    ...prev[responseId].ratings,
                    [category]: value,
                },
            },
        }));
    }

    function handleTextFeedbackChange(responseId: string, text: string) {
        setDetailedFeedback((prev) => ({
            ...prev,
            [responseId]: {
                ...prev[responseId],
                feedback: text,
            },
        }));
    }

    // --------------------------
    // 4. Submit Final Feedback
    // --------------------------
    async function handleSubmitFeedback() {
        // Construct final array of AI responses with rank, ratings, feedback
        const finalResponses = aiResponses.map((resp) => {
            const rank = getRankLabel(resp.response_id);
            const df = detailedFeedback[resp.response_id] || { ratings: {}, feedback: "" };
            return {
                response_id: resp.response_id,
                text: resp.text,
                rank: rank ?? null,
                ratings: df.ratings,
                feedback: df.feedback,
            };
        });

        const feedbackPayload: FeedbackPayload = {
            session_id: "session_20250314155454", // Hard-coded for demonstration
            patient_id: "patient_1",
            prompt: patientPrompt,
            ai_responses: finalResponses,
        };

        try {
            const res = await fetch("http://127.0.0.1:8000/submit_feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(feedbackPayload),
            });
            if (!res.ok) {
                throw new Error("Failed to submit feedback.");
            }
            alert("Feedback submitted successfully!");

            // Clear local state
            setAiResponses([]);
            setRankSequence([]);
            setSelectedResponse(null);
            setDetailedFeedback({});
            setPatientPrompt("");
        } catch (error) {
            console.error("Error submitting feedback:", error);
        }
    }

    // --------------------------
    // RENDER
    // --------------------------
    return (
        <>
            <PageMeta
                title="Pilot Feedback | MemoryBridge"
                description="Expert feedback for AI memory therapy responses"
            />

            <div className="p-4 sm:p-6 lg:p-8 space-y-6 bg-white dark:bg-gray-900 min-h-screen text-gray-800 dark:text-gray-100">
                {/* Page Header */}
                <div className="space-y-1">
                    <h1 className="text-2xl font-bold">Pilot Feedback</h1>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                        A single-turn feedback interface for memory care experts to evaluate AI responses.
                    </p>
                </div>

                {/* Prompt Input & Fetch Button */}
                <div className="space-y-2">
                    <label className="block text-sm font-medium">
                        Enter Patient Prompt:
                    </label>
                    <input
                        type="text"
                        className="w-full border dark:border-gray-700 p-2 rounded-lg bg-white dark:bg-gray-900 text-sm"
                        placeholder="E.g., 'I can't remember my childhood home.'"
                        value={patientPrompt}
                        onChange={(e) => setPatientPrompt(e.target.value)}
                    />
                    <button
                        onClick={handleFetchResponses}
                        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 text-sm font-medium"
                    >
                        Fetch AI Responses
                    </button>
                </div>

                {/* AI Responses Section */}
                {aiResponses.length > 0 && (
                    <div className="flex flex-col md:flex-row gap-4">
                        {aiResponses.map((res) => {
                            const rankLabel = getRankLabel(res.response_id);
                            const isSelected = selectedResponse === res.response_id;
                            const df = detailedFeedback[res.response_id];
                            const ratings = df?.ratings || {};
                            const feedback = df?.feedback || "";

                            return (
                                <div
                                    key={res.response_id}
                                    className="flex-1 rounded-lg border border-gray-200 
                    dark:border-gray-700 bg-white dark:bg-gray-800 p-4 shadow-sm 
                    hover:shadow-md transition-shadow relative space-y-2"
                                >
                                    <p className="text-sm md:text-base">{res.text}</p>

                                    {/* Rank Toggle */}
                                    <button
                                        className={`inline-block px-3 py-1 text-sm rounded-full 
                      border dark:border-gray-600
                      ${rankLabel
                                                ? "bg-green-100 dark:bg-green-700/50 text-green-700 dark:text-green-100"
                                                : "bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-200"
                                            }`}
                                        onClick={() => handleRankClick(res.response_id)}
                                    >
                                        {rankLabel ? `Rank: ${rankLabel}` : "Click to Rank"}
                                    </button>

                                    {/* Show/Hide Ratings */}
                                    <button
                                        className={`block w-full bg-blue-100 dark:bg-blue-700/50 
                      text-blue-600 dark:text-blue-200 p-2 rounded-lg 
                      hover:bg-blue-200 dark:hover:bg-blue-700 text-sm font-medium
                      ${isSelected ? "ring-2 ring-blue-500" : ""}`}
                                        onClick={() =>
                                            handleSelectResponse(isSelected ? null : res.response_id)
                                        }
                                    >
                                        {isSelected ? "Hide Ratings" : "Show Ratings"}
                                    </button>

                                    {/* Inline Ratings for This Response */}
                                    {isSelected && (
                                        <div className="mt-2 bg-gray-50 dark:bg-gray-700 p-3 rounded space-y-2">
                                            <p className="text-xs italic text-gray-600 dark:text-gray-200">
                                                Detailed Feedback for: "{res.text}"
                                            </p>

                                            {/* Ratings Grid */}
                                            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                                                {[
                                                    "clarity",
                                                    "therapeutic_value",
                                                    "empathy",
                                                    "personalization",
                                                    "consistency",
                                                    "safety",
                                                ].map((category) => (
                                                    <div
                                                        key={category}
                                                        className="flex flex-col space-y-1"
                                                    >
                                                        <label className="text-xs font-medium capitalize">
                                                            {category.replace("_", " ")}
                                                        </label>
                                                        <select
                                                            className="border dark:border-gray-600 rounded p-1 bg-white dark:bg-gray-900 text-xs"
                                                            value={ratings[category] || ""}
                                                            onChange={(e) =>
                                                                handleRatingChange(
                                                                    res.response_id,
                                                                    category as RatingCategory,
                                                                    Number(e.target.value)
                                                                )
                                                            }
                                                        >
                                                            <option value="">--</option>
                                                            {[1, 2, 3, 4, 5].map((num) => (
                                                                <option key={num} value={num}>
                                                                    {num}
                                                                </option>
                                                            ))}
                                                        </select>
                                                    </div>
                                                ))}
                                            </div>

                                            {/* Qualitative Feedback Input */}
                                            <textarea
                                                className="w-full p-2 border dark:border-gray-600 rounded bg-white dark:bg-gray-900 text-sm"
                                                placeholder="Provide additional feedback..."
                                                value={feedback}
                                                onChange={(e) =>
                                                    handleTextFeedbackChange(res.response_id, e.target.value)
                                                }
                                            />
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                )}

                {/* Reset Ranks & Submit Feedback Buttons */}
                {aiResponses.length > 0 && (
                    <div className="space-x-2 flex justify-end">
                        <button
                            className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 px-4 py-2 rounded 
                hover:bg-gray-300 dark:hover:bg-gray-600 text-sm"
                            onClick={handleResetRanks}
                        >
                            Reset Ranks
                        </button>
                        <button
                            onClick={handleSubmitFeedback}
                            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 text-sm font-medium"
                        >
                            Submit Feedback
                        </button>
                    </div>
                )}
            </div>
        </>
    );
}
